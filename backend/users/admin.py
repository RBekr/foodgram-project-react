from django.conf import settings
from django.contrib import admin

from .models import User, UserFollowing


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id', 'username', 'email',
                    'first_name', 'last_name',
                    'date_joined', 'last_login')
    list_editable = ('first_name', 'last_name',)
    list_filter = ('username', 'email',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


@admin.register(UserFollowing)
class FollowAdmin(admin.ModelAdmin):
    model = UserFollowing
    list_display = ('id', 'user_id', 'following_user_id',)
    list_filter = ('user_id', 'following_user_id',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY
