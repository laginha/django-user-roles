from django.http import HttpResponse
from userroles.decorators import role_required

@role_required('manager')
def home(request):
    return HttpResponse('success')
