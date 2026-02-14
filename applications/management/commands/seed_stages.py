from django.core.management.base import BaseCommand
from applications.models import Stage


class Command(BaseCommand):
    help = "Seed default Kanban stages"

    def handle(self, *args, **options):
        stages = [
            ("Saved", 1),
            ("Applied", 2),
            ("Interview", 3),
            ("Offer", 4),
            ("Rejected", 5),
        ]
        for name, order in stages:
            Stage.objects.get_or_create(name=name, defaults={"order": order})

        self.stdout.write(self.style.SUCCESS("✅ Default stages seeded"))
