"""System 2: Rule-based workflow with no LLM."""

import re
from config import VEHICLES, QUESTIONS


def workflow(question):
    codes = re.findall(r"CAR\d{3}", question.upper())

    vehicles = [
        VEHICLES[code]
        for code in codes
        if code in VEHICLES
    ]

    if not vehicles:
        return "Sorry, I can only answer questions about vehicle service records."

    text = question.lower()

    # Single vehicle service cost
    if len(vehicles) == 1 and "cost" in text:
        code = codes[0]
        return (
            f"Service cost for {code}: "
            f"Rs. {VEHICLES[code]['service_cost']:,}"
        )

    # Total service cost
    if "total" in text and len(vehicles) >= 2:
        total = sum(vehicle["service_cost"] for vehicle in vehicles)

        return f"Total service cost: Rs. {total:,}"

    # Comparison
    if (
        len(vehicles) >= 2
        and ("more expensive" in text or "difference" in text)
    ):
        first = vehicles[0]["service_cost"]
        second = vehicles[1]["service_cost"]

        difference = abs(first - second)

        if first > second:
            return f"{codes[0]} costs Rs. {difference:,} more to service than {codes[1]}."
        elif second > first:
            return f"{codes[1]} costs Rs. {difference:,} more to service than {codes[0]}."
        else:
            return "Both vehicles have the same service cost."

    return "Sorry, I do not have a rule for this type of question."


if __name__ == "__main__":
    print("\n=== SYSTEM 2: RULE-BASED WORKFLOW ===\n")

    for question in QUESTIONS:
        print("Q:", question)
        print("A:", workflow(question))
        print("-" * 70)