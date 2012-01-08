from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.views import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from contenteditable.utils import content_update_from_dict, content_delete
from newspaper.models import Article

from contenteditablesettings import CONTENTEDITABLE_MODELS


@csrf_exempt
@require_POST
#@login_required        ### UNCOMMENT THIS!
def update_view(request):
    model = request.POST.get('model')
    if CONTENTEDITABLE_MODELS.get(model) is not None:
        e_conf = CONTENTEDITABLE_MODELS[model]
        if content_update_from_dict(e_conf[0], request.POST, e_conf[1]):
            return HttpResponse('ok')
        else:
            return HttpResponseServerError('Content cannot be updated')
    else:
        raise ValueError('Unknown model: {0}'.format(request.POST.get('model')))


@csrf_exempt
@require_POST
#@login_required        ### UNCOMMENT THIS!
def delete_view(request):
    model = request.POST.get('model')
    if CONTENTEDITABLE_MODELS.get(model) is not None: 
        content_delete(CONTENTEDITABLE_MODELS[model][0], pk=request.POST.get('id'))
        return HttpResponse('ok')
    else:
        raise ValueError('Unknown model: {0}'.format(request.POST.get('model')))

