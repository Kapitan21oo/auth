from django.core import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.contrib.auth import authenticate, login
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, \
    UserProfileUpdateSerializer
from django.core.cache import cache
from auth_app.tasks import send_otp_email


@permission_classes([permissions.AllowAny])
class UserRegistrationView(APIView):
    """
        View for user registration.

        Request (POST):
        - email (string)
        - password (string)
git
        Response (201 Created):
        - message (string)

        Response (400 Bad Request):
        - Validation errors
        """

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
        View for user login.

        Request (POST):
        - email (string)
        - password (string)

        Response (200 OK):
        - access_token (string)
        - message (string)

        Response (400 Bad Request):
        - Invalid email or password
        """

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:

                send_otp_email.delay(email)

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                print(user.email)
                return Response({'access_token': access_token, 'message': 'OTP code sent successfully'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    """
        View for OTP verification.

        Request (POST):
        - email (string)
        - otp_code (string)

        Response (200 OK):
        - message (string)

        Response (400 Bad Request):
        - Invalid OTP code
        """

    def post(self, request):
        email = request.data.get('email')
        input_otp_code = request.data.get('otp_code')

        stored_otp_code = cache.get(f'otp_code_{email}')

        if stored_otp_code and input_otp_code == stored_otp_code:
            user = CustomUser.objects.get(email=email)
            if user:

                login(request, user)
                return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
        View for retrieving user profile.

        Requires authentication.

        Response (200 OK):
        - User profile data

        Response (401 Unauthorized):
        - User is not authenticated
        """

    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileUpdateView(APIView):
    """
        View for updating user profile.

        Requires authentication.

        Request (PUT):
        - User profile data

        Response (200 OK):
        - message (string)

        Response (400 Bad Request):
        - Validation errors
        """

    def put(self, request):
        serializer = UserProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAccountDeleteView(APIView):
    """
       View for deleting user account.

       Requires authentication.

       Response (204 No Content):
       - Account deleted successfully
       """

    def delete(self, request):
        user = request.user.delete()

        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
