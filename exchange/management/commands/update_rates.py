# coding: utf-8
from optparse import make_option
import datetime
from django.core.management.base import BaseCommand, CommandError
from exchange.conversion import update_rates_from_date


class Command(BaseCommand):
    help = 'This command triggers exchane update process (for today or from date)'
    option_list = BaseCommand.option_list + (
        make_option('--from', '-f', dest='from', help='date from (example: 2014-05-01)'),
    )

    def handle(self, *args, **options):
        """Handle command"""
        try:
            from_date = None
            if options['from']:
                from_date = datetime.datetime.strptime(options['from'], '%Y-%m-%d').date()
            update_rates_from_date(date=from_date)
            print 'EXCHANGE RATE UPDATE FINISHED!'
        except Exception, e:
            raise CommandError(e)
