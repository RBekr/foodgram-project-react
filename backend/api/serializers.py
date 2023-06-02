from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from users.models import UserFollowing

from .validators import username_not_me


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )
        read_only_fields = ('id',)


class CustomUserCreateSerializer(UserCreateSerializer):

    def validate_username(self, value):
        return username_not_me(value)


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = ('id', 'email', 'username',
                  'password', 'first_name', 'last_name', 'is_subscribed', )
        extra_kwargs = {'password': {'write_only': True}}

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserFollowing.objects.filter(
                user_id=obj.id,
                following_user_id=request.user.id
            ).exists()
        return False

    def validate_username(self, value):
        return username_not_me(value)


class RecipeSerializerGet(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'tags', 'author',
                  'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'image', 'text', 'cooking_time',)
        read_only_fields = ('id',)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return Recipe.objects.filter(
            pk=obj.id,
            favorited_by=request.user
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return Recipe.objects.filter(
            pk=obj.id,
            added_by=request.user
        ).exists()

    def get_ingredients(self, obj):
        ingredient_recipes = IngredientRecipe.objects.filter(recipe=obj)
        serialized_data = []
        for ingredient_recipe in ingredient_recipes:
            ingredient_data = IngredientSerializer(
                ingredient_recipe.ingredient
            ).data
            ingredient_data['amount'] = ingredient_recipe.amount
            serialized_data.append(ingredient_data)
        return serialized_data


class RecipeSerializerSet(serializers.ModelSerializer):
    ingredients = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(),
        ),
        write_only=True,
    )
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time', )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=ingredient['amount']
            )
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        IngredientRecipe.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])
            IngredientRecipe.objects.get_or_create(
                recipe=instance,
                ingredient=current_ingredient,
                amount=ingredient['amount']
            )
        instance.tags.set(tags)
        return super().update(instance, validated_data)


class SimpleRecipeSerializer(RecipeSerializerGet):
    class Meta(RecipeSerializerGet.Meta):
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ('user_id', 'following_user_id')

    def validate(self, attrs):
        if attrs['user_id'] == attrs['following_user_id']:
            raise serializers.ValidationError(
                'Вы не можете подписаться на сами себя'
            )
        return attrs


class FollowUsersSerializer(CustomUserSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = (CustomUserSerializer.Meta.fields
                  + ('recipes', 'recipes_count'))

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes_limit = self.context.get(
            'request'
        ).query_params.get('recipes_limit', None)
        if recipes_limit:
            recipes = obj.recipes.all()[:int(recipes_limit)]
        serializer = SimpleRecipeSerializer(recipes, many=True)
        return serializer.data
