# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from shared_foundation import constants
from shared_foundation.models.me import SharedMe
from shared_foundation.utils import (
    get_random_string,
    get_unique_username_from_email
)


class Command(BaseCommand):
    help = _('Command will create an executive account in our application.')

    def add_arguments(self, parser):
        """
        Run manually in console:
        python manage.py create_executive_account "bart@overfiftyfive.com" "123password" "Bart" "Mika"
        """
        parser.add_argument('email', nargs='+', type=str)
        parser.add_argument('password', nargs='+', type=str)
        parser.add_argument('first_name', nargs='+', type=str)
        parser.add_argument('last_name', nargs='+', type=str)

    def handle(self, *args, **options):
        # Get the user inputs.
        email = options['email'][0]
        password = options['password'][0]
        first_name = options['first_name'][0]
        last_name = options['last_name'][0]

        # Defensive Code: Prevent continuing if the email already exists.
        if User.objects.filter(email=email).exists():
            raise CommandError(_('Email already exists, please pick another email.'))

        # Create the user.
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=get_unique_username_from_email(email),
            is_active=True,
            is_superuser=True,
            is_staff=True
        )

        # Generate and assign the password.
        user.set_password(password)
        user.save()

        # Generate the private access key.
        token = Token.objects.create(user=user)

        # Create our profile.
        SharedMe.objects.create(
            user=user
        )

        # Attach our user to the "Executive"
        user.groups.add(constants.EXECUTIVE_GROUP_ID)
