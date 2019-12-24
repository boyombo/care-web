import pytest
from django.utils import timezone
from model_bakery import baker
from dateutil.relativedelta import relativedelta

from subscription import utils
from subscription.models import Subscription
from client.models import Dependant


@pytest.fixture
def plan_rate():
    _plan = baker.make("core.Plan", has_extra=True, family_inclusive=True, size=4)
    return baker.make(
        "core.PlanRate", plan=_plan, payment_cycle="M", rate=520, extra_rate=400
    )


@pytest.fixture
def plan():
    return baker.make("core.Plan", has_extra=True, family_inclusive=True, size=4)


@pytest.mark.django_db
def test_family(plan):
    """Test calculation of subscription amount for family plan with dependants
    who are part of the family"""
    dob = timezone.now() - relativedelta(years=10)
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=3620, extra_rate=580)
    primary = baker.make("client.Client", plan=plan, payment_option="M")
    baker.make("client.Dependant", relationship=Dependant.SPOUSE, primary=primary)
    baker.make("client.Dependant", relationship=Dependant.SON, primary=primary, dob=dob)
    baker.make(
        "client.Dependant", relationship=Dependant.DAUGHTER, primary=primary, dob=dob
    )
    rate = utils.get_subscription_rate(primary)
    assert rate == 3620


@pytest.mark.django_db
def test_family_sons(plan):
    """Test calculation of subscription amount for family plan with sons"""
    dob = timezone.now() - relativedelta(years=10)
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=3620, extra_rate=580)
    primary = baker.make("client.Client", plan=plan, payment_option="M")
    baker.make("client.Dependant", relationship=Dependant.SPOUSE, primary=primary)
    baker.make("client.Dependant", relationship=Dependant.SON, primary=primary, dob=dob)
    baker.make("client.Dependant", relationship=Dependant.SON, primary=primary, dob=dob)
    rate = utils.get_subscription_rate(primary)
    assert rate == 3620


@pytest.mark.django_db
def test_family_daughters(plan):
    """Test calculation of subscription amount for family plan with daughters"""
    dob = timezone.now() - relativedelta(years=10)
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=3620, extra_rate=580)
    primary = baker.make("client.Client", plan=plan, payment_option="M")
    baker.make("client.Dependant", relationship=Dependant.SPOUSE, primary=primary)
    baker.make(
        "client.Dependant", relationship=Dependant.DAUGHTER, primary=primary, dob=dob
    )
    baker.make(
        "client.Dependant", relationship=Dependant.DAUGHTER, primary=primary, dob=dob
    )
    rate = utils.get_subscription_rate(primary)
    assert rate == 3620


@pytest.mark.django_db
def test_family_other(plan):
    """Test calculation of subscription amount for family plan with others"""
    dob = timezone.now() - relativedelta(years=10)
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=3620, extra_rate=580)
    primary = baker.make("client.Client", plan=plan, payment_option="M")
    baker.make("client.Dependant", relationship=Dependant.SPOUSE, primary=primary)
    baker.make(
        "client.Dependant", relationship=Dependant.OTHERS, primary=primary, dob=dob
    )
    rate = utils.get_subscription_rate(primary)
    assert rate == 4200


@pytest.mark.django_db
def test_family_plus_other(plan):
    """Test calculation of subscription amount for family plan with others"""
    dob = timezone.now() - relativedelta(years=10)
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=3620, extra_rate=580)
    primary = baker.make("client.Client", plan=plan, payment_option="M")
    baker.make("client.Dependant", relationship=Dependant.SPOUSE, primary=primary)
    baker.make("client.Dependant", relationship=Dependant.SON, primary=primary, dob=dob)
    baker.make(
        "client.Dependant", relationship=Dependant.DAUGHTER, primary=primary, dob=dob
    )
    baker.make(
        "client.Dependant", relationship=Dependant.OTHERS, primary=primary, dob=dob
    )
    rate = utils.get_subscription_rate(primary)
    assert rate == 4200


