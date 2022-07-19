from requests import get, Response

from django.conf import settings

import logging
logger = logging.getLogger(__name__)

REVENUECAT_REST_URL = "https://api.revenuecat.com/v1/subscribers"


class RevenueCatService:
    """A wrapper to communicate with RevenueCat API."""

    def __init__(self, app_user_id, *args, **kwargs):
        self.app_user_id = app_user_id
        self.url = f"{REVENUECAT_REST_URL}/{self.app_user_id}"

        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.REVENUE_CAT_API_KEY}",
            "Content-Type": "application/json",
        }

    def get_response(self) -> Response:
        """
        Returns a [Subscriber](https://docs.revenuecat.com/reference/subscribers#the-subscriber-object)
        Object with subscription, non-subscription and entitlement objects
        """
        response = get(url=self.url, headers=self.headers)

        return response

    def revoke_subscription(self, product_identifier: str) -> Response:
        """
        Revoke a user subscription from Google Play
        """

        url = f"{REVENUECAT_REST_URL}/{self.app_user_id}/subscriptions/{product_identifier}/revoke"

        response = get(url=url, headers=self.headers)

        return response

    def verify_non_subscription_payment(
        self, product_identifier: str, rc_id: str, purchase_date
    ) -> bool:
        """
        Verifies a [Non Subscription](https://docs.revenuecat.com/reference/subscribers#the-non-subscription-object) Payment from RevenueCat

        Args:
            product_identifier (str): Identifier to identify the product
            rc_id (str): RevenueCat Purchase ID
            purchase_date (date | str): Purchase Date of the product

        Returns:
            bool: If the product purchase is successful
        """

        response = self.get_response().json()
        non_subscriptions = response["subscriber"]["non_subscriptions"]
        try:
            products = non_subscriptions[product_identifier]
        except KeyError as ke:
            logger.exception(ke)
            return False
        else:
            for product in products:
                if product["id"] == rc_id:
                    return True
        return False
