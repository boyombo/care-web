from datetime import datetime, timedelta

from django import template
from django.db.models import Sum

from client.models import Client
from core.models import Plan
from payment.models import Payment
from ranger.models import Ranger

register = template.Library()


@register.inclusion_tag('core/dashboard__header_stat.html', takes_context=True)
def header_stat(context):
    clients = Client.objects.filter(verified=True).count()
    rangers = Ranger.objects.count()
    payment = Payment.objects.aggregate(Sum('amount'))['amount__sum']
    now = datetime.now()
    current = now.replace(day=1)
    month_payment = Payment.objects.filter(payment_date__gte=current.date()).aggregate(Sum('amount'))['amount__sum']
    payment = "{0:,.2f}".format(payment) if payment else "0.00"
    month_payment = "{0:,.2f}".format(month_payment) if month_payment else "0.00"
    return {
        "clients": clients,
        "rangers": rangers,
        "payment": payment,
        "month_payment": month_payment
    }


@register.inclusion_tag('core/dashboard__charts.html', takes_context=True)
def dashboard_charts(context):
    today = datetime.now().date()
    last_7_days = today + timedelta(days=-6)
    weekly_subscribers = []
    for i in range((today - last_7_days).days + 1):
        date = last_7_days + timedelta(i)
        weekly_subscribers.append({
            "date": date.strftime("%B %d"),
            "count": Client.objects.filter(registration_date__date=date).count()
        })
    plans = []
    for plan in Plan.objects.all():
        plans.append({
            "plan": plan.name,
            "code": plan.code,
            "count": Client.objects.filter(plan=plan).count()
        })
    return {
        "weekly_subscribers": weekly_subscribers,
        "plans": plans,
        "weekly_length": len(weekly_subscribers),
        "plans_length": len(plans)
    }
