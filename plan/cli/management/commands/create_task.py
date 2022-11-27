from django.core.management.base import BaseCommand

from to_do.factories import TaskFactory


class Command(BaseCommand):
    help = """Generate 10 fake data for task, default are 10"""

    def add_arguments(self, parser):
        parser.add_argument(
            '--amount',
            type=int,
            help='The amount of fake data',
        )

    @staticmethod
    def _generate_task(amount):
        TaskFactory.create_batch(amount)

    def handle(self, *args, **options):
        options['amount'] = 10 if options['amount'] is None else options['amount']
        amount = options.get('amount')
        self._generate_task(amount)

        print('Task Created Successfully')

