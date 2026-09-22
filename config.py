"""Shared configuration for the Personal Vehicle Service Records project."""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq").strip().lower()

if PROVIDER == "groq":
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")

else:
    raise SystemExit(
        f"Unknown PROVIDER '{PROVIDER}'. "
        "This project is configured for Groq."
    )

if not API_KEY:
    raise SystemExit(
        "No Groq API key found. Check your .env file."
    )

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)


# Private vehicle service data.
# This is our own scenario data.
VEHICLES = {
    "CAR101": {
        "model": "Honda City",
        "service_cost": 8500,
        "km": 42000,
        "last_service": "2026-06-10"
    },
    "CAR202": {
        "model": "Hyundai i20",
        "service_cost": 6200,
        "km": 35000,
        "last_service": "2026-07-15"
    },
    "CAR303": {
        "model": "Toyota Glanza",
        "service_cost": 9100,
        "km": 51000,
        "last_service": "2026-05-20"
    }
}


QUESTIONS = [
    "What was the service cost for CAR101?",
    "What is the total service cost for CAR101 and CAR202?",
    "Is CAR303 more expensive to service than CAR202, and by how much?",
    "Write a two-line service reminder for a vehicle owner."
]


def banner(system_name):
    print(
        f"\n=== {system_name} | "
        f"provider: {PROVIDER} | model: {MODEL} ===\n"
    )