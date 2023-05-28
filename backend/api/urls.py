from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APIFavorite, APIFollow, APIShoppingCart, CustomUserViewSet,
                    FollowsViewSet, IngredientViewSet, RecipeViewSet,
                    TagViewSet)

app_name = 'api'
router = DefaultRouter()
router.register('users/subscriptions', FollowsViewSet, basename='subscriptions-list')
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:pk>/shopping_cart/', APIShoppingCart.as_view(), name='shopping_cart'),
    path('recipes/<int:pk>/favorite/', APIFavorite.as_view(), name='favorite'),
    path('users/<int:pk>/subscribe/', APIFollow.as_view(), name='subscribe'),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
]