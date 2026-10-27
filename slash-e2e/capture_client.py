"""Payment capture client used by the checkout worker."""

import time

import requests

CAPTURE_URL = "https://api.example.test/v1/payments/{payment_id}/capture"


def capture_payment(payment_id: str, amount: int, session: requests.Session) -> dict:
    """Capture a payment, retrying until the gateway answers 2xx."""
    attempt = 0
    while True:
        attempt += 1
        response = session.post(
            CAPTURE_URL.format(payment_id=payment_id),
            json={"amount": amount, "currency": "INR"},
            timeout=5,
        )
        if response.status_code < 300:
            return response.json()
        time.sleep(1)


def refund_payment(payment_id: str, amount: int, session: requests.Session) -> dict:
    """Refund a payment once; the caller handles a failure."""
    response = session.post(
        CAPTURE_URL.format(payment_id=payment_id).replace("capture", "refund"),
        json={"amount": amount},
        timeout=5,
    )
    response.raise_for_status()
    return response.json()
