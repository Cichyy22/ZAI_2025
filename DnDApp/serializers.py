from rest_framework import serializers
from .models import Campaign, Character, NPC, Monster, Item, Quest, Event
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = '__all__'


class CharacterSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # campaign = CampaignSerializer()

    class Meta:
        model = Character
        fields = '__all__'


class NPCSerializer(serializers.ModelSerializer):
    # campaign = CampaignSerializer()

    class Meta:
        model = NPC
        fields = '__all__'


class MonsterSerializer(serializers.ModelSerializer):
    # campaign = CampaignSerializer()

    class Meta:
        model = Monster
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    # characters = CharacterSerializer(many=True, required=False, allow_null=True)
    # npcs = NPCSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Item
        fields = '__all__'


class QuestSerializer(serializers.ModelSerializer):
    # campaign = CampaignSerializer()
    # characters = CharacterSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Quest
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    # campaign = CampaignSerializer()

    class Meta:
        model = Event
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
