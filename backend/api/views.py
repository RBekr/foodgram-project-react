from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from users.models import User, UserFollowing

from .filters import IngredientFilterBackend, RecipeFilterBackend
from .permissitons import IsAdminOrAuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import (FollowSerializer, FollowUsersSerializer,
                          IngredientSerializer, RecipeSerializerGet,
                          RecipeSerializerSet, SimpleRecipeSerializer,
                          TagSerializer)


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

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeSerializerGet
        return RecipeSerializerSet

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        recipes = IngredientRecipe.objects.filter(
            recipe__in=request.user.shopping_cart.all()
        )
        ingredients = recipes.values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_count=Sum('amount'))
        response = HttpResponse(content_type='text/plain; charset=utf-8')
        filename = f'{request.user}_shopping_cart.txt'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        recipes_name = ', '.join(
            set([recipe.recipe.name for recipe in recipes])
        )
        response.write(f'Ингредиенты для рецептов {recipes_name}\n\n')
        response.write('Ingredient\tCount\tUnit\n')

        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            count = ingredient['ingredient_count']
            measurement_unit = ingredient['ingredient__measurement_unit']
            line = f'{name} - \t{count}\t{measurement_unit}\n'
            response.write(line)
        response.write('\n Автор: Бекренёв Руслан; Приложение  - FOORGRAM')

        return response


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
