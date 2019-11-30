from django.utils import timezone

from client.models import Client, Dependant
from subscription.models import Subscription


def get_subscription_rate(clt):
    divisor = {
        Client.WEEKLY: 52,
        Client.MONTHLY: 12,
        Client.QUARTERLY: 4,
        Client.ANNUALLY: 1,
    }
    divide_by = divisor[clt.payment_option]
    dependant_amount = 0
    for dependant in Dependant.objects.filter(primary=clt):
        if dependant.relationship == Dependant.SPOUSE:
            dependant_amount += clt.plan.spouse_dependant_rate
        elif dependant.relationship in [Dependant.DAUGHTER, Dependant.SON]:
            dependant_amount += clt.plan.minor_dependant_rate
        else:
            dependant_amount += clt.plan.other_dependant_rate
    return (clt.plan.client_rate + dependant_amount) / divide_by


def get_last_subscription(sub):
    next_subscription = sub.next_subscription
    if not next_subscription:
        return sub
    return get_last_subscription(next_subscription)


def get_active_subscription(cl):
    try:
        active_sub = Subscription.objects.get(client=cl, active=True)
    except Subscription.DoesNotExist:
        return None
    else:
        return active_sub


def get_next_subscription_date(cl):
    try:
        active_sub = Subscription.objects.get(client=cl, active=True)
    except Subscription.DoesNotExist:
        return timezone.now().date()
    else:
        return active_sub.expiry_date + timezone.timedelta(1)


def create_subscription(cl, amount):
    # import pdb;pdb.set_trace()
    active_sub = get_active_subscription(cl)
    if not active_sub:
        next_sub_date = timezone.now().date()
        last_sub = None
        is_active = True
    else:
        last_sub = get_last_subscription(active_sub)
        next_sub_date = last_sub.expiry_date + timezone.timedelta(1)
        is_active = False

    _sub = Subscription.objects.create(
        client=cl,
        start_date=next_sub_date,
        expiry_date=timezone.now().date(),
        plan=cl.plan,
        amount=amount,
        active=is_active,
    )
    # if last_sub:
    #    last_sub.next_subscription = _sub
    #    last_sub.save()
    return _sub
