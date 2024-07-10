from django.contrib import admin
from .models import CustomUser, Address, TaskerSkillProof
from request.models import Request

admin.site.register(CustomUser)
admin.site.register(Address)
admin.site.register(TaskerSkillProof)
admin.site.register(Request)
