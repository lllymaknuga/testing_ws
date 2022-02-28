from rest_framework.serializers import ModelSerializer

from my_chat.models import City, Message


class CitySerializer(ModelSerializer):
    class Meta:
        fields = ['name']
        model = City


class MessageSerializer(ModelSerializer):
    class Meta:
        fields = ['content', 'city_id']
        model = Message

    def save(self, **kwargs):
        print(2)
        print(self.validated_data)
        print(2)
        super().save(**kwargs)
