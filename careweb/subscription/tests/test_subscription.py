import pytest
from django.utils import timezone
from model_bakery import baker
from dateutil.relativedelta import relativedelta

from subscription import utils
from subscription.models import Subscription
from client.models import Dependant


@pytest.fixture
def plan():
    return baker.make("core.Plan")


@pytest.fixture
def client():
    return baker.make("client.Client", payment_option="A")


@pytest.mark.django_db
def test_get_next_subscription_date_no_subscription(client):
    next_sub_date = utils.get_next_subscription_date(client)
    assert next_sub_date == timezone.now().date()


@pytest.mark.django_db
def test_get_next_subscription_date_active(client):
    today = timezone.now().date()
    tomorrow = today + timezone.timedelta(1)
    baker.make(
        "subscription.Subscription", client=client, active=True, expiry_date=today
    )
    next_sub_date = utils.get_next_subscription_date(client)
    assert next_sub_date == tomorrow


@pytest.mark.django_db
def test_get_next_subscription_date_inactive(client):
    today = timezone.now().date()
    # tomorrow = today + timezone.timedelta(1)
    baker.make(
        "subscription.Subscription", client=client, active=False, expiry_date=today
    )
    next_sub_date = utils.get_next_subscription_date(client)
    assert next_sub_date == today


@pytest.mark.django_db
def test_create_first_subscription(plan):
    """Test the start date for first subscription"""
    baker.make("core.PlanRate", plan=plan, payment_cycle="A", rate=500, extra_rate=400)
    client = baker.make("client.Client", plan=plan, payment_option="A")
    sub = utils.create_subscription(client, 1000)
    assert sub.start_date == timezone.now().date()
    assert sub.plan == plan
    assert sub.active is True
    assert 1 == Subscription.objects.count()


@pytest.mark.django_db
def test_create_new_subscription_active(plan):
    """Test new subscription is active when there is no active subscription
    but there are inactive ones"""
    baker.make("core.PlanRate", plan=plan, payment_cycle="A", rate=500, extra_rate=400)
    client = baker.make("client.Client", plan=plan, payment_option="A")
    for i in range(3):
        baker.make("subscription.Subscription", plan=plan, client=client, active=False)
    sub = utils.create_subscription(client, 1000)
    assert sub.active is True


@pytest.mark.django_db
def test_create_subscription_active(plan):
    """Test creating new subscription when there is an active one.
    new subscription should be inactive, date should start day after
    expiry of current one and current subscription should point to this
    as next subscription. also test that new subscription will be inactive"""
    baker.make("core.PlanRate", plan=plan, payment_cycle="A", rate=500, extra_rate=400)
    today = timezone.now().date()
    tomorrow = today + timezone.timedelta(1)
    next_tom = today + timezone.timedelta(2)
    client = baker.make("client.Client", plan=plan, payment_option="A")
    baker.make(
        "subscription.Subscription",
        client=client,
        active=True,
        expiry_date=tomorrow,
        next_subscription=None,
    )
    # import pdb;pdb.set_trace()
    sub = utils.create_subscription(client, 1000)
    assert sub.start_date == next_tom
    assert sub.active is False


@pytest.mark.django_db
def test_wrong_amount_less():
    """Test that the wrong amount will not create a subscription"""
    plan = baker.make("core.Plan")
    baker.make("core.PlanRate", plan=plan, payment_cycle="A", rate=5200, extra_rate=400)
    client = baker.make("client.Client", plan=plan, payment_option="A")
    utils.create_subscription(client, 5000)
    assert 0 == Subscription.objects.count()


@pytest.mark.django_db
def test_client_balance_default(plan):
    """Default client balance is 0"""
    client = baker.make("client.Client", plan=plan, payment_option="A")
    assert 0 == client.balance


@pytest.mark.django_db
def test_client_balance_excess_subscription():
    """Test that excess subscription will be added to wallet balance"""
    plan = baker.make("core.Plan")
    baker.make("core.PlanRate", plan=plan, payment_cycle="A", rate=5200, extra_rate=400)
    client = baker.make("client.Client", plan=plan, payment_option="A")
    utils.create_subscription(client, 6000)
    assert 1 == Subscription.objects.count()
    assert 800 == client.balance


