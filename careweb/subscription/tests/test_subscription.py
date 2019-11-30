import pytest
from django.utils import timezone
from model_bakery import baker

from subscription import utils
from client.models import Dependant


@pytest.fixture
def plan():
    return baker.make("core.Plan")


@pytest.fixture
def client():
    return baker.make("client.Client")


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
    client = baker.make("client.Client", plan=plan)
    sub = utils.create_subscription(client, 1000)
    assert sub.start_date == timezone.now().date()
    assert sub.plan == plan
    assert sub.active is True


@pytest.mark.django_db
def test_create_new_subscription_active(plan):
    """Test new subscription is active when there is no active subscription
    but there are inactive ones"""
    client = baker.make("client.Client", plan=plan)
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
    today = timezone.now().date()
    tomorrow = today + timezone.timedelta(1)
    next_tom = today + timezone.timedelta(2)
    client = baker.make("client.Client", plan=plan)
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
def test_calculate_subscription_no_deps():
    """Test the calculation of subscription amount with no dependants"""
    plan = baker.make("core.Plan", client_rate=1200)
    client = baker.make("client.Client", plan=plan, payment_option="A")
    rate = utils.get_subscription_rate(client)
    assert rate == 1200


@pytest.mark.django_db
def test_calculate_subscription_deps():
    """Test calculation of subscription amount with dependants"""
    plan = baker.make(
        "core.Plan",
        client_rate=2400,
        spouse_dependant_rate=1000,
        minor_dependant_rate=500,
    )
    client = baker.make("client.Client", plan=plan, payment_option="A")
    baker.make("client.Dependant", relationship=Dependant.SPOUSE, primary=client)
    baker.make("client.Dependant", relationship=Dependant.SON, primary=client)
    rate = utils.get_subscription_rate(client)
    assert rate == 3900


@pytest.mark.django_db
def test_monthly_subscription_calculated_correctly():
    """monthly subscription calculated correctly"""
    plan = baker.make("core.Plan", client_rate=2400)
    client = baker.make("client.Client", plan=plan, payment_option="M")
    rate = utils.get_subscription_rate(client)
    assert rate == 200


@pytest.mark.django_db
def test_weekly_subscription_calculated_correctly():
    """weekly subscription calculated correctly"""
    plan = baker.make("core.Plan", client_rate=5200)
    client = baker.make("client.Client", plan=plan, payment_option="W")
    rate = utils.get_subscription_rate(client)
    assert rate == 100


@pytest.mark.django_db
def test_annual_subscription_calculated_correctly():
    """annual subscription calculated correctly"""
    plan = baker.make("core.Plan", client_rate=5200)
    client = baker.make("client.Client", plan=plan, payment_option="A")
    rate = utils.get_subscription_rate(client)
    assert rate == 5200


@pytest.mark.django_db
def _test_quarterly_subscription_calculated_correctly():
    """biannual subscription calculated correctly"""
    plan = baker.make("core.Plan", client_rate=5200)
    client = baker.make("client.Client", plan=plan, payment_option="Q")
    rate = utils.get_subscription_rate(client)
    assert rate == 1300