from datetime import datetime


def create_record(customer, action, status="Completed", details=""):
    """Create a record of an action taken by the agent."""

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "customer": customer["name"],
        "booking_reference": customer["booking_reference"],
        "action": action,
        "status": status,
        "details": details
    }


def initiate_refund(customer):
    """Initiate full refund for an airline-caused cancellation."""

    return create_record(
        customer,
        "Full refund initiated",
        "Completed",
        "Refund will be processed to the original payment method within 7 business days."
    )


def rebook_customer(customer):
    """Rebook customer on the next available flight within 24 hours."""

    return create_record(
        customer,
        "Free rebooking requested",
        "Completed",
        "Next available flight within 24 hours."
    )


def issue_meal_voucher(customer):
    """Issue meal voucher."""

    return create_record(
        customer,
        "Meal voucher issued",
        "Completed",
        "Meal voucher provided according to delay policy."
    )


def provide_lounge_access(customer):
    """Provide lounge access."""

    return create_record(
        customer,
        "Lounge access provided",
        "Completed",
        "Lounge access provided according to delay policy."
    )


def arrange_hotel(customer):
    """Arrange hotel for eligible delayed hours only."""

    return create_record(
        customer,
        "Hotel accommodation arranged",
        "Completed",
        "Accommodation covers delayed hours only, not a full night's stay."
    )


def escalate_to_human(customer, reason):
    """Create a human escalation record."""

    return create_record(
        customer,
        "Human escalation",
        "Escalated",
        reason
    )