@pytest.mark.django_db
def test_client_subscription_without_plan():
    """Test that subscription doesn't work with no plan selected"""
    client = baker.make("client.Client", plan=None)
    sub = utils.create_subscription(client, 1000)
    assert 0 == Subscription.objects.count()
    assert sub is None


@pytest.mark.django_db
def test_client_subscription_without_payment_option():
    """Test that subscription doesn't work with no payment option"""
    client = baker.make("client.Client", payment_option=None)
    sub = utils.create_subscription(client, 1000)
    assert 0 == Subscription.objects.count()
    assert sub is None


@pytest.mark.django_db
def test_client_subscription_rate_without_plan():
    """Test that subscription rate is None where no plan"""
    client = baker.make("client.Client", plan=None, payment_option="A")
    rate = utils.get_subscription_rate(client)
    assert rate is None


@pytest.mark.django_db
def test_client_subscription_rate_without_payment_option(plan):
    """Test that subscription rate is None where no payment option"""
    baker.make("core.PlanRate", plan=plan, payment_cycle="A", rate=5200, extra_rate=400)
    client = baker.make("client.Client", payment_option=None, plan=plan)
    rate = utils.get_subscription_rate(client)
    assert rate is None


## Management of subscription balance


@pytest.mark.django_db
def test_client_balance_excess_subscription_multiple():
    """Test that multiple subscriptions will be added to wallet balance"""
    plan = baker.make("core.Plan")
    baker.make("core.PlanRate", plan=plan, payment_cycle="A", rate=5200, extra_rate=400)
    client = baker.make("client.Client", plan=plan, payment_option="A")
    utils.create_subscription(client, 6000)
    utils.create_subscription(client, 6000)
    assert 2 == Subscription.objects.count()
    assert 1600 == client.balance


@pytest.mark.django_db
def test_client_balance_added_to_subscription():
    """Wallet balance is used to make up subscription cost"""
    plan = baker.make("core.Plan")
    baker.make("core.PlanRate", plan=plan, payment_cycle="A", rate=5200, extra_rate=400)
    client = baker.make("client.Client", plan=plan, payment_option="A")
    utils.create_subscription(client, 6000)
    print(client.balance)
    # should have balance of 800
    utils.create_subscription(client, 5000)
    assert 2 == Subscription.objects.count()
    assert 600 == client.balance


##  Calculation of subscription amount


@pytest.mark.django_db
def test_calculate_subscription_no_deps():
    """Test the calculation of subscription amount with no dependants"""
    plan = baker.make("core.Plan")
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=520, extra_rate=400)
    client = baker.make("client.Client", plan=plan, payment_option="M")
    rate = utils.get_subscription_rate(client)
    assert rate == 520


@pytest.mark.django_db
def test_calculate_subscription_deps_family(plan):
    """Test calculation of subscription amount for family plan with dependants
    who are part of the family"""
    plan = baker.make("core.Plan", has_extra=True, family_inclusive=True)
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=520, extra_rate=400)
    client = baker.make("client.Client", plan=plan, payment_option="M")
    baker.make("client.Dependant", relationship=Dependant.SPOUSE, primary=client)
    baker.make("client.Dependant", relationship=Dependant.SON, primary=client)
    rate = utils.get_subscription_rate(client)
    assert rate == 520


@pytest.mark.django_db
def test_calculate_subscription_deps_outside_family():
    """Test calculation of subscription amount for family plan with dependants
    who are NOT a part of the family"""
    plan = baker.make("core.Plan", has_extra=True, family_inclusive=True)
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=520, extra_rate=400)
    client = baker.make("client.Client", plan=plan, payment_option="M")
    baker.make("client.Dependant", relationship=Dependant.OTHERS, primary=client)
    rate = utils.get_subscription_rate(client)
    assert rate == 920


@pytest.mark.django_db
def test_calculate_subscription_deps_single():
    """Test calculation of subscription amount for single plan with dependants
    """
    plan = baker.make("core.Plan", has_extra=True, family_inclusive=False)
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=520, extra_rate=400)
    client = baker.make("client.Client", plan=plan, payment_option="M")
    baker.make("client.Dependant", relationship=Dependant.SON, primary=client)
    rate = utils.get_subscription_rate(client)
    assert rate == 920


