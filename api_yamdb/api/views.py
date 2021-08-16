from .permissions import AdminOnly, OnlyOwnAccount
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from rest_framework import viewsets
from .serializers import CustomUserSerializer, TokenSerializer
from .serializers import SignUpSerializer
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import IsAuthenticated, AllowAny


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = CustomUserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    permission_classes = (AdminOnly,)

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=(OnlyOwnAccount, IsAuthenticated))
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(user,
                                             data=request.data, partial=True)
            if serializer.is_valid():
                if 'role' in request.data:
                    if user.role != 'user':
                        serializer.save()
                else:
                    serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if not User.objects.filter(username=request.data['username'],
                                       email=request.data['email']).exists():
                serializer.save()
            user = User.objects.get(username=request.data['username'],
                                    email=request.data['email'])
            conformation_code = default_token_generator.make_token(user)
            send_mail(f'Hello, {str(user.username)}! Your code is here!',
                      conformation_code,
                      'donotrespond@yamdb.com',
                      [request.data['email']],
                      fail_silently=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    if request.method == 'POST':
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, username=request.data['username'])
            confirmation_code = request.data['confirmation_code']
            if default_token_generator.check_token(user, confirmation_code):
                token = get_tokens_for_user(user)
                response = {'token': str(token['access'])}
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_MOTHOD_NOT_ALLOWED)
