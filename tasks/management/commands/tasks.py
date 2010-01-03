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
        
        task_slug = None
        if len(args) > 1:
            task_slug = args[1]
            print "Touching users only for task %s" % task_slug
        
        for user in users:
            try:
                user_touch.send(self, user=user, task_slug=task_slug)
                print "Touched user %s" % user
            except TaskUser.AlreadyAssigned:
                print "Already assigned to %s" % user
        
        