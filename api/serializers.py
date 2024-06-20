from rest_framework import serializers
from .models import Tasker

class TaskerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasker
        fields = ['tasker_id','username','email','password','about','is_active','service','price','address_state','address_city','address_full','pincode','phone_no']
