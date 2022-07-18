from requests import get, Response
from typing import Any, Dict, List, Union

from django.conf import settings

REVENUECAT_REST_URL = "https://api.revenuecat.com/v1/subscribers"
JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]

class RevenueCatService:
    """A wrapper to communicate with RevenueCat API."""

    def __init__(self, app_user_id, *args, **kwargs):
        self.app_user_id = app_user_id
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.REVENUE_CAT_API_KEY}",
            "Content-Type": "application/json",
        }

    def get_response(self) -> Response:
        """
        Returns a [Subscriber](https://docs.revenuecat.com/reference/subscribers#the-subscriber-object)
        Object with subscription and non-subscription details
        """
        response = get(
            url=f"{REVENUECAT_REST_URL}/{self.app_user_id}", headers=self.headers
        )

        return response

    def revoke_subscription(self, product_identifier: str) -> Response:
        """
        Revoke a user subscription from Google Play
        """
        
        url = f"{REVENUECAT_REST_URL}/{self.app_user_id}/subscriptions/{product_identifier}/revoke"

        response = get(url=url, headers=self.headers)

        return response


"""
Sample Response from RevenueCat
{
    "request_date": "2022-07-11T06:34:15Z",
    "request_date_ms": 1657521244881,
    "subscriber": {
        "entitlements": {
            "test_plan": {
                "expires_date": null,
                "grace_period_expires_date": null,
                "product_identifier": "test_plan",
                "purchase_date": "2022-07-11T06:32:19Z"
            }
        },
        "first_seen": "2022-07-11T06:04:04Z",
        "last_seen": "2022-07-11T06:04:04Z",
        "management_url": null,
        "non_subscriptions": {
            "test_plan": [
                {
                    "id": "98787dh5ss",
                    "is_sandbox": true,
                    "original_purchase_date": "2022-07-11T06:10:38Z",
                    "purchase_date": "2022-07-11T06:10:38Z",
                    "store": "play_store"
                },
                {
                    "id": "98787dh5ss",
                    "is_sandbox": true,
                    "original_purchase_date": "2022-07-11T06:32:19Z",
                    "purchase_date": "2022-07-11T06:32:19Z",
                    "store": "play_store"
                }
            ]
        },
        "original_app_user_id": "$RCAnonymousID:253affa82fc84feca9dbd046836028cb",
        "original_application_version": null,
        "original_purchase_date": null,
        "other_purchases": {
            "test_plan": {"purchase_date": "2022-07-11T06:32:19Z"}
        },
        "subscriptions": {}
    }
}

"""
