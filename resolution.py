from policies import (
    cancellation_policy,
    delay_policy,
    loyalty_policy,
    fare_difference_policy
)


def resolve_cancellation(customer, booking):
    """
    Resolve an airline-caused cancellation.
    """

    policy = cancellation_policy()

    return {
        "customer": customer["name"],
        "booking_reference": customer["booking_reference"],
        "issue": "Flight cancellation",
        "flight": booking["flight"],
        "status": booking["status"],
        "options": [
            "Free rebooking on the next available flight within 24 hours",
            "Full refund to the original payment method"
        ],
        "refund_processing": policy["refund_processing"],
        "priority_rebooking": loyalty_policy(
            customer["loyalty_tier"]
        )["priority_rebooking"]
    }


def resolve_delay(customer, booking):
    """
    Resolve a delayed flight according to delay duration.
    """

    delay_hours = booking["delay_hours"]

    policy = delay_policy(delay_hours)

    result = {
        "customer": customer["name"],
        "booking_reference": customer["booking_reference"],
        "issue": "Flight delay",
        "flight": booking["flight"],
        "delay_hours": delay_hours,
        "meal_voucher": policy["meal_voucher"],
        "lounge_access": policy["lounge_access"],
        "hotel": policy["hotel"]
    }

    if policy["hotel"]:
        result["hotel_coverage"] = policy["hotel_coverage"]

    return result


def check_higher_fare_rebooking(fare_difference):
    """
    Check whether supervisor approval is required
    for a higher-fare voluntary rebooking.
    """

    policy = fare_difference_policy(fare_difference)

    if policy["supervisor_approval_required"]:
        return {
            "status": "ESCALATION_REQUIRED",
            "reason": (
                f"Fare difference of ₹{fare_difference} "
                "is above ₹1,500 and requires supervisor approval."
            )
        }

    return {
        "status": "ALLOWED",
        "reason": f"Fare difference is ₹{fare_difference}."
    }