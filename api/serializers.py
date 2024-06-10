from rest_framework import serializers
from .models import Company, User

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    location = serializers.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].choices = self.get_location_choices()

    def get_location_choices(self):
        companies = Company.objects.values_list('location', flat=True).distinct()
        return [(location, location) for location in companies]

    def validate(self, data):
        """
        Check that the company type matches the user's work type.
        """
        company = data.get('company')
        work = data.get('work')

        if company and work and company.type != work:
            raise serializers.ValidationError("The company type must match the user's work type.")

        return data
