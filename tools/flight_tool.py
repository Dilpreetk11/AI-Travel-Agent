# import os
import requests
import streamlit as st

from dotenv import load_dotenv


# ============================================================
# LOAD .ENV
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


# ============================================================
# GET AVIATIONSTACK API KEY
# ============================================================

# First try local .env
API_KEY = os.getenv("AVIATIONSTACK_API_KEY")


# If not found, try Streamlit Cloud Secrets
if not API_KEY:
    try:
        API_KEY = st.secrets.get("AVIATIONSTACK_API_KEY")
    except Exception:
        API_KEY = None


# ============================================================
# CHECK API KEY
# ============================================================

if not API_KEY:
    raise ValueError(
        "AVIATIONSTACK_API_KEY is missing. "
        "Add it to your .env file or Streamlit Cloud Secrets."
    )


# ============================================================
# SEARCH FLIGHTS
# ============================================================

def search_flights(query):

    url = "http://api.aviationstack.com/v1/flights"

    params = {
        "access_key": API_KEY,
        "limit": 5
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        flights = []

        if "data" in data:

            for flight in data["data"][:5]:

                airline = (
                    flight
                    .get("airline", {})
                    .get("name", "Unknown")
                )

                departure = (
                    flight
                    .get("departure", {})
                    .get("airport", "Unknown")
                )

                arrival = (
                    flight
                    .get("arrival", {})
                    .get("airport", "Unknown")
                )

                status = flight.get(
                    "flight_status",
                    "Unknown"
                )

                flights.append(
                    f"""
Airline: {airline}

Departure: {departure}

Arrival: {arrival}

Status: {status}
"""
                )

        if not flights:
            return "No flight data found."

        return "\n".join(flights)

    except Exception as e:

        print(
            f"Flight search failed: {e}"
        )

        return (
            "Flight search is temporarily unavailable."
        )