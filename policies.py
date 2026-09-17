# Airline Service Policies


def cancellation_policy():
    """
    Policy for airline-caused flight cancellation.
    """

    return {
        "free_rebooking": True,
        "rebooking_limit": "next available flight within 24 hours",
        "full_refund": True,
        "refund_processing": "within 7 business days",
        "refund_method": "original payment method"
    }


def delay_policy(delay_hours):
    """
    Returns compensation based on the length of the delay.
    """

    if delay_hours < 3:
        return {
            "meal_voucher": True,
            "lounge_access": False,
            "hotel": False
        }

    elif delay_hours > 5:
        return {
            "meal_voucher": True,
            "lounge_access": True,
            "hotel": True,
            "hotel_coverage": "delayed hours only"
        }

    else:
        return {
            "meal_voucher": True,
            "lounge_access": True,
            "hotel": False
        }


def loyalty_policy(loyalty_tier):
    """
    Gold and Platinum customers get priority rebooking.
    No additional compensation is provided because of loyalty tier.
    """

    if loyalty_tier in ["Gold", "Platinum"]:
        return {
            "priority_rebooking": True,
            "extra_compensation": False
        }

    return {
        "priority_rebooking": False,
        "extra_compensation": False
    }


def fare_difference_policy(fare_difference):
    """
    Handles higher-fare voluntary rebooking.
    """

    if fare_difference > 1500:
        return {
            "supervisor_approval_required": True
        }

    return {
        "supervisor_approval_required": False
    }


def extra_compensation_policy():
    """
    Compensation beyond the stated policy requires escalation.
    """

    return {
        "human_approval_required": True
    }