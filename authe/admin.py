from django.contrib import admin
from .models import CustomUser, Address, TaskerSkillProof

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_approved']
    list_filter = ['is_approved']
    actions = ['approve_taskers']

    def approve_taskers(self, request, queryset):
        queryset.update(is_approved=True)
    approve_taskers.short_description = "Approve selected taskers"
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'state', 'city', 'pincode', 'full_address')

@admin.register(TaskerSkillProof)
class TaskerSkillProofAdmin(admin.ModelAdmin):
    list_display = ('tasker', 'pdf', 'uploaded_at')
