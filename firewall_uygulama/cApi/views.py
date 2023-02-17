from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import *
from rest_framework.parsers import JSONParser
from rest_framework import views, status
from rest_framework.response import Response


     

from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import *
from .models import *
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin,UpdateModelMixin,RetrieveModelMixin


class djangoUserViewSet(ListModelMixin, UpdateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = djangoUserSerializer
    queryset = DjangoUser.objects.all()



class UserViewSet(ListModelMixin, UpdateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class LogViewSet(ListModelMixin, UpdateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogSerializer
    queryset = Log.objects.all()
    
class EmailViewSet(ListModelMixin, UpdateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmailSerializer
    queryset = email_verification.objects.all()










class djangoUserView(views.APIView):
    def get(self, request):
        users = DjangoUser.objects.all()
        serializer = djangoUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = djangoUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(views.APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(views.APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogView(views.APIView):
    def get(self, request):
        logs = Log.objects.all()
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = LogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailView(views.APIView):
    def get(self, request):
        emails = email_verification.objects.all()
        serializer = EmailSerializer(emails, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = EmailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerifyView(views.APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = EmailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
