from DnDApp.models import Character, Campaign, NPC, Monster, Item, Quest, Event
import graphene
from django.db import models
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"

class CampaignType(DjangoObjectType):
    class Meta:
        model = Campaign
        fields = "__all__"

class CharacterType(DjangoObjectType):
    class Meta:
        model = Character
        fields = "__all__"

class NPCType(DjangoObjectType):
    class Meta:
        model = NPC
        fields = "__all__"

class MonsterType(DjangoObjectType):
    class Meta:
        model = Monster
        fields = "__all__"

class ItemType(DjangoObjectType):
    class Meta:
        model = Item
        fields = "__all__"

class QuestType(DjangoObjectType):
    class Meta:
        model = Quest
        fields = "__all__"

class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = "__all__"



class Query(graphene.ObjectType):
    all_characters = graphene.List(CharacterType)
    character = graphene.Field(CharacterType, id=graphene.Int())

    all_campaigns = graphene.List(CampaignType)
    campaign = graphene.Field(CampaignType, id=graphene.Int())

    all_npcs = graphene.List(NPCType)
    npc = graphene.Field(NPCType, id=graphene.Int())

    all_monsters = graphene.List(MonsterType)
    monster = graphene.Field(MonsterType, id=graphene.Int())

    all_items = graphene.List(ItemType)
    item = graphene.Field(ItemType, id=graphene.Int())

    all_quests = graphene.List(QuestType)
    quest = graphene.Field(QuestType, id=graphene.Int())

    all_events = graphene.List(EventType)
    event = graphene.Field(EventType, id=graphene.Int())

    def resolve_all_characters(self, info):
        return Character.objects.all()

    def resolve_character(self, info, id):
        return Character.objects.filter(id=id).first()

    def resolve_all_campaigns(self, info):
        return Campaign.objects.all()

    def resolve_campaign(self, info, id):
        return Campaign.objects.filter(id=id).first()

    def resolve_all_npcs(self, info):
        return NPC.objects.all()

    def resolve_npc(self, info, id):
        return NPC.objects.filter(id=id).first()

    def resolve_all_monsters(self, info):
        return Monster.objects.all()

    def resolve_monster(self, info, id):
        return Monster.objects.filter(id=id).first()

    def resolve_all_items(self, info):
        return Item.objects.all()

    def resolve_item(self, info, id):
        return Item.objects.filter(id=id).first()

    def resolve_all_quests(self, info):
        return Quest.objects.all()

    def resolve_quest(self, info, id):
        return Quest.objects.filter(id=id).first()

    def resolve_all_events(self, info):
        return Event.objects.all()

    def resolve_event(self, info, id):
        return Event.objects.filter(id=id).first()



