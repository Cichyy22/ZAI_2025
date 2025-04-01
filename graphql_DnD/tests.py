from django.test import TestCase
from graphene.test import Client
from django.contrib.auth.models import User
from graphql_DnD.schema import schema
from DnDApp.models import Character, Campaign, NPC, Monster, Item, Quest, Event


class GraphQLTestCase(TestCase):
    def setUp(self):
        """Tworzy przykładowe dane do testów"""
        self.client = Client(schema)

        self.user = User.objects.create(username="testuser")
        self.user2 = User.objects.create(username="testuser2")
        self.campaign = Campaign.objects.create(
            name="Test Campaign",
            description="Example",
            dungeon_master=self.user2
        )
        self.character = Character.objects.create(
            name="Hero", race="Elf", character_class="Warrior",
            level=5, gold=100, user=self.user2, campaign=self.campaign
        )
        self.npc = NPC.objects.create(name="Gandalf", role="Wizard", campaign=self.campaign)
        self.monster = Monster.objects.create(name="Orc", health_points=10, attack_power=3, campaign=self.campaign)
        self.item = Item.objects.create(name="Sword", description="Sharp blade", value=50)
        self.quest = Quest.objects.create(title="Find the Ring", description="A mysterious ring", campaign=self.campaign, completed=False)
        self.event = Event.objects.create(title="Battle of Helm's Deep", description="Epic battle",
                                          campaign=self.campaign, date="2018-11-20T15:58:44.767594-06:00")


    def test_get_all_characters(self):
        query = """
        query {
            allCharacters {
                name
                race
                characterClass
                level
                gold
            }
        }
        """
        response = self.client.execute(query)
        self.assertEqual(response["data"]["allCharacters"][0]["name"], "Hero")

    def test_get_single_character(self):
        query = f"""
        query {{
            character(id: {self.character.id}) {{
                name
                race
                characterClass
                level
                gold
            }}
        }}
        """
        response = self.client.execute(query)
        self.assertEqual(response["data"]["character"]["name"], "Hero")

    def test_get_all_campaigns(self):
        query = """
        query {
            allCampaigns {
                name
                description
            }
        }
        """
        response = self.client.execute(query)
        self.assertEqual(response["data"]["allCampaigns"][0]["name"], "Test Campaign")

    def test_get_single_campaign(self):
        query = f"""
        query {{
            campaign(id: {self.campaign.id}) {{
                name
                description
            }}
        }}
        """
        response = self.client.execute(query)
        self.assertEqual(response["data"]["campaign"]["name"], "Test Campaign")



    def test_create_character(self):
        mutation = f"""
        mutation {{
            createCharacter(
                name: "New Hero",
                race: "Human",
                characterClass: "Mage",
                level: 10,
                userId: {self.user.id},
                campaignId: {self.campaign.id}
            ) {{
                character {{
                    name
                    race
                    characterClass
                    level
                }}
            }}
        }}
        """
        response = self.client.execute(mutation)
        print(response)
        self.assertEqual(response["data"]["createCharacter"]["character"]["name"], "New Hero")

    def test_update_character(self):
        mutation = f"""
        mutation {{
            updateCharacter(
                id: {self.character.id},
                name: "Updated Hero"
            ) {{
                character {{
                    name
                }}
            }}
        }}
        """
        response = self.client.execute(mutation)
        self.assertEqual(response["data"]["updateCharacter"]["character"]["name"], "Updated Hero")

    def test_delete_character(self):
        mutation = f"""
        mutation {{
            deleteCharacter(id: {self.character.id}) {{
                success
            }}
        }}
        """
        response = self.client.execute(mutation)
        self.assertTrue(response["data"]["deleteCharacter"]["success"])
        self.assertEqual(Character.objects.count(), 0)


    def test_get_all_monsters(self):
        query = """
        query {
            allMonsters {
                name
                healthPoints
                attackPower
            }
        }
        """
        response = self.client.execute(query)
        self.assertEqual(response["data"]["allMonsters"][0]["name"], "Orc")

    def test_get_single_monster(self):
        query = f"""
        query {{
            monster(id: {self.monster.id}) {{
                name
                healthPoints
                attackPower
            }}
        }}
        """
        response = self.client.execute(query)
        self.assertEqual(response["data"]["monster"]["name"], "Orc")

    def test_get_all_items(self):
        query = """
        query {
            allItems {
                name
                description
                value
            }
        }
        """
        response = self.client.execute(query)
        self.assertEqual(response["data"]["allItems"][0]["name"], "Sword")

    def test_get_all_quests(self):
        query = """
        query {
            allQuests {
                title
                description
                completed
            }
        }
        """
        response = self.client.execute(query)
        self.assertEqual(response["data"]["allQuests"][0]["title"], "Find the Ring")

    def test_get_all_events(self):
        query = """
        query {
            allEvents {
                title
                description
                date
            }
        }
        """
        response = self.client.execute(query)
        self.assertEqual(response["data"]["allEvents"][0]["title"], "Battle of Helm's Deep")


    def test_update_monster(self):
        mutation = f"""
        mutation {{
            updateMonster(
                id: {self.monster.id},
                name: "Updated Orc"
            ) {{
                monster {{
                    name
                }}
            }}
        }}
        """
        response = self.client.execute(mutation)
        self.assertEqual(response["data"]["updateMonster"]["monster"]["name"], "Updated Orc")

    def test_update_item(self):
        mutation = f"""
        mutation {{
            updateItem(
                id: {self.item.id},
                name: "Magic Sword"
            ) {{
                item {{
                    name
                }}
            }}
        }}
        """
        response = self.client.execute(mutation)
        self.assertEqual(response["data"]["updateItem"]["item"]["name"], "Magic Sword")

    def test_update_quest(self):
        mutation = f"""
        mutation {{
            updateQuest(
                id: {self.quest.id},
                completed: true
            ) {{
                quest {{
                    completed
                }}
            }}
        }}
        """
        response = self.client.execute(mutation)
        self.assertTrue(response["data"]["updateQuest"]["quest"]["completed"])

    def test_update_event(self):
        mutation = f"""
        mutation {{
            updateEvent(
                id: {self.event.id},
                title: "Updated Battle"
            ) {{
                event {{
                    title
                }}
            }}
        }}
        """
        response = self.client.execute(mutation)
        self.assertEqual(response["data"]["updateEvent"]["event"]["title"], "Updated Battle")

