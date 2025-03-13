from rest_framework import generics
from .models import Campaign, Character, NPC, Monster, Item, Quest, Event
from .serializers import (
    CampaignSerializer, CharacterSerializer, NPCSerializer, MonsterSerializer, ItemSerializer,
    QuestSerializer, EventSerializer, RegisterSerializer
)
from rest_framework.reverse import reverse
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrAdmin


class LoginAPIView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairView.serializer_class


class TokenRefreshAPIView(TokenRefreshView):
    permission_classes = [AllowAny]


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10


class CampaignList(generics.ListCreateAPIView):
    queryset = Campaign.objects.annotate(num_characters=Count('characters')).all()
    serializer_class = CampaignSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ['name', 'status']
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status']
    name = 'campaign-list'


class CampaignDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [IsAdminUser]
    name = 'campaign-detail'


class CharacterList(generics.ListCreateAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    permission_classes = [IsAuthenticated]
    ordering_fields = ['name', 'level']
    filterset_fields = ['race', 'character_class']
    name = 'character-list'


class CharacterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = [IsOwnerOrAdmin]
    name = 'character-detail'


class NPCList(generics.ListCreateAPIView):
    queryset = NPC.objects.all()
    serializer_class = NPCSerializer
    permission_classes = [IsAdminUser]
    name = 'npc-list'


class NPCDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = NPC.objects.all()
    serializer_class = NPCSerializer
    permission_classes = [IsAdminUser]
    name = 'npc-detail'


class MonsterList(generics.ListCreateAPIView):
    queryset = Monster.objects.all()
    serializer_class = MonsterSerializer
    permission_classes = [IsAdminUser]
    name = 'monster-list'


class MonsterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Monster.objects.all()
    serializer_class = MonsterSerializer
    permission_classes = [IsAdminUser]
    name = 'monster-detail'


class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAdminUser]
    name = 'item-list'


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAdminUser]
    name = 'item-detail'


class QuestList(generics.ListCreateAPIView):
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer
    permission_classes = [IsAuthenticated]
    name = 'quest-list'


class QuestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer
    permission_classes = [IsAdminUser]
    name = 'quest-detail'


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    name = 'event-list'


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]
    name = 'event-detail'


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': RegisterSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'campaigns': reverse(CampaignList.name, request=request),
            'characters': reverse(CharacterList.name, request=request),
            'npcs': reverse(NPCList.name, request=request),
            'monsters': reverse(MonsterList.name, request=request),
            'items': reverse(ItemList.name, request=request),
            'quests': reverse(QuestList.name, request=request),
            'events': reverse(EventList.name, request=request),
        })