from django.shortcuts import redirect, render
import logging

class HandleExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response


    def process_exception(self, request, exception):
        logging.error(f'Path: {request.path} Excpetion: {repr(exception)}' )
        return redirect('error page')