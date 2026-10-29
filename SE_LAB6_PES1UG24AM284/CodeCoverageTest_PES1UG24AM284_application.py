import pytest

from mobile_data_plan import (
    overage_charge,
    recharge_allowed,
    validity_status,
)


# Code coverage tests for overage_charge

def test_overage_unknown_plan():
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge("gold", 5, False, False)


def test_overage_negative_data():
    with pytest.raises(ValueError, match="invalid data usage"):
        overage_charge("basic", -1, False, False)


def test_overage_loyal_customer():
    assert overage_charge("basic", 3, False, True) == 0


def test_overage_non_roaming():
    assert overage_charge("basic", 5, False, False) == 45


def test_overage_roaming():
    assert overage_charge("basic", 3, True, False) == 40


def test_overage_large_non_roaming():
    assert overage_charge("basic", 13, False, False) == 275


def test_overage_large_roaming():
    assert overage_charge("basic", 13, True, False) == 605


def test_premium_loyal_customer():
    assert overage_charge("premium", 10, False, True) == 0


# Code coverage tests for recharge_allowed

def test_recharge_kyc_within_limit():
    assert recharge_allowed(200, 5, True) is True


def test_recharge_kyc_over_limit():
    assert recharge_allowed(201, 1, True) is False


def test_recharge_over_2000():
    assert recharge_allowed(2001, 0, False) is False


def test_recharge_too_many_pending():
    assert recharge_allowed(500, 3, False) is False


def test_recharge_two_pending():
    assert recharge_allowed(500, 2, False) is True


# Code coverage tests for validity_status

def test_validity_prepaid_active():
    assert validity_status(0, True, False) == "active"


def test_validity_postpaid_active():
    assert validity_status(3, False, False) == "active"


def test_validity_addon_cutoff():
    assert validity_status(2, True, True) == "active"


def test_validity_grace():
    assert validity_status(-1, True, False) == "grace"


def test_validity_expired():
    assert validity_status(-16, True, False) == "expired"


def test_validity_postpaid_grace():
    assert validity_status(-12, False, False) == "grace"
