from django.shortcuts import redirect, get_object_or_404, render
from authentication.models import Payment

def payment_req():
    def decorators(func):
        def wrap(request, *args, **kwargs):
            user=request.user
            if Payment.objects.filter(user_id = user.id, status='True'):
                return func(request, *args, **kwargs)
            else:
                return render(request,'user_dash/index.html',{'error_message': "Pay the registration fee to add vehicles"})
        return wrap
    return decorators
