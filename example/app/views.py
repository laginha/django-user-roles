from django.http import HttpResponse
from userroles.decorators import role_required
from userroles import roles

@role_required('manager')
def home(request):
    return HttpResponse('success')
    
@role_required(roles.manager, roles.moderator)
def manager_or_moderator(request):
    return HttpResponse('success')
