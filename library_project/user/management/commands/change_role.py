from django.core.management.base import BaseCommand
from user.models import CustomUser

class Command(BaseCommand):
    help = 'Change user role'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user')
        parser.add_argument('role', type=str, help='New role (admin/client)')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        role = kwargs['role']
        
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR('User does not exist'))
            return

        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS('Role changed to admin'))
        elif role == 'client':
            user.is_staff = False
            user.is_superuser = False
            user.save()
            self.stdout.write(self.style.SUCCESS('Role changed to client'))
        else:
            self.stdout.write(self.style.ERROR('Invalid role. Use "admin" or "client"'))