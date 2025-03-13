from django.db import models
from django.contrib.auth.models import User


class ActiveCampaignsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='ACTIVE')


class Campaign(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('PLANNED', 'Planned')
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PLANNED')
    dungeon_master = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_campaigns')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    active_campaigns = ActiveCampaignsManager()

    class Meta:
        ordering = ['status']

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=255)
    race = models.CharField(max_length=100)
    character_class = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    gold = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='character')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='characters')

    image = models.ImageField(upload_to='characters/', blank=True, null=True)

    class Meta:
        ordering = ['campaign']

    def __str__(self):
        return f"{self.name} ({self.character_class})"

    def add_gold(self, amount):
        self.gold += amount
        self.save()


class NPC(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100, choices=[('ALLY', 'Ally'), ('ENEMY', 'Enemy'), ('NEUTRAL', 'Neutral')])
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='npcs')

    class Meta:
        ordering = ['campaign']

    def __str__(self):
        return self.name


class Monster(models.Model):
    name = models.CharField(max_length=255)
    health_points = models.IntegerField()
    attack_power = models.IntegerField()
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='monsters')

    class Meta:
        ordering = ['campaign']

    def __str__(self):
        return f"{self.name} (HP: {self.health_points})"


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    characters = models.ManyToManyField(Character, related_name='items', blank=True)
    npcs = models.ManyToManyField(NPC, related_name='items', blank=True)

    def __str__(self):
        return self.name


class Quest(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='quests')
    characters = models.ManyToManyField(Character, related_name='quests', blank=True)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['campaign']

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='events')

    class Meta:
        ordering = ['campaign']

    def __str__(self):
        return f"{self.title} ({self.date.strftime('%Y-%m-%d')})"
