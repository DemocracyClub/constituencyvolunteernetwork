import os
from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from signup.models import CustomUser
from signup.signals import user_touch
from tasks.models import TaskUser

class Command(BaseCommand):
    option_list =  BaseCommand.option_list + (
        make_option('--dry-run', '-n', dest='dry_run',
                    action="store_true",
                    help="Only show what would be done"),
        make_option('--slug', '-s', dest='task_slug',
                    action="store",
                    help="Only assign named task"),
        make_option('--emailfilter', '-e', dest='emailfilter',
                    action="store",
                    help="Only assign to users with emails containing")
        )
    help = "Assign tasks to users"
                        
    def handle(self, *args, **options):
        """
            The 'touch' command fires the user_touch signal on every
            user on the site. This allows tasks to :
            assign themselves
            to pre-existing users (in addition to new users, as handled
            by user_signup)
            """
        if not args or (args and args[0] not in ('touch','email')):
            raise CommandError()
        users = CustomUser.objects.all()
        emailfilter = options.get('emailfilter', '')
        if emailfilter:
            users = users.filter(email__icontains=emailfilter)
        task_slug = options.get('task_slug', None)
        dry_run = options.get('dry_run', False)
        for user in users:
            msg = "user %s" % user
            if args[0] == "touch":
                msg += "\n  touching:"
                if not dry_run:
                    responses = user_touch.send(self, user=user,
                                                task_slug=task_slug)
                    msg += "\n  ".join([x[1] for x in responses\
                                        if x[1]])
            elif args[0] == "email":
                for task in TaskUser.objects.filter(emails_sent=0,
                                                    user=user):
                    msg += "\n  emailing about %s" % task.task.slug
                    if not dry_run:
                        task.send_email()
                    
            print msg

