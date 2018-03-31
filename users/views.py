from django.core.cache import caches
from django.contrib.auth import (
    login,
    logout,
    authenticate
)
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    SignUpStep1Serializer,
    SignUpStep2Serializer,
    SignInSerializer,
    CurrentUserSerializer,
)
from .models import User
from .tasks import send_verification_email

cache_sign_up = caches['sign_up']


@api_view(['POST'])
def sign_up_step1(request):
    serializer = SignUpStep1Serializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get("email")
        send_verification_email.delay(email)
        return Response()

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def sign_up_step2(request):
    serializer = SignUpStep2Serializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get("email")
        first_name = serializer.data.get("first_name")
        last_name = serializer.data.get("last_name")
        password = serializer.data.get("password")
        confirmation_key1 = serializer.data.get("confirmation_key")

        confirmation_key2 = cache_sign_up.get(email)

        if confirmation_key2 is not None and confirmation_key1 == confirmation_key2:
            user = User.objects.create_user(
                email,
                password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            return Response()

        return Response({'confirmation_key': 'Не верный код'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def sign_in(request):
    serializer = SignInSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get("email")
        password = serializer.data.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response()


class RetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer

    def get_object(self):
        return self.request.user
