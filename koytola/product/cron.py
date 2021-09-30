from django_cron import CronJobBase, Schedule
from .models import OpenExchange
import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 60

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
        url = 'https://openexchangerates.org/api/latest.json'
        data = requests.get(url, params={"app_id": "7b6b711a030d4e98a43a357ed5cfbee5"}).json()
        base = "TRY"
        data['base'] = base
        rates = {}
        for currency in data['rates']:
            if currency == base:
                rates['USD'] = data['rates'][base]
                continue
            elif currency == 'USD':
                continue
            elif currency in ['JPY', 'USD', 'EUR', 'GBP', 'BTC', 'KRW', 'CNY', 'SGD', 'AUD', 'CAD', 'CHF', 'MXN', 'BRL',
                              'RUB']:
                rates[currency] = data['rates'][base] / data['rates'][currency]

        timestamp = datetime.fromtimestamp(data['timestamp'])
        if not OpenExchange.objects.filter(base=base).exists():
            OpenExchange(base=base, timestamp=timestamp, rates=rates).save()
            logging.info("Open Exchange create")
        else:
            OpenExchange.objects.filter(base=base).update(timestamp=timestamp, rates=rates, updated_at=datetime.now())
            logging.info("Open Exchange update")

