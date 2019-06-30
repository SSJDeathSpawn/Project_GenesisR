from django.shortcuts import redirect

def redirect_status(request):
    return redirect('status:index')