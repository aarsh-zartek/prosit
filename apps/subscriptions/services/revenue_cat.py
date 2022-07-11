import requests

from django.conf import settings


REVENUE_CAT_REST_URL = "https://api.revenuecat.com/v1/subscribers"


class RevenueCat:

	def __init__(self, user_id, *args, **kwargs):
		self.user_id = user_id

	
	def get_status(self):

		response = requests.get(
				url=f"{REVENUE_CAT_REST_URL}/{self.user_id}",
				headers={
					'Accept': 'application/json',
					'Authorization': f'Bearer {settings.REVENUE_CAT_API_KEY}',
					'Content-Type': 'application/json',
				}
			)
		
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
