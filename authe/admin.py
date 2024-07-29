from django import forms
from django.contrib import admin
from .models import CustomUser, Address, TaskerSkillProof
from request.models import Request

class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_user_type(self):
        # No validation needed for user_type here since it's not editable
        return self.instance.user_type

class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserAdminForm  # Use the custom form

    # Make the user_type field read-only
    readonly_fields = ('user_type',)

    def user_type_display(self, obj):
        return 'user' if obj.user_type == 1 else 'tasker'

    user_type_display.short_description = 'User Type'

    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type_display')
    list_filter = ('user_type',)
    search_fields = ('username', 'email')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address)
admin.site.register(TaskerSkillProof)
admin.site.register(Request)
