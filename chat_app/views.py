from django.shortcuts import render


def socket_call(request):
    return render(request, 'index.html')
