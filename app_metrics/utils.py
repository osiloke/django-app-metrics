import datetime 
from django.conf import settings 
from django.utils.importlib import import_module 

from app_metrics.models import Metric, MetricSet, MetricItem 

def create_metric_set(name=None, metrics=None, email_recipients=None, no_email=False, send_daily=True, send_weekly=False, send_monthly=False): 
    """ Create a metric set """ 
    try: 
        metric_set = MetricSet(
                            name=name, 
                            no_email=no_email, 
                            send_daily=send_daily,
                            send_weekly=send_weekly,
                            send_monthly=send_monthly)
        metric_set.save()

        for m in metrics: 
            metric_set.metrics.add(m)

        for e in email_recipients: 
            metric_set.email_recipients.add(e)

    except: 
        return False 

    return metric_set 

def create_metric(name=None, slug=None): 
    """ Create a new type of metric to track """ 
    try: 
        new_metric = Metric(name=name, slug=slug)
        new_metric.save()

    except: 
        return False 

    return new_metric 

class InvalidMetricsBackend(Exception): pass 
class MetricError(Exception): pass 

def metric(slug=None, num=1):
    """ Increment a metric """ 
   
    backend_string = getattr(settings, 'APP_METRICS_BACKEND', 'app_metrics.backends.db')

    # Attempt to import the backend 
    try: 
        backend = import_module(backend_string)
    except: 
        raise InvalidMetricsBackend("Could not load '%s' as a backend" % backend_string )

    #try: 
    backend.metric(slug, num)
    #except: 
        #raise MetricError('Unable to capture metric')

def week_for_date(date=None): 
    return date - datetime.timedelta(days=date.weekday())

def month_for_date(month=None): 
    return month - datetime.timedelta(days=month.day-1)

def year_for_date(year=None): 
    return datetime.date(year.year, 01, 01)

