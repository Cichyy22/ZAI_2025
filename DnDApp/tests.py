from django.test import TestCase
from django.contrib.auth.models import User
from .models import Campaign, Character, NPC, Monster, Item, Quest, Event
from datetime import datetime


class CampaignModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='dm', password='password')
        self.campaign = Campaign.objects.create(
            name='Epic Adventure',
            description='An epic journey awaits.',
            status='ACTIVE',
            dungeon_master=self.user
        )

    def test_campaign_creation(self):
        self.assertEqual(self.campaign.name, 'Epic Adventure')
        self.assertEqual(self.campaign.status, 'ACTIVE')
        self.assertEqual(str(self.campaign), 'Epic Adventure')


class CharacterModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='hero', password='password')
        self.dm = User.objects.create_user(username='dm', password='password')
        self.campaign = Campaign.objects.create(name='Quest', dungeon_master=self.dm)
        self.character = Character.objects.create(
            name='Arthas', race='Human', character_class='Paladin', level=5, gold=100,
            user=self.user, campaign=self.campaign
        )

    def test_character_creation(self):
        self.assertEqual(self.character.name, 'Arthas')
        self.assertEqual(self.character.level, 5)
        self.assertEqual(self.character.gold, 100)
        self.assertEqual(str(self.character), 'Arthas (Paladin)')

    def test_add_gold(self):
        self.character.add_gold(50)
        self.assertEqual(self.character.gold, 150)


class NPCModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='dm', password='password')
        self.campaign = Campaign.objects.create(name='Quest', dungeon_master=self.user)
        self.npc = NPC.objects.create(name='Gandalf', role='ALLY', campaign=self.campaign)

    def test_npc_creation(self):
        self.assertEqual(self.npc.name, 'Gandalf')
        self.assertEqual(self.npc.role, 'ALLY')
        self.assertEqual(str(self.npc), 'Gandalf')


class MonsterModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='dm', password='password')
        self.campaign = Campaign.objects.create(name='Quest', dungeon_master=self.user)
        self.monster = Monster.objects.create(name='Dragon', health_points=500, attack_power=50, campaign=self.campaign)

    def test_monster_creation(self):
        self.assertEqual(self.monster.name, 'Dragon')
        self.assertEqual(self.monster.health_points, 500)
        self.assertEqual(str(self.monster), 'Dragon (HP: 500)')


class ItemModelTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(name='Excalibur', description='Legendary sword', value=1000)

    def test_item_creation(self):
        self.assertEqual(self.item.name, 'Excalibur')
        self.assertEqual(str(self.item), 'Excalibur')


class QuestModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='dm', password='password')
        self.campaign = Campaign.objects.create(name='Quest', dungeon_master=self.user)
        self.quest = Quest.objects.create(title='Find the Grail', description='Retrieve the Holy Grail',
                                          campaign=self.campaign)

    def test_quest_creation(self):
        self.assertEqual(self.quest.title, 'Find the Grail')
        self.assertEqual(str(self.quest), 'Find the Grail')


class EventModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='dm', password='password')
        self.campaign = Campaign.objects.create(name='Quest', dungeon_master=self.user)
        self.event = Event.objects.create(title='Battle of Helms Deep', description=' A great battle', date=datetime(2023, 6, 15), campaign=self.campaign)

    def test_event_creation(self):
        self.assertEqual(self.event.title, "Battle of Helms Deep")
        self.assertEqual(str(self.event), "Battle of Helms Deep (2023-06-15)")