@pytest.mark.django_db
def test_family_more_kids(plan):
    """Test calculation of subscription amount for family plan with others"""
    dob = timezone.now() - relativedelta(years=10)
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=3620, extra_rate=580)
    primary = baker.make("client.Client", plan=plan, payment_option="M")
    baker.make("client.Dependant", relationship=Dependant.SPOUSE, primary=primary)
    baker.make("client.Dependant", relationship=Dependant.SON, primary=primary, dob=dob)
    baker.make(
        "client.Dependant", relationship=Dependant.DAUGHTER, primary=primary, dob=dob
    )
    baker.make("client.Dependant", relationship=Dependant.SON, primary=primary, dob=dob)
    rate = utils.get_subscription_rate(primary)
    assert rate == 4200


@pytest.mark.django_db
def test_family_older_kids(plan):
    """Test calculation of subscription amount for family plan with a kid > 18 yrs old"""
    dob = timezone.now() - relativedelta(years=10)
    old = timezone.now() - relativedelta(years=18)
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=3620, extra_rate=580)
    primary = baker.make("client.Client", plan=plan, payment_option="M")
    baker.make("client.Dependant", relationship=Dependant.SPOUSE, primary=primary)
    baker.make("client.Dependant", relationship=Dependant.SON, primary=primary, dob=dob)
    baker.make(
        "client.Dependant", relationship=Dependant.DAUGHTER, primary=primary, dob=old
    )
    rate = utils.get_subscription_rate(primary)
    assert rate == 4200


@pytest.mark.django_db
def test_family_sons_plus_other(plan):
    """Test calculation of subscription amount for family plan with others"""
    dob = timezone.now() - relativedelta(years=10)
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=3620, extra_rate=580)
    primary = baker.make("client.Client", plan=plan, payment_option="M")
    baker.make("client.Dependant", relationship=Dependant.SPOUSE, primary=primary)
    baker.make("client.Dependant", relationship=Dependant.SON, primary=primary, dob=dob)
    baker.make("client.Dependant", relationship=Dependant.SON, primary=primary, dob=dob)
    baker.make(
        "client.Dependant", relationship=Dependant.DAUGHTER, primary=primary, dob=dob
    )
    baker.make(
        "client.Dependant", relationship=Dependant.OTHERS, primary=primary, dob=dob
    )
    rate = utils.get_subscription_rate(primary)
    assert rate == 4780


@pytest.mark.django_db
def test_family_daughters_one_adult(plan):
    """Test calculation of subscription amount for family plan with one daughter an adult"""
    dob = timezone.now() - relativedelta(years=10)
    older = timezone.now() - relativedelta(years=19)
    baker.make("core.PlanRate", plan=plan, payment_cycle="M", rate=3620, extra_rate=580)
    primary = baker.make("client.Client", plan=plan, payment_option="M")
    baker.make("client.Dependant", relationship=Dependant.SPOUSE, primary=primary)
    baker.make(
        "client.Dependant", relationship=Dependant.DAUGHTER, primary=primary, dob=dob
    )
    baker.make(
        "client.Dependant", relationship=Dependant.DAUGHTER, primary=primary, dob=dob
    )
    baker.make(
        "client.Dependant", relationship=Dependant.DAUGHTER, primary=primary, dob=older
    )
    rate = utils.get_subscription_rate(primary)
    assert rate == 4200


@pytest.mark.django_db
def test_sigle_with_extras():
    """Test calculation of subscription amount for family plan with one daughter an adult"""
    dob = timezone.now() - relativedelta(years=10)
    return baker.make("core.Plan", has_extra=True, family_inclusive=True, size=1)
    baker.make(
        "core.PlanRate", plan=plan, payment_cycle="A", rate=8500, extra_rate=6000
    )
    primary = baker.make("client.Client", plan=plan, payment_option="A")
    baker.make("client.Dependant", relationship=Dependant.SPOUSE, primary=primary)
    baker.make(
        "client.Dependant", relationship=Dependant.DAUGHTER, primary=primary, dob=dob
    )
    baker.make(
        "client.Dependant", relationship=Dependant.DAUGHTER, primary=primary, dob=dob
    )
    baker.make(
        "client.Dependant", relationship=Dependant.DAUGHTER, primary=primary, dob=dob
    )
    rate = utils.get_subscription_rate(primary)
    assert rate == 32500
