from django.urls import path
from . import views

urlpatterns = [
    # Punkt wejścia API
    path('', views.ApiRoot.as_view(), name='api-root'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('token/refresh/', views.TokenRefreshAPIView.as_view(), name='token_refresh'),
    # Kampanie
    path('api/campaigns/', views.CampaignList.as_view(), name='campaign-list'),
    path('api/campaigns/<int:pk>/', views.CampaignDetail.as_view(), name='campaign-detail'),

    # Postacie
    path('api/characters/', views.CharacterList.as_view(), name='character-list'),
    path('api/characters/<int:pk>/', views.CharacterDetail.as_view(), name='character-detail'),

    # NPC
    path('api/npcs/', views.NPCList.as_view(), name='npc-list'),
    path('api/npcs/<int:pk>/', views.NPCDetail.as_view(), name='npc-detail'),

    # Potwory
    path('api/monsters/', views.MonsterList.as_view(), name='monster-list'),
    path('api/monsters/<int:pk>/', views.MonsterDetail.as_view(), name='monster-detail'),

    # Przedmioty
    path('api/items/', views.ItemList.as_view(), name='item-list'),
    path('api/items/<int:pk>/', views.ItemDetail.as_view(), name='item-detail'),

    # Misje
    path('api/quests/', views.QuestList.as_view(), name='quest-list'),
    path('api/quests/<int:pk>/', views.QuestDetail.as_view(), name='quest-detail'),

    # Wydarzenia
    path('api/events/', views.EventList.as_view(), name='event-list'),
    path('api/events/<int:pk>/', views.EventDetail.as_view(), name='event-detail'),
]
