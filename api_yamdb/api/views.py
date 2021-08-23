from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ParseError
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import (CharFilter, DjangoFilterBackend,
                                           FilterSet)

from reviews.models import Category, Comment, Genre, Review, Title, User
from users.models import User

from .permissions import (AdminOnly, AdminOrReadOnly,
                          IsAuthorOrModerOrAdmin, OnlyOwnAccount)
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomUserSerializer, GenreSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitlePostSerializer, TitleSerializer,
                          TokenSerializer)


class FilterTitle(FilterSet):
    category = CharFilter(field_name='category__slug', lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['year']


class CreateListDestroy(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = FilterTitle
    search_fields = ('name', 'year', 'genre__slug', 'category__slug')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitlePostSerializer

    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            queryset = (Title.objects.prefetch_related('reviews').all().
                        annotate(rating=Avg('reviews__score')).
                        order_by('name'))
            return queryset
        return Title.objects.all()

    def perform_create(self, serializer):
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        return super().perform_update(serializer)


class GenreViewSet(CreateListDestroy):
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    search_fields = ('name', 'slug')
    filterset_fields = ('name', 'slug')


class CategoryViewSet(CreateListDestroy):
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('name', 'slug')
    search_fields = ('name', 'slug')


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
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReviewViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModerOrAdmin,)

    def title_rating_update(self, title_id):
        title = get_object_or_404(Title, pk=title_id)
        rating = title.reviews.aggregate(Avg('score'))
        return round(rating['score__avg'])

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        if title.reviews.filter(author=self.request.user).exists():
            raise ParseError(
                'Возможен только один отзыв на произведение!'
            )
        serializer.save(
            author=self.request.user,
            title_id=title.id
        )
        title.rating = self.title_rating_update(title.id)
        title.save()

    def perform_update(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        # сохранить имя автора, если правит не он
        review_id = self.kwargs.get('pk')
        author = Review.objects.get(pk=review_id).author
        serializer.save(
            author=author,
            title_id=title.id
        )
        title.rating = self.title_rating_update(title.id)
        title.save()

    def perform_destroy(self, instance):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        instance.delete()
        title.rating = self.title_rating_update(title.id)
        title.save()


class CommentViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModerOrAdmin,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review_id=review.id)

    def perform_update(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        # сохранить имя автора, если правит не он
        comment_id = self.kwargs.get('pk')
        author = Comment.objects.get(pk=comment_id).author
        serializer.save(
            author=author,
            review_id=review.id
        )
