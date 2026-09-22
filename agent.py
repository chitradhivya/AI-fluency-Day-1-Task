"""System 3: AI agent using an LLM + tools + loop."""

import json

from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = (
    "You are a vehicle service assistant. "
    "Never guess private vehicle service information. "
    "Always use get_vehicle_service_record when a vehicle code "
    "is mentioned. "
    "Use calculator for arithmetic. "
    "Available vehicle codes are CAR101, CAR202 and CAR303. "
    "If no tool is needed, answer directly."
)


def agent(question, max_steps=6, verbose=True):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(1, max_steps + 1):

        # 1. Ask the LLM what to do next
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        message = response.choices[0].message

        # 2. If no tool is requested, return the final answer
        if not message.tool_calls:
            return message.content.strip()

        # 3. Add the assistant tool request to the conversation
        messages.append(
            {
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments
                        }
                    }
                    for call in message.tool_calls
                ]
            }
        )

        # 4. Execute each requested tool
        for call in message.tool_calls:

            name = call.function.name

            arguments = json.loads(
                call.function.arguments or "{}"
            )

            function = TOOL_FUNCTIONS.get(name)

            if function:
                result = function(**arguments)
            else:
                result = f"Unknown tool: {name}"

            if verbose:
                print(
                    f"   step {step}: "
                    f"{name}({arguments}) -> {result}"
                )

            # 5. Send tool result back to the LLM
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result
                }
            )

    return "Stopped: maximum steps reached."


if __name__ == "__main__":

    banner("SYSTEM 3: AI AGENT")

    for question in QUESTIONS:

        print("Q:", question)

        print("A:", agent(question))

        print("-" * 70)