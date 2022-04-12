from django.shortcuts import redirect, render
import logging

# def handle_exception(get_response):
#     def process_exception(request, exception):
#         response = get_response(request, exception)
#         if response.status_code >= 500:
#             return redirect('500')
#         if response.status_code >= 400:
#             logging.error(f'Bequest path: {request.path} Status code: {response.status_code}')
#             return redirect('400')
#         return response
#
#     return process_exception
#

class HandleExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response


    def process_exception(self, request, exception):
        logging.error(f'Path: {request.path} Excpetion: {repr(exception)}' )
        return redirect('error page')