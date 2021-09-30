from django_cron import CronJobBase, Schedule
from .models import OpenExchange
import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def open_exchange_rates_cron_job():
    print(" ------ Start cron ")
    url = 'https://openexchangerates.org/api/latest.json'
    data = requests.get(url, params={"app_id": "52b0e42121c84181815a8d97e6eef9b8"}).json()
    base = "TRY"
    data['base'] = base
    for currency in data['rates']:
        if currency == base:
            data['rates']['USD'] = 1 / data['rates'][base]
            continue
        data['rates'][currency] = data['rates'][currency] / data['rates'][base]
    timestamp = datetime.fromtimestamp(data['timestamp'])
    if not OpenExchange.objects.filter(base=base).exists():
        OpenExchange(base=base, timestamp=timestamp, rates=data['rates']).save()
    else:
        OpenExchange.objects.filter(base=base).update(timestamp=timestamp, rates=data['rates'],
                                                          updated_at=datetime.now())
