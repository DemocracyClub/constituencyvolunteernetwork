import os

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import transaction

from signup import models



class Command(BaseCommand):
    def handle(self, *args, **options):
        possible_args = ('unconfirmed-list',
                         'unconfirmed-poke')
        if not args or (args and args[0] not in possible_args):
            raise CommandError("USAGE: ./manage.py %s %s" % \
                    (os.path.basename(__file__).split('.')[0],
                     " ".join(possible_args)))

        transaction.enter_transaction_management()
        transaction.managed(True)
        if args[0] == 'unconfirmed-list':
            for user in models.CustomUser.objects\
                    .filter(is_active=False):
                print user, user.date_joined
        elif args[0] == 'unconfirmed-poke':
            for user in models.CustomUser.objects\
                    .filter(is_active=False):
                if user.email.startswith('asd'):
                    print user.registrationprofile_set.get()
                    profile = user.registrationprofile_set.get()
                    print profile.resend_activation_email()
                else:
                    continue
