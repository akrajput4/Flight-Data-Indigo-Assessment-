from datetime import datetime

from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.exceptions import NotFound, ValidationError
from Flights.models.flight_model import Flight, FlightSchedule
from Flights.serializers.flight_serializer import FlightSerializer, FlightScheduleSerializer
from Flights.tasks import send_email_to_passengers
from utils.logger import service_logger


class FlightsViewSet(NestedViewSetMixin, ModelViewSet):
    model = Flight
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()

    def create(self, request, *args, **kwargs):
        service_logger.info("Create request received with data: %s", request.data)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            service_logger.info("Flight entry created successfully: %s", serializer.data)
            return Response({"success": True, "message": 'Flight entry created', "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except ValidationError as ve:
            service_logger.error("Validation error: %s", ve)
            return Response({"success": False, "message": "Validation error", "errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            service_logger.error("An error occurred: %s", str(e))
            return Response({"success": False, "message": "An error occurred", "errors": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):

        try:
            queryset = self.queryset
            params = request.query_params

            # Filter by airline
            airline = params.get('airline')
            if airline:
                queryset = queryset.filter(airline=airline)

            # Filter by departure date
            departure_date = params.get('departure_date')
            if departure_date:
                try:
                    departure_date = datetime.strptime(departure_date, "%Y-%m-%d")
                    queryset = queryset.filter(departure_schedule__date=departure_date)
                except ValueError:
                    service_logger.error("Invalid departure date format: %s", departure_date)
                    return Response({"success": False, "message": "Invalid departure date format. Use YYYY-MM-DD."},
                                    status=status.HTTP_400_BAD_REQUEST)

            # Filter by arrival date
            arrival_date = params.get('arrival_date')
            if arrival_date:
                try:
                    arrival_date = datetime.strptime(arrival_date, "%Y-%m-%d")
                    queryset = queryset.filter(arrival_schedule__date=arrival_date)
                except ValueError:
                    service_logger.error("Invalid arrival date format: %s", arrival_date)
                    return Response({"success": False, "message": "Invalid arrival date format. Use YYYY-MM-DD."},
                                    status=status.HTTP_400_BAD_REQUEST)

            # Filter by departure time range
            departure_time_start = params.get('departure_time_start')
            departure_time_end = params.get('departure_time_end')
            if departure_time_start and departure_time_end:
                try:
                    departure_time_start = datetime.strptime(departure_time_start, "%H:%M:%S").time()
                    departure_time_end = datetime.strptime(departure_time_end, "%H:%M:%S").time()
                    queryset = queryset.filter(
                        departure_schedule__time__range=(departure_time_start, departure_time_end))
                except ValueError:
                    service_logger.error("Invalid departure time format: %s - %s", departure_time_start,
                                         departure_time_end)
                    return Response({"success": False, "message": "Invalid departure time format. Use HH:MM:SS."},
                                    status=status.HTTP_400_BAD_REQUEST)

            # Filter by arrival time range
            arrival_time_start = params.get('arrival_time_start')
            arrival_time_end = params.get('arrival_time_end')
            if arrival_time_start and arrival_time_end:
                try:
                    arrival_time_start = datetime.strptime(arrival_time_start, "%H:%M:%S").time()
                    arrival_time_end = datetime.strptime(arrival_time_end, "%H:%M:%S").time()
                    queryset = queryset.filter(arrival_schedule__time__range=(arrival_time_start, arrival_time_end))
                except ValueError:
                    service_logger.error("Invalid arrival time format: %s - %s", arrival_time_start, arrival_time_end)
                    return Response({"success": False, "message": "Invalid arrival time format. Use HH:MM:SS."},
                                    status=status.HTTP_400_BAD_REQUEST)

            # Filter by seat availability
            min_seats_available = params.get('min_seats_available')
            if min_seats_available:
                try:
                    min_seats_available = int(min_seats_available)
                    queryset = queryset.filter(seats_available__gte=min_seats_available)
                except ValueError:
                    service_logger.error("Invalid minimum seats available format: %s", min_seats_available)
                    return Response(
                        {"success": False, "message": "Invalid format for minimum seats available. Use an integer."},
                        status=status.HTTP_400_BAD_REQUEST)

            # Filter by flight duration range
            flight_duration_min = params.get('flight_duration_min')
            flight_duration_max = params.get('flight_duration_max')
            if flight_duration_min and flight_duration_max:
                try:
                    queryset = queryset.filter(flight_duration__range=(flight_duration_min, flight_duration_max))
                except ValueError:
                    service_logger.error("Invalid flight duration format: %s - %s", flight_duration_min,
                                         flight_duration_max)
                    return Response({"success": False, "message": "Invalid format for flight duration range."},
                                    status=status.HTTP_400_BAD_REQUEST)

            if not queryset.exists():
                service_logger.warning("No flights found.")
                raise NotFound("No flights found.")

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            service_logger.info("List request successful.")
            return Response(serializer.data)

        except Exception as e:
            service_logger.error("An error occurred during list operation: %s", str(e))
            return Response({"success": False, "message": "An error occurred", "errors": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            # Get the instance to be updated
            instance = self.get_object()
            flight_id = kwargs['pk']
            # Initialize the serializer with the instance and request data
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            # Validate the serializer
            serializer.is_valid(raise_exception=True)
            # Perform the update operation
            self.perform_update(serializer)
            service_logger.info("Flight updated successfully with data: %s", serializer.data)
            send_email_to_passengers.apply_async(args=[flight_id], countdown=0)

            return Response(serializer.data)
        except Exception as e:
            service_logger.error("An error occurred during update operation: %s", str(e))
            return Response({"success": False, "message": "An error occurred", "errors": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        try:
            # Call the update method with partial=True
            response = self.update(request, *args, **kwargs)
            service_logger.info("Partial update successful with response data: %s", response.data)
            return response
        except Exception as e:
            service_logger.error("An error occurred during partial update operation: %s", str(e))
            return Response({"success": False, "message": "An error occurred", "errors": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        # Log the incoming request with the flight ID to be "deleted"
        try:
            # Retrieve the instance to be updated
            instance = self.get_object()

            # Update the status of the flight to '2' (soft delete)
            instance.status = 2
            instance.save()

            # Log successful status update
            service_logger.info("Flight status updated to '2' successfully for ID: %s", instance.id)

            # Return a 204 No Content response indicating successful deletion
            return Response({'success': True, 'message': 'Deleted Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle any unexpected errors that occur during the process
            service_logger.error("An error occurred during destroy operation: %s", str(e))
            return Response({"success": False, "message": "An error occurred", "errors": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self):
        try:
            return super().get_object()
        except Flight.DoesNotExist:
            raise NotFound("Flight not found.")


class FlightScheduleViewSet(NestedViewSetMixin, ModelViewSet):
    model = FlightSchedule
    serializer_class = FlightScheduleSerializer
    queryset = FlightSchedule.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                with transaction.atomic():
                    serializer.save()
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Unexpected error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Unexpected error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            with transaction.atomic():
                instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({'error': 'FlightSchedule not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Unexpected error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Unexpected error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': 'Unexpected error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
