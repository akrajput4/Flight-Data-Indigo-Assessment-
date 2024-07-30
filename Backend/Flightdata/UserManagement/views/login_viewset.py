from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from UserManagement.models.user_model import User
from rest_framework import status
from UserManagement.serializers.user_serializer import UserSerializer
from common.permission import Permission
from common.token import create_jwt_token
from utils.helper_methods import hash_string_with_secret_key, validate_email, validate_password
from django.conf import settings

from utils.logger import service_logger


class LoginViewSet(NestedViewSetMixin, ModelViewSet):
    model = User
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        """
        Handle user login by verifying email and password, and returning a JWT token if authentication is successful.

        Args:
            request (Request): The HTTP request containing the login credentials.

        Returns:
            Response: A Response object with status and message or token.
        """
        try:
            # Retrieve email and password from the request data
            email_id = request.data.get('email_id', None)
            password = request.data.get('password', None)

            # Check if the email is provided
            if email_id is None or len(email_id) == 0:
                service_logger.info("Email ID is missing from the request.")
                return Response({'error': True, 'message': 'email id is required'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Check if the password is provided
            if password is None or len(password) == 0:
                service_logger.info("Password is missing from the request.")
                return Response({'error': True, 'message': 'password is required'},
                                status=status.HTTP_400_BAD_REQUEST)

            ###################### Authenticate the user ############################

            # Fetch the user record from the database
            user_queryset = self.model.objects.filter(email_id=email_id).values('email_id', 'password')
            if user_queryset is None or len(user_queryset) == 0:
                service_logger.info(f"No user found with email: {email_id}")
                return Response({'error': True, 'message': 'No user found with this email'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Hash the provided password using the secret key
            hashed_password = hash_string_with_secret_key(password, settings.SECRET_KEY_FOR_PASSWORD)


            token = None
            # Check if the hashed password matches the stored password
            if hashed_password == user_queryset[0].get('password'):
                # Generate a JWT token for the authenticated user
                token = create_jwt_token(email_id)

                service_logger.info(f"User authenticated successfully: {email_id}")
            else:
                service_logger.info(f"Invalid login attempt for email: {email_id}")
                return Response({'error': True, 'message': 'Invalid Login Credentials'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Prepare the response data
            response_data = {
                'email_id': email_id,
                'token': token
            }
            return Response({'success': True, 'data': response_data}, status=status.HTTP_200_OK)

        except Exception as e:
            # Log any exceptions that occur during the login process
            service_logger.error(f"An error occurred during login: {str(e)}")
            return Response({'error': True, 'message': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def sign_up(self, request, *args, **kwargs):
        """
        Handle user sign-up by validating and registering a new user.

        Args:
            request (Request): The HTTP request containing the user registration details.

        Returns:
            Response: A Response object with status and message.
        """
        try:
            # Retrieve user details from the request data
            email_id = request.data.get('email_id', None)
            password = request.data.get('password', None)
            first_name = request.data.get('first_name', None)
            last_name = request.data.get('last_name', None)

            # Validate email presence
            if email_id is None:
                service_logger.info("Email is missing from the sign-up request.")
                return Response({'error': True, 'message': 'email is required'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Validate email format
            if not validate_email(email_id):
                service_logger.info(f"Invalid email format provided: {email_id}")
                return Response({'error': True, 'message': 'Enter a proper email id'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Check if the email is already registered
            email_queryset = self.model.objects.filter(email_id=email_id)
            if email_queryset.exists():
                service_logger.info(f"Email already registered: {email_id}")
                return Response({'error': True, 'message': 'User is already registered with this email'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Validate password presence and format
            if password is None:
                service_logger.info("Password is missing from the sign-up request.")
                return Response({'error': True, 'message': 'password is required'},
                                status=status.HTTP_400_BAD_REQUEST)

            if not validate_password(password):
                service_logger.info(f"Password validation failed for email: {email_id}")
                return Response({'error': True,
                                 'message': 'Password should contain one special character, a number, and start with a capital letter'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Validate first and last names
            if not first_name or not last_name:
                service_logger.info("First name or last name is missing from the sign-up request.")
                return Response({'error': True, 'message': 'First and last name should not be none'},
                                status=status.HTTP_400_BAD_REQUEST)

            # If all validations pass, proceed with user creation (this part is assumed to be implemented elsewhere)
            user_data = {
                'email_id': email_id,
                'password': hash_string_with_secret_key(password, settings.SECRET_KEY_FOR_PASSWORD),
                'first_name': first_name,
                'last_name': last_name
            }
            serializer = self.serializer_class(data=user_data)

            # Attempt to save the user data
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                service_logger.info(f"User successfully registered: {email_id}")
                return Response({'success': True, 'message': 'User registered successfully'},
                                status=status.HTTP_201_CREATED)
            else:
                service_logger.error(f"User registration failed for email: {email_id} with errors: {serializer.errors}")
                return Response({'error': True, 'message': 'User registration failed'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log the exception
            service_logger.error(f"An error occurred during sign-up: {str(e)}")
            return Response({'error': True, 'message': 'An error occurred'},
                            status=status.HTTP_400_BAD_REQUEST)
