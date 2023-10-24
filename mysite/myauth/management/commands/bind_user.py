from django.contrib.auth.models import User,Group, Permission
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(pk=2)
        group, created = Group.objects.get_or_create(
            name='profile manager'
        )
        permissions_profile = Permission.objects.get(
            codename='view_permission'
        )
        permissions_logentry = Permission.objects.get(
            codename='view_logentry'
        )

        group.permissions.add(permissions_profile)
        user.groups.add(group)
        user.user_permissions.add(permissions_logentry)

        user.save()
        group.save()