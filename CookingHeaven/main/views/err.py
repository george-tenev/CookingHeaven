from django.shortcuts import render


def internal_error(request):
    return render(request, 'err/500.html')


def bad_request(request):
    return render(request, 'err/400.html')
