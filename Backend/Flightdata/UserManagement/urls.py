from rest_framework_extensions.routers import ExtendedDefaultRouter

from UserManagement.views.login_viewset import LoginViewSet

router = ExtendedDefaultRouter(trailing_slash=False)

################################### Connector API's #############################################
router.register('user', LoginViewSet, basename='user')


urlpatterns = router.urls