@pytest.mark.django_db
def test_calculate_subscription_deps_family():
    """Test calculation of subscription amount for family plan with dependants
    """
    plan = baker.make("core.Plan", has_extra=True, family_inclusive=True)
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=520, extra_rate=400)
    client = baker.make("client.Client", plan=plan, payment_option="M")
    baker.make("client.Dependant", relationship=Dependant.SON, primary=client)
    rate = utils.get_subscription_rate(client)
    assert rate == 520


@pytest.mark.django_db
def _test_calculate_subscription_deps_not_supported(plan):
    """TODO: Test attempt to add dependants to plan that does not support
    dependants"""
    plan = baker.make("core.Plan", has_extra=False)
    client = baker.make("client.Client", plan=plan, payment_option="A")
    baker.make("client.Dependant", primary=client)
    baker.make("client.Dependant", relationship=Dependant.SON, primary=client)
    rate = utils.get_subscription_rate(client)
    assert rate == 3900


@pytest.mark.django_db
def test_monthly_subscription_calculated_correctly(plan):
    """monthly subscription calculated correctly"""
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=520)
    client = baker.make("client.Client", plan=plan, payment_option="M")
    rate = utils.get_subscription_rate(client)
    assert rate == 520


@pytest.mark.django_db
def test_weekly_subscription_calculated_correctly(plan):
    """weekly subscription calculated correctly"""
    baker.make("core.PlanRate", plan=plan, payment_cycle="W", rate=520)
    client = baker.make("client.Client", plan=plan, payment_option="W")
    rate = utils.get_subscription_rate(client)
    assert rate == 520


@pytest.mark.django_db
def test_annual_subscription_calculated_correctly(plan):
    """annual subscription calculated correctly"""
    baker.make("core.PlanRate", plan=plan, payment_cycle="A", rate=5200)
    client = baker.make("client.Client", plan=plan, payment_option="A")
    rate = utils.get_subscription_rate(client)
    assert rate == 5200


@pytest.mark.django_db
def test_daily_subscription_calculated_correctly(plan):
    """daily subscription calculated correctly"""
    baker.make("core.PlanRate", plan=plan, payment_cycle="D", rate=130)
    client = baker.make("client.Client", plan=plan, payment_option="D")
    rate = utils.get_subscription_rate(client)
    assert rate == 130


##  End dates for subscription


@pytest.mark.django_db
def test_weekly_subscription_expiry(plan):
    """Test expiry date for weekly subscription"""
    # plan = baker.make("core.Plan", client_rate=5200)
    baker.make("core.PlanRate", plan=plan, payment_cycle="W", rate=1000)
    client = baker.make("client.Client", plan=plan, payment_option="W")
    sub = utils.create_subscription(client, 1000)
    aweek = timezone.now().date() + timezone.timedelta(6)
    assert aweek == sub.expiry_date


@pytest.mark.django_db
def test_monthly_subscription_expiry(plan):
    """Test expiry date for weekly subscription"""
    # plan = baker.make("core.Plan", client_rate=5200)
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=1000)
    client = baker.make("client.Client", plan=plan, payment_option="M")
    sub = utils.create_subscription(client, 1000)
    amonth = timezone.now().date() + relativedelta(months=1, days=-1)
    assert amonth == sub.expiry_date


@pytest.mark.django_db
def test_multiple_subscription_start_expiry():
    """Test that multiple subscriptions have correct expiry"""
    plan = baker.make("core.Plan")
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=1000)
    client = baker.make("client.Client", plan=plan, payment_option="M")
    sub1 = utils.create_subscription(client, 1000)
    sub2 = utils.create_subscription(client, 1000)
    sub3 = utils.create_subscription(client, 1000)

    today = timezone.now().date()
    amonth = timezone.now().date() + relativedelta(months=1, days=-1)
    two_start = amonth + timezone.timedelta(1)
    two_end = timezone.now().date() + relativedelta(months=2, days=-1)
    three_start = two_end + timezone.timedelta(1)
    three_end = timezone.now().date() + relativedelta(months=3, days=-1)
    assert today == sub1.start_date
    assert amonth == sub1.expiry_date
    assert sub1.active is True

    assert two_start == sub2.start_date
    assert two_end == sub2.expiry_date

    assert three_start == sub3.start_date
    assert three_end == sub3.expiry_date
