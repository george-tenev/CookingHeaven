from django.shortcuts import redirect, render


def handle_exception(get_response):
    def middleware(request):
        response = get_response(request)
        if response.status_code >= 500:
            return redirect('500')
        if response.status_code >= 400:
            return redirect('400')
        return response

    return middleware
