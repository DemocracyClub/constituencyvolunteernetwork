import os

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from signup.models import CustomUser
from signup.signals import user_touch

class Command(BaseCommand):
    def handle(self, *args, **options):
        """
            The 'touch' command fires the user_touch signal on every
            user on the site. This allows tasks to assign themselves
            to pre-existing users (in addition to new users, as handled
            by user_signup)
        """
        if not args or (args and args[0] not in ('touch')):
            raise CommandError("USAGE: ./manage.py %s touch" % \
                    os.path.basename(__file__).split('.')[0])
        
        users = CustomUser.objects.all()
        
        for user in users:
            user_touch.send(self, user=user)
            print "Touched user %s" % user
        
        