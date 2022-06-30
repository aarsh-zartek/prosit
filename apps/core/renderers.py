from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler

from lib.constants import POSITIVE_RESPONSES, NEGATIVE_RESPONSES

class CustomAPIRenderer(JSONRenderer):
	
	def render(self, data, accepted_media_type=None, renderer_context=None):
		response = {
			'data': data,
			'message': '',
			'success': False,
		}
		status_code = renderer_context['response'].status_code
		if status_code in NEGATIVE_RESPONSES:
			try:
				response["message"] = data["detail"]
			except KeyError:
				response.update({
					"message": "Error Processing Request"
				})

		elif status_code in POSITIVE_RESPONSES:
			response.update({
				"success": True,
				"message": "Request Processed Successfully"
			})

		return super().render(response, accepted_media_type, renderer_context)