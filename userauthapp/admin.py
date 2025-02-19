from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register User model with custom UserAdmin
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_verified', 'date_joined', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)
    
    # Add is_verified to fieldsets
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Verification', {'fields': ('is_verified', 'verification_token')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
