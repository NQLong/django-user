from django.core.management.base import BaseCommand
import time
from random import randint
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.core import serializers
class Command(BaseCommand):
    
    def handle(self, *args, **options):
        from User.models import MyUser
        # for i in range(1,6):

        #     instance = MyUser.objects.create_user(
        #         username = f"{i}",
        #         email = f"{i}@{i}.com",
        #         full_name = f"{i}",
        #         password = f"{i}",
        #     )
        for i in MyUser.objects.all():
            # i.company_name = "Horus"
            # i.save()
            i.user_profile.company_name = i.company_name
            i.user_profile.save()
        # from Auth.models import MyUser

        # a = MyUser.objects.all().first()
        # print(a.__getattribute__("user_profile"))