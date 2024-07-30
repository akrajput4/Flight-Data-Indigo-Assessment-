from rest_framework_extensions.routers import ExtendedDefaultRouter

from .views.flight_viewset import FlightsViewSet, FlightScheduleViewSet

router = ExtendedDefaultRouter(trailing_slash=False)

################################### Connector API's #############################################
router.register('add-flight', FlightsViewSet, basename='add-flight')
router.register('schedule-flight', FlightScheduleViewSet, basename='schedule-flight')

urlpatterns = router.urls
