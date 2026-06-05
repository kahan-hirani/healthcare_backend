"""
Custom exception handler for consistent API error responses.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent error format.
    Format: {"error": "message"}
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Customize the response format
        error_message = "Something went wrong"
        
        # Extract error message from response data
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                error_message = response.data['detail']
            elif 'non_field_errors' in response.data:
                error_message = response.data['non_field_errors'][0]
            else:
                # Get the first error message from any field
                first_key = list(response.data.keys())[0]
                first_error = response.data[first_key]
                if isinstance(first_error, list):
                    error_message = first_error[0]
                else:
                    error_message = str(first_error)
        elif isinstance(response.data, list):
            error_message = response.data[0]
        
        # Return consistent error format
        return Response(
            {"error": error_message},
            status=response.status_code
        )
    
    # If no response from default handler, return generic 500 error
    return Response(
        {"error": "Internal server error"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
