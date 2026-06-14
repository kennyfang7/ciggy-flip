import random
import requests
import os

# Config
MIN_SMOKES = 1
MAX_SMOKES = 10
NUM_FLIPS = 10  # How many coins to flip
WEBHOOK_URL = os.environ["WEBHOOK_URL"]  # Pulled securely from GitHub Secrets


def flip_coins(num_flips: int) -> int:

    results = [random.choice([0, 1]) for _ in range(num_flips)]
    total = sum(results)
    return max(MIN_SMOKES, min(total, MAX_SMOKES))


def send_to_discord(cigarette_count: int):

    if cigarette_count == MIN_SMOKES:
        note = "Tough luck — minimum day. 💪"
    elif cigarette_count == MAX_SMOKES:
        note = "Maximum day. Try to stay strong. 🙏"
    else:
        note = "Stay mindful today."

    payload = {
        "content": (
            f"🪙 **Daily Cigarette Limit**\n"
            f"The coins have spoken: **{cigarette_count}** cigarette(s) today.\n"
            f"{note}"
        )
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    response.raise_for_status()  # Raises an error if the Discord call fails
    print(f"✅ Sent limit of {cigarette_count} to Discord.")


if __name__ == "__main__":
    limit = flip_coins(NUM_FLIPS)
    send_to_discord(limit)