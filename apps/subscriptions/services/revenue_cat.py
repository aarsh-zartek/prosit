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

