from rest_framework.serializers import ModelSerializer
from contact.models import Contact

class ContactSerializer(ModelSerializer):
    class Meta:
        fields = ['name', 'surname', 'subject', 'phone', 'message']
        model = Contact
    
    def create(self, validated_data):
        return super().create(validated_data)
        