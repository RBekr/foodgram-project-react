from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import Ingredient, Recipe, Tag
from users.models import User, UserFollowing

from .filters import IngredientFilterBackend, RecipeFilterBackend
from .permissitons import IsAdminOrAuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import (FollowSerializer, FollowUsersSerializer,
                          IngredientSerializer, RecipeSerializerGet,
                          RecipeSerializerSet, SimpleRecipeSerializer,
                          TagSerializer)
from .utils import shopping_cart_response


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly, )


class IngredientViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilterBackend, )


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (RecipeFilterBackend, )
    permission_classes = (IsAdminOrAuthorOrReadOnly, )

    # def get_queryset(self):
    #     return Recipe.objects.select_related(
    #         'author'
    #     ).prefetch_related('ingredients', 'tags')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeSerializerGet
        return RecipeSerializerSet

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['request'] = self.request
    #     return context

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        return shopping_cart_response(request)


class APIShoppingCart(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = SimpleRecipeSerializer(recipe)
        user = request.user
        recipe.added_by.add(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        recipe.added_by.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class APIFavorite(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = SimpleRecipeSerializer(recipe)
        user = request.user
        recipe.favorited_by.add(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        recipe.favorited_by.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class APIFollow(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        data = {
            'user_id': pk,
            'following_user_id': request.user.id
        }
        follow_serializer = FollowSerializer(data=data)
        if follow_serializer.is_valid():
            follow_serializer.save()
            user = User.objects.get(pk=pk)
            serializer = FollowUsersSerializer(
                user,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(
            UserFollowing,
            user_id=pk,
            following_user_id=request.user
        )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = FollowUsersSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return User.objects.filter(
            following__following_user_id=self.request.user.id
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CustomUserViewSet(UserViewSet):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
