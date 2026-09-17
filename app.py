import streamlit as st
import json

from agent import generate_response


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Airline Resolution Agent",
    page_icon="✈️",
    layout="wide"
)


# -----------------------------
# LOAD DATA
# -----------------------------
try:
    with open("data/customers.json", "r", encoding="utf-8") as file:
        customers = json.load(file)

    with open("data/bookings.json", "r", encoding="utf-8") as file:
        bookings = json.load(file)

except Exception as e:
    st.error("❌ Error loading customer or booking data.")
    st.exception(e)
    st.stop()


# -----------------------------
# CHECK DATA
# -----------------------------
if not customers:
    st.error("❌ No customers found in customers.json")
    st.stop()

if not bookings:
    st.error("❌ No bookings found in bookings.json")
    st.stop()


# -----------------------------
# TITLE
# -----------------------------
st.title("✈️ Airline Customer Resolution Agent")
st.write("AI-powered customer support agent for airline disruptions.")

st.divider()


# -----------------------------
# CUSTOMER SELECTION
# -----------------------------
customer_names = [
    customer.get("name", "Unknown Customer")
    for customer in customers
]

selected_name = st.selectbox(
    "👤 Select Customer",
    customer_names
)


# Find selected customer
customer = next(
    customer for customer in customers
    if customer.get("name") == selected_name
)


# -----------------------------
# FIND BOOKING
# -----------------------------
customer_bookings = [
    booking for booking in bookings
    if booking.get("customer") == selected_name
]

if not customer_bookings:
    st.error(f"❌ No booking found for {selected_name}")
    st.stop()

booking = customer_bookings[0]


# -----------------------------
# BOOKING INFORMATION
# -----------------------------
st.subheader("📋 Booking Information")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Customer:** {customer.get('name', 'N/A')}")
    st.write(
        f"**Loyalty Tier:** "
        f"{customer.get('loyalty_tier', 'N/A')}"
    )
    st.write(
        f"**Booking Reference:** "
        f"{customer.get('booking_reference', 'N/A')}"
    )

with col2:
    st.write(
        f"**Flight:** "
        f"{booking.get('flight', 'N/A')}"
    )
    st.write(
        f"**Route:** "
        f"{booking.get('route', 'N/A')}"
    )
    st.write(
        f"**Status:** "
        f"{booking.get('status', 'N/A')}"
    )

st.divider()


# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "action_logs" not in st.session_state:
    st.session_state.action_logs = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# -----------------------------
# AI DECISION
# -----------------------------
if st.session_state.last_result:

    result = st.session_state.last_result

    st.subheader("🤖 AI Decision")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            f"**Intent:** {result.get('intent', 'N/A')}"
        )

    with col2:
        st.info(
            f"**Emotion:** {result.get('emotion', 'N/A')}"
        )


# -----------------------------
# ACTION LOG
# -----------------------------
st.subheader("⚙️ Action Log")

if st.session_state.action_logs:

    for action in reversed(st.session_state.action_logs):

        if action.get("status") == "Escalated":

            st.warning(
                f"🚨 **{action.get('action', 'Action')}**\n\n"
                f"Customer: {action.get('customer', 'N/A')}\n\n"
                f"Reason: {action.get('details', 'N/A')}"
            )

        else:

            st.success(
                f"✅ **{action.get('action', 'Action')}**\n\n"
                f"Customer: {action.get('customer', 'N/A')}\n\n"
                f"Details: {action.get('details', 'N/A')}"
            )

else:

    st.info("No actions taken yet.")


st.divider()


# -----------------------------
# CHAT HISTORY
# -----------------------------
st.subheader("💬 Customer Support Chat")

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# -----------------------------
# CHAT INPUT
# -----------------------------
user_message = st.chat_input(
    "Type customer's issue here..."
)


# -----------------------------
# PROCESS MESSAGE
# -----------------------------
if user_message:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    try:

        result = generate_response(
            customer,
            booking,
            user_message
        )

        # Save result
        st.session_state.last_result = result

        # Save actions
        for action in result.get("actions_taken", []):
            st.session_state.action_logs.append(action)

        # Add AI response
        st.session_state.messages.append({
            "role": "assistant",
            "content": result.get(
                "response",
                "I could not generate a response."
            )
        })

    except Exception as e:

        st.error("❌ Error while processing the request.")
        st.exception(e)

    st.rerun()