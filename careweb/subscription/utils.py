from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import Max

from core.models import PlanRate
from client.models import Client, Dependant
from subscription.models import Subscription


def _get_expiry_date(clt, start_date):
    if clt.payment_option == Client.DAILY:
        return start_date
    if clt.payment_option == Client.WEEKLY:
        return start_date + relativedelta(weeks=1, days=-1)
    elif clt.payment_option == Client.MONTHLY:
        return start_date + relativedelta(months=1, days=-1)
    # elif clt.payment_option == Client.QUARTERLY:
    #    return start_date + relativedelta(months=3, days=-1)
    else:
        return start_date + relativedelta(years=1, days=-1)


def get_subscription_rate(clt):
    if not clt.payment_option or not clt.plan:
        return
    plan = clt.plan
    try:
        plan_rate = PlanRate.objects.get(
            plan=clt.plan, payment_cycle=clt.payment_option
        )
    except PlanRate.DoesNotExist:
        return None
    client_rate = plan_rate.rate
    cutoff_age = 18  # cutoff age for dependants
    cutoff_date = timezone.now().date() - relativedelta(years=cutoff_age)
    # import pdb;pdb.set_trace()

    # dependants
    # spouse = Dependant.objects.filter(primary=clt, relationship=Dependant.SPOUSE).count()
    # sons = Dependant.objects.filter(primary=clt, relationship=Dependant.SON, dob__lte=cutoff_date)
    # daughters = Dependant.objects.filter(primary=clt, relationship=Dependant.SON, dob__lte=cutoff_date)
    family_dep_count = 0
    other_dep_count = 0
    for dependant in Dependant.objects.filter(primary=clt):
        if dependant.relationship == Dependant.SPOUSE:
            family_dep_count += 1
        elif dependant.relationship == Dependant.OTHERS:
            other_dep_count += 1
        elif dependant.relationship in [Dependant.SON, Dependant.DAUGHTER]:
            if dependant.dob > cutoff_date:
                family_dep_count += 1
            else:
                other_dep_count += 1
    # family_deps = (
    #    Dependant.objects.filter(primary=clt)
    #    .exclude(relationship=Dependant.OTHERS)
    #    .count()
    # )
    # other_deps = Dependant.objects.filter(
    #    primary=clt, relationship=Dependant.OTHERS
    # ).count()
    if family_dep_count > plan.size - 1:
        other_dep_count += family_dep_count + 1 - plan.size
    if plan.has_extra and plan_rate.extra_rate:
        dep_rate = plan_rate.extra_rate * other_dep_count
        # if plan.family_inclusive:
        #    dep_rate = other_dep_count * plan_rate.extra_rate
        # else:
        #    dep_rate = plan_rate.extra_rate * other_dep_count
    else:
        dep_rate = 0
    return client_rate + dep_rate

    # divisor = {
    #    Client.WEEKLY: 52,
    #    Client.MONTHLY: 12,
    #    Client.QUARTERLY: 4,
    #    Client.ANNUALLY: 1,
    # }
    # try:
    #    divide_by = divisor[clt.payment_option]
    # except KeyError:
    #    return None
    # if not clt.plan:
    #    return None
    # dependant_amount = 0
    # for dependant in Dependant.objects.filter(primary=clt):
    #    if dependant.relationship == Dependant.SPOUSE:
    #        dependant_amount += clt.plan.spouse_dependant_rate
    #    elif dependant.relationship in [Dependant.DAUGHTER, Dependant.SON]:
    #        dependant_amount += clt.plan.minor_dependant_rate
    #    else:
    #        dependant_amount += clt.plan.other_dependant_rate
    # return (clt.plan.client_rate + dependant_amount) / divide_by


def get_last_subscription(clt):
    subs = Subscription.objects.filter(client=clt).order_by("-expiry_date")
    if subs:
        return subs[0]
    # next_subscription = sub.next_subscription
    # if not next_subscription:
    #    return sub
    # return get_last_subscription(next_subscription)


def get_active_subscription(cl):
    try:
        active_sub = Subscription.objects.get(client=cl, active=True)
    except Subscription.DoesNotExist:
        return None
    else:
        return active_sub


def get_next_subscription_date(cl):
    subscriptions = Subscription.objects.filter(client=cl, active=True)
    if not subscriptions:
        return timezone.now().date()
    exp = subscriptions.aggregate(Max("expiry_date"))["expiry_date__max"]
    return exp + timezone.timedelta(1)
    # try:
    #    active_sub = Subscription.objects.get(client=cl, active=True)
    # except Subscription.DoesNotExist:
    #    return timezone.now().date()
    # else:
    #    return active_sub.expiry_date + timezone.timedelta(1)


def create_subscription(cl, amount):
    # import pdb; pdb.set_trace()
    if not cl.plan:
        return None
    rate = get_subscription_rate(cl)
    if rate > (amount + cl.balance):
        return None
    active_sub = get_active_subscription(cl)
    if not active_sub:
        next_sub_date = timezone.now().date()
        last_sub = None
        is_active = True
    else:
        last_sub = get_last_subscription(cl)
        next_sub_date = last_sub.expiry_date + timezone.timedelta(1)
        is_active = False

    # expiry date
    print("next sub date: {}".format(next_sub_date))
    expiry_date = _get_expiry_date(cl, next_sub_date)
    print("expiry: {}".format(expiry_date))

    _sub = Subscription.objects.create(
        client=cl,
        start_date=next_sub_date,
        expiry_date=expiry_date,
        plan=cl.plan,
        amount=rate,
        active=is_active,
    )
    if cl.balance + amount > rate:
        cl.balance += amount - rate
        cl.save()
    # if last_sub:
    #    last_sub.next_subscription = _sub
    #    last_sub.save()
    return _sub