class CreateCharacter(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        race = graphene.String(required=True)
        character_class = graphene.String(required=True)
        level = graphene.Int(required=True)
        gold = graphene.Float()
        user_id = graphene.Int(required=True)
        campaign_id = graphene.Int(required=True)

    character = graphene.Field(CharacterType)

    def mutate(self, info, name, race, character_class, level, user_id, campaign_id, gold=0):
        user = User.objects.get(id=user_id)
        campaign = Campaign.objects.get(id=campaign_id)
        character = Character.objects.create(
            name=name, race=race, character_class=character_class, level=level, gold=gold,
            user=user, campaign=campaign
        )
        if gold != 0:
            character.gold = gold
        return CreateCharacter(character=character)


class UpdateCharacter(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        race = graphene.String()
        character_class = graphene.String()
        level = graphene.Int()
        gold = graphene.Float()

    character = graphene.Field(CharacterType)

    def mutate(self, info, id, name=None, race=None, character_class=None, level=None, gold=None):
        character = Character.objects.filter(id=id).first()
        if not character:
            return None
        if name:
            character.name = name
        if race:
            character.race = race
        if character_class:
            character.character_class = character_class
        if level:
            character.level = level
        if gold is not None:
            character.gold = gold
        character.save()
        return UpdateCharacter(character=character)


class DeleteCharacter(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        character = Character.objects.filter(id=id).first()
        if not character:
            return DeleteCharacter(success=False)
        character.delete()
        return DeleteCharacter(success=True)


class CreateCampaign(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        status = graphene.String(required=True)
        dungeon_master_id = graphene.Int(required=True)

    campaign = graphene.Field(CampaignType)

    def mutate(self, info, name, description, status, dungeon_master_id):
        dungeon_master = User.objects.get(id=dungeon_master_id)
        campaign = Campaign.objects.create(
            name=name, description=description, status=status, dungeon_master=dungeon_master
        )
        return CreateCampaign(campaign=campaign)


class DeleteCampaign(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        campaign = Campaign.objects.filter(id=id).first()
        if not campaign:
            return DeleteCampaign(success=False)
        campaign.delete()
        return DeleteCampaign(success=True)

class UpdateCampaign(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()
        status = graphene.String()

    campaign = graphene.Field(CampaignType)

    def mutate(self, info, id, name=None, description=None, status=None):
        campaign = Campaign.objects.filter(id=id).first()
        if not campaign:
            return None
        if name:
            campaign.name = name
        if description:
            campaign.description = description
        if status:
            campaign.status = status
        campaign.save()
        return UpdateCampaign(campaign=campaign)


class CreateNPC(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        role = graphene.String(required=True)
        campaign_id = graphene.Int(required=True)

    npc = graphene.Field(NPCType)

    def mutate(self, info, name, role, campaign_id):
        campaign = Campaign.objects.get(id=campaign_id)
        npc = NPC.objects.create(name=name, role=role, campaign=campaign)
        return CreateNPC(npc=npc)


class DeleteNPC(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()


    def mutate(self, info, id):
        npc = NPC.objects.filter(id=id).first()
        if not npc:
            return DeleteNPC(success=False)
        npc.delete()
        return DeleteNPC(success=True)


class UpdateNPC(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        role = graphene.String()

    npc = graphene.Field(NPCType)

    def mutate(self, info, id, name=None, role=None):
        npc = NPC.objects.filter(id=id).first()
        if not npc:
            return None
        if name:
            npc.name = name
        if role:
            npc.role = role
        npc.save()
        return UpdateNPC(npc=npc)

class CreateMonster(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        health_points = graphene.Int(required=True)
        attack_power = graphene.Int(required=True)
        campaign_id = graphene.Int(required=True)

    monster = graphene.Field(MonsterType)

    def mutate(self, info, name, health_points, attack_power, campaign_id):
        campaign = Campaign.objects.get(id=campaign_id)
        monster = Monster.objects.create(
            name=name, health_points=health_points, attack_power=attack_power, campaign=campaign
        )
        return CreateMonster(monster=monster)


class UpdateMonster(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        health_points = graphene.Int()
        attack_power = graphene.Int()

    monster = graphene.Field(MonsterType)

    def mutate(self, info, id, name=None, health_points=None, attack_power=None):
        monster = Monster.objects.filter(id=id).first()
        if not monster:
            return None
        if name:
            monster.name = name
        if health_points:
            monster.health_points = health_points
        if attack_power:
            monster.attack_power = attack_power
        monster.save()
        return UpdateMonster(monster=monster)


class DeleteMonster(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        monster = Monster.objects.filter(id=id).first()
        if not monster:
            return DeleteMonster(success=False)
        monster.delete()
        return DeleteMonster(success=True)


class CreateItem(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        value = graphene.Float(required=True)

    item = graphene.Field(ItemType)

    def mutate(self, info, name, description, value):
        item = Item.objects.create(name=name, description=description, value=value)
        return CreateItem(item=item)


class UpdateItem(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()
        value = graphene.Float()

    item = graphene.Field(ItemType)

    def mutate(self, info, id, name=None, description=None, value=None):
        item = Item.objects.filter(id=id).first()
        if not item:
            return None
        if name:
            item.name = name
        if description:
            item.description = description
        if value:
            item.value = value
        item.save()
        return UpdateItem(item=item)


class DeleteItem(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        item = Item.objects.filter(id=id).first()
        if not item:
            return DeleteItem(success=False)
        item.delete()
        return DeleteItem(success=True)


class CreateQuest(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        campaign_id = graphene.Int(required=True)
        completed = graphene.Boolean()

    quest = graphene.Field(QuestType)

    def mutate(self, info, title, description, campaign_id, completed=False):
        campaign = Campaign.objects.get(id=campaign_id)
        quest = Quest.objects.create(
            title=title, description=description, campaign=campaign, completed=completed
        )
        return CreateQuest(quest=quest)


class UpdateQuest(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        completed = graphene.Boolean()

    quest = graphene.Field(QuestType)

    def mutate(self, info, id, title=None, description=None, completed=None):
        quest = Quest.objects.filter(id=id).first()
        if not quest:
            return None
        if title:
            quest.title = title
        if description:
            quest.description = description
        if completed is not None:
            quest.completed = completed
        quest.save()
        return UpdateQuest(quest=quest)


class DeleteQuest(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        quest = Quest.objects.filter(id=id).first()
        if not quest:
            return DeleteQuest(success=False)
        quest.delete()
        return DeleteQuest(success=True)


class CreateEvent(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        date = graphene.DateTime(required=True)
        campaign_id = graphene.Int(required=True)

    event = graphene.Field(EventType)

    def mutate(self, info, title, description, date, campaign_id):
        campaign = Campaign.objects.get(id=campaign_id)
        event = Event.objects.create(title=title, description=description, date=date, campaign=campaign)
        return CreateEvent(event=event)


class UpdateEvent(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        date = graphene.DateTime()

    event = graphene.Field(EventType)

    def mutate(self, info, id, title=None, description=None, date=None):
        event = Event.objects.filter(id=id).first()
        if not event:
            return None
        if title:
            event.title = title
        if description:
            event.description = description
        if date:
            event.date = date
        event.save()
        return UpdateEvent(event=event)


class DeleteEvent(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        event = Event.objects.filter(id=id).first()
        if not event:
            return DeleteEvent(success=False)
        event.delete()
        return DeleteEvent(success=True)


class Mutation(graphene.ObjectType):
    create_character = CreateCharacter.Field()
    update_character = UpdateCharacter.Field()
    delete_character = DeleteCharacter.Field()
    create_campaign = CreateCampaign.Field()
    update_campaign = UpdateCampaign.Field()
    delete_campaign = DeleteCampaign.Field()
    create_npc = CreateNPC.Field()
    update_npc = UpdateNPC.Field()
    delete_npc = DeleteNPC.Field()
    create_monster = CreateMonster.Field()
    update_monster = UpdateMonster.Field()
    delete_monster = DeleteMonster.Field()
    create_item = CreateItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()
    create_quest = CreateQuest.Field()
    update_quest = UpdateQuest.Field()
    delete_quest = DeleteQuest.Field()
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

