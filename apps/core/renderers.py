from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler
from rest_framework import status


class CustomAPIRenderer(JSONRenderer):

	POSITIVE_RESPONSES = [
		status.HTTP_200_OK,
		status.HTTP_201_CREATED,
		status.HTTP_202_ACCEPTED,
		status.HTTP_204_NO_CONTENT
	]
	
	NEGATIVE_RESPONSES = [
		status.HTTP_400_BAD_REQUEST,
		status.HTTP_401_UNAUTHORIZED,
		status.HTTP_403_FORBIDDEN,
		status.HTTP_404_NOT_FOUND,
		status.HTTP_405_METHOD_NOT_ALLOWED,
		status.HTTP_422_UNPROCESSABLE_ENTITY,
		status.HTTP_429_TOO_MANY_REQUESTS,
		status.HTTP_418_IM_A_TEAPOT
	]
	
	def render(self, data, accepted_media_type=None, renderer_context=None):
		response = {
			'data': data,
			'message': '',
			'success': False,
		}
		status_code = renderer_context['response'].status_code
		if status_code in self.NEGATIVE_RESPONSES:
			try:
				response["message"] = data["detail"]
			except KeyError:
				response.update({
					"message": "Error Processing Request"
				})

		elif status_code in self.POSITIVE_RESPONSES:
			response.update({
				"success": True,
				"message": "Request Processed Successfully"
			})

		return super().render(response, accepted_media_type, renderer_context)