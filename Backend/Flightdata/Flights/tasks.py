from celery import shared_task
from Flights.models import FlightSchedule, Flight
from UserManagement.models import User
from utils.helper_methods import send_email


@shared_task
def send_email_to_passengers(flight_id):
    try:
        # Get the flight details
        flight = Flight.objects.get(id=flight_id)
        message = f"Hi, your flight details have been updated. Here are the new flight details: {flight}"

        # Get the users associated with the flight
        user_queryset = FlightSchedule.objects.filter(flight_id=flight_id)

        for user_schedule in user_queryset:
            # Get user email
            user_email = User.objects.get(id=user_schedule.user_id).email
            send_email(
                subject="Updated Flight Details",
                message=message,
                recipient_list=[user_email]
            )
    except Flight.DoesNotExist:
        # Handle the case where the flight does not exist
        print(f"Flight with id {flight_id} does not exist.")
    except User.DoesNotExist:
        # Handle the case where a user does not exist
        print(f"User associated with flight schedule does not exist.")
    except Exception as e:
        # Handle any other exceptions
        print(f"An error occurred: {str(e)}")


