from typing import Any
from django.http import JsonResponse

from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import exception_handler

from apps.core.renderers import CustomAPIRenderer

def get_structured_response(
	message=None,
	result=None,
	success: bool=False,
	status_code: int=HTTP_200_OK
) -> dict:
	return {
		"message": message or str(),
		"result": result or dict(),
		"success": success,
		"status_code": status_code,
	}


def get_error_message(error: dict):
	response = error[next(iter(error))]
	if isinstance(response, dict):
		response = get_structured_response(response)
	elif isinstance(response, list):
		if isinstance(response[0], dict):
			response = get_structured_response(response[0])
		else:
			response = response[0]
	return response


def custom_exception_handler(exc, context):
	response = exception_handler(exc, context)

	if response:
		error = response.data

		if isinstance(error, list) and error:
			if isinstance(error[0], dict):
				response.data = get_structured_response(
					message=get_error_message(error),
					result=error,
					success=False,
					status_code=error.status_code
				)

			elif isinstance(error[0], str):
				response.data = get_structured_response(
					message=error[0],
					result=error[1],
					success=False,
					status_code=response.get('status_code')
				)
		
		elif isinstance(error, dict):
			response.data = get_structured_response(
				message=get_error_message(error),
				result=error,
				success=False,
				status_code=response.status_code
			)
	
	return response


class CustomExceptionMiddleware(object):
	def __init__(self, response) -> None:
		self.response = response
	
	def __call__(self, request) -> Any:
		response = get_structured_response(request)

		if response.get('status_code') == HTTP_404_NOT_FOUND:
			response = get_structured_response(
				message="Page/Object not found",
				status_code=response.get('status_code')
			)

			return JsonResponse(response, status=HTTP_404_NOT_FOUND)
		
		if response.get('status_code') == HTTP_500_INTERNAL_SERVER_ERROR:
			response = get_structured_response(
				message="Internal Server Error occured. Try Again later.",
				success=False,
				status_code=response.get('status_code')
			)
			return JsonResponse(response, status=HTTP_500_INTERNAL_SERVER_ERROR)
		return response