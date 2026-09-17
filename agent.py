import json

from policies import (
    cancellation_policy,
    delay_policy,
    loyalty_policy,
    fare_difference_policy
)

from actions import (
    initiate_refund,
    rebook_customer,
    issue_meal_voucher,
    provide_lounge_access,
    arrange_hotel,
    escalate_to_human
)


def understand_customer(message):
    """
    Local customer intent and emotion detection.
    No OpenAI API required.
    """

    text = message.lower()

    # -------------------------
    # EMOTION
    # -------------------------
    angry_words = [
        "angry",
        "unacceptable",
        "ridiculous",
        "terrible",
        "worst",
        "complaint",
        "furious",
        "very angry"
    ]

    frustrated_words = [
        "frustrated",
        "waiting",
        "annoyed",
        "upset",
        "disappointed",
        "not helping"
    ]

    if any(word in text for word in angry_words):
        emotion = "angry"

    elif any(word in text for word in frustrated_words):
        emotion = "frustrated"

    else:
        emotion = "neutral"

    # -------------------------
    # INTENT
    # -------------------------

    if any(word in text for word in [
        "refund",
        "money back",
        "get my money"
    ]):
        intent = "refund"

    elif any(word in text for word in [
        "cancel",
        "cancelled",
        "canceled"
    ]):
        intent = "cancellation"

    elif any(word in text for word in [
        "rebook",
        "rebooking",
        "change my flight",
        "change flight",
        "another flight"
    ]):
        intent = "rebooking"

    elif any(word in text for word in [
        "hotel",
        "accommodation",
        "stay"
    ]):
        intent = "hotel"

    elif any(word in text for word in [
        "meal",
        "food",
        "voucher"
    ]):
        intent = "meal_voucher"

    elif any(word in text for word in [
        "lounge"
    ]):
        intent = "lounge"

    elif any(word in text for word in [
        "compensation",
        "compensate",
        "additional compensation"
    ]):
        intent = "extra_compensation"

    elif any(word in text for word in [
        "human",
        "agent",
        "manager",
        "complaint",
        "speak to someone"
    ]):
        intent = "complaint"

    else:
        intent = "general"

    return {
        "intent": intent,
        "emotion": emotion
    }


def generate_response(customer, booking, message):

    understanding = understand_customer(message)

    intent = understanding["intent"]
    emotion = understanding["emotion"]

    response = ""
    actions_taken = []

    # -------------------------
    # EMOTION RESPONSE
    # -------------------------

    if emotion in ["angry", "frustrated"]:
        response += (
            "I understand that this disruption has been frustrating. "
        )

    # =========================
    # CANCELLED FLIGHT
    # =========================

    if booking["status"] == "Cancelled":

        if intent == "refund":

            policy = cancellation_policy()

            action = initiate_refund(customer)
            actions_taken.append(action)

            response += (
                "Your flight was cancelled due to operational reasons. "
                "You are entitled to a full refund. "
                f"The refund will be processed to your "
                f"{policy['refund_method']} "
                f"{policy['refund_processing']}."
            )

        elif intent == "rebooking":

            loyalty = loyalty_policy(
                customer["loyalty_tier"]
            )

            action = rebook_customer(customer)
            actions_taken.append(action)

            response += (
                "Your free rebooking request has been initiated. "
                "You can be rebooked on the next available flight "
                "within 24 hours."
            )

            if loyalty["priority_rebooking"]:
                response += (
                    f" As a {customer['loyalty_tier']} customer, "
                    "you receive priority rebooking."
                )

        elif intent == "extra_compensation":

            action = escalate_to_human(
                customer,
                "Customer requested additional compensation "
                "not authorized by the supplied policy."
            )

            actions_taken.append(action)

            response += (
                "I understand you are requesting additional compensation. "
                "The supplied policy does not authorize additional "
                "compensation. Your request has been escalated to a "
                "human agent for review."
            )

        elif intent == "complaint":

            action = escalate_to_human(
                customer,
                "Customer requested human assistance."
            )

            actions_taken.append(action)

            response += (
                "I understand your concern. "
                "Your request has been escalated to a human agent "
                "for further assistance."
            )

        else:

            response += (
                "Your flight was cancelled due to operational reasons. "
                "You can choose either free rebooking on the next available "
                "flight within 24 hours or a full refund."
            )

    # =========================
    # DELAYED FLIGHT
    # =========================

    elif booking["status"] == "Delayed":

        delay_hours = booking["delay_hours"]

        policy = delay_policy(delay_hours)

        if intent == "hotel":

            if policy["hotel"]:

                action = arrange_hotel(customer)
                actions_taken.append(action)

                response += (
                    f"Your flight is delayed by {delay_hours} hours. "
                    "Hotel accommodation has been arranged for the "
                    "eligible delayed hours. "
                    "A full night's stay is not covered by the supplied policy."
                )

            else:

                response += (
                    f"Your flight is delayed by {delay_hours} hours. "
                    "Hotel accommodation does not apply under the "
                    "supplied policy."
                )

        elif intent == "meal_voucher":

            if policy["meal_voucher"]:

                action = issue_meal_voucher(customer)
                actions_taken.append(action)

                response += (
                    f"Your flight is delayed by {delay_hours} hours. "
                    "A meal voucher has been issued."
                )

            else:

                response += (
                    "A meal voucher is not available under the "
                    "applicable delay policy."
                )

        elif intent == "lounge":

            if policy["lounge_access"]:

                action = provide_lounge_access(customer)
                actions_taken.append(action)

                response += (
                    "Lounge access has been provided according to "
                    "the applicable delay policy."
                )

            else:

                response += (
                    "Lounge access is not available under the "
                    "applicable delay policy."
                )

        elif intent == "rebooking":

            fare_difference = 2000

            fare_check = fare_difference_policy(fare_difference)

            if fare_check["supervisor_approval_required"]:

                action = escalate_to_human(
                    customer,
                    f"Fare difference of ₹{fare_difference} "
                    "requires supervisor approval."
                )

                actions_taken.append(action)

                response += (
                    f"The requested flight has a fare difference of "
                    f"₹{fare_difference}. Supervisor approval is required, "
                    "so I have escalated your rebooking request to a "
                    "human agent."
                )

            else:

                response += (
                    "Your rebooking request can be processed according "
                    "to the applicable fare-difference policy."
                )

        elif intent == "complaint":

            action = escalate_to_human(
                customer,
                "Customer requested human assistance."
            )

            actions_taken.append(action)

            response += (
                "I understand your concern. "
                "Your request has been escalated to a human agent "
                "for further assistance."
            )

        else:

            response += (
                f"Your flight is delayed by {delay_hours} hours. "
            )

            if policy["meal_voucher"]:
                response += "You qualify for a meal voucher. "

            if policy["lounge_access"]:
                response += "You qualify for lounge access. "

            if policy["hotel"]:
                response += (
                    "You also qualify for hotel accommodation covering "
                    "the delayed hours only."
                )

    # =========================
    # OTHER STATUS
    # =========================

    else:

        response += (
            f"Your flight {booking['flight']} is currently shown as "
            f"{booking['status']}."
        )

    return {
        "intent": intent,
        "emotion": emotion,
        "response": response,
        "actions_taken": actions_taken
    }