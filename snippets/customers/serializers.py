from rest_framework.serializers import ModelSerializer

from customers.models import MyUser,SnippetTitle,SnippetSheetDetails

from rest_framework import serializers


class UserCreationSerializer(ModelSerializer):
    class Meta:
        model=MyUser
        fields=["email","role","password"]
    def create(self, validated_data):
        return MyUser.objects.create_user(email=validated_data["email"],
                                          role=validated_data["role"],
                                          password=validated_data["password"]
                                          )


class SignInSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class AddingSnippetTitleSerializer(ModelSerializer):
    class Meta:
        model=SnippetTitle
        fields="__all__"


class AddingSnippetDescriptionsSerializer(ModelSerializer):
    class Meta:
        model=SnippetSheetDetails
        fields="__all__"