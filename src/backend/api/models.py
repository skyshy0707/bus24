import random

from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.db import models

from api import validators

# Create your models here.

COLORS = (
    ("white", "white"),
    ("purple", "purple"),
    ("blue", "blue"),
    ("green", "green"),
    ("red", "red"),
    ("orange", "orange"),
    ("yellow", "yellow"),
    ("pink", "pink")
)

CAPACITY_CATHEGORY = (
    ("very_big", "very_big"),
    ("big", "big"),
    ("medium", "medium"),
    ("small", "small"),
    ("very_small", "very_small")
)

capacity_cathegory_ = dict(CAPACITY_CATHEGORY)

def define_min_capacity(capacity_class: str) -> int:
    
    if capacity_class == capacity_cathegory_["very_small"]:
        return 10
    elif capacity_class ==  capacity_cathegory_["small"]:
        return 60
    elif capacity_class == capacity_cathegory_["medium"]:
        return 80
    elif capacity_class == capacity_cathegory_["big"]:
        return 110
    elif capacity_class == capacity_cathegory_["very_big"]:
        return 130
    
def assign_route_no():

    return str(random.randint(1, 1000))

class Bus(models.Model):

    model = models.CharField(verbose_name="Наименование модели и марки", max_length=256, unique=True)
    capacity = models.PositiveIntegerField(verbose_name="Номинальная вместимость", validators=[validators.capacity])

    @property
    def capacity_class(self):
        capacity = self.capacity

        if capacity <= 15 and capacity > 10:
            return capacity_cathegory_["very_small"] 
        elif capacity <= 60: 
            return capacity_cathegory_["small"] 
        elif capacity <= 80:
            return capacity_cathegory_["medium"] 
        elif capacity <= 110:
            return capacity_cathegory_["big"]
        elif capacity > 110:
            return capacity_cathegory_["very_big"]

class User(AbstractUser):

    USERNAME_FIELD = "username"
    username = models.EmailField(verbose_name="email", max_length=256, unique=True)

    class Meta:
        app_label = "api"

class ATP(models.Model):

    name = models.CharField(verbose_name="Название компании", max_length=40, unique=True)
    user = models.OneToOneField(verbose_name="Пользователь", to=User, on_delete=models.CASCADE)

    def chat_url(self):
        return f"chat/{self.id}"

class Lead(models.Model):

    atp = models.ForeignKey(verbose_name="Транспортная компания", to=ATP, on_delete=models.CASCADE)
    route_wiki_url = models.URLField(verbose_name="Урл-адрес маршрута", unique=True, validators=[validators.route_wiki_url])
    route_no = models.CharField(verbose_name="Номер маршрута", unique=True, default=assign_route_no)
    capacity_class = models.CharField(verbose_name="Класс вместимости", max_length=14, choices=CAPACITY_CATHEGORY)
    units_per_route = models.PositiveIntegerField(verbose_name="Количество транспорта на маршруте")
    date = models.DateTimeField(verbose_name="Дата заявки", auto_now=True)

class Unit(models.Model):

    bus = models.ForeignKey(verbose_name="Наименование подвижной единицы", to=Bus, on_delete=models.DO_NOTHING)
    atp = models.ForeignKey(verbose_name="Транспортная компания", to=ATP, on_delete=models.CASCADE)
    lead = models.ForeignKey(verbose_name="Заявка", to=Lead, blank=True, null=True, on_delete=models.SET_NULL)
    bort = models.PositiveIntegerField(verbose_name="Бортовой номер", unique=True)
    color = models.CharField(verbose_name="Цвет", max_length=16, choices=COLORS)

class Message(models.Model):

    atp = models.ForeignKey(verbose_name="От кого", to=ATP, on_delete=models.DO_NOTHING)
    to = models.ManyToManyField(verbose_name="Кому", related_name="recepients", to=ATP)
    lead = models.ForeignKey(verbose_name="Лиды", to=Lead, on_delete=models.DO_NOTHING)
    text = models.TextField(verbose_name="Текст", blank=True, null=True)
    date = models.DateTimeField(verbose_name="Создано", auto_now=True)

    def get_lead_url(self):
        return f"lead/{self.lead_id}"

    def get_atp_name(self):
        return self.atp.name
    
admin.site.register((
    ATP,
    Bus,
    Lead
))