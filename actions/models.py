

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from actions.choices import ACTION_PRIORITY_CHOICES, ACTION_TYPE_CHOICES
from cat.models import Cat


# Create your models here.
class Action(models.Model):
    cat = models.ForeignKey('cat.Cat', on_delete=models.CASCADE, related_name='actions')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE_CHOICES)
    treatment_cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    priority = models.CharField(max_length=10, choices=ACTION_PRIORITY_CHOICES)

    FIXED_COSTS = {
        'Neuter': 50.00,
        'Chip': 20.00,
    }

    FIXED_PRIORITY = {
        'Neuter': 'Medium',
        'Chip': 'Low',
    }

    def save(self, *args, **kwargs):
        if self.action_type in ['Neuter', 'Chip']:
            self.treatment_cost = self.FIXED_COSTS[self.action_type]
            self.priority = self.FIXED_PRIORITY[self.action_type]
        super().save(*args, **kwargs)

    @receiver(post_save, sender=Cat)
    def create_actions(sender, instance, created, **kwargs):
        is_adult = instance.age is None or instance.age > 1
        if is_adult and instance.chipped is False:
            if not instance.actions.filter(action_type='Chip').exists():
                Action.objects.create(cat=instance, action_type='Chip')
        if is_adult and instance.neutered is False:
            if not instance.actions.filter(action_type='Neuter').exists():
                Action.objects.create(cat=instance, action_type='Neuter')
        if instance.health_notes:
            if not instance.actions.filter(action_type='Health issue').exists():
                Action.objects.create(cat=instance, action_type='Health issue')
