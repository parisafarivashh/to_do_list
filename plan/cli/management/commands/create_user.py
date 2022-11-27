from django.core.management.base import BaseCommand

from user.factories import UserFactory


class Command(BaseCommand):
    help = """Generate 10 fake data for user, default are 10"""

    def add_arguments(self, parser):
        parser.add_argument(
            '--amount',
            type=int,
            help='The amount of fake data',
        )

    @staticmethod
    def _generate_user(amount):
        UserFactory.create_batch(amount)

    def handle(self, *args, **options):
        options['amount'] = 10 if options['amount'] is None else options['amount']
        amount = options.get('amount')
        self._generate_user(amount)

        print('User Created Successfully')



