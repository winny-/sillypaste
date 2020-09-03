from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_http_methods
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from core.models import Paste

@require_GET
def index(request):
    return render(request, 'index.html', {'recent': Paste.objects.order_by('-timestamp')[:20]})

@require_GET
def all_pastes(request):
    return render(request, 'all_pastes.html', {'pastes': Paste.objects.order_by('-timestamp')})

@require_GET
def show_paste(request, paste_id):
    p = get_object_or_404(Paste, pk=paste_id)
    return render(request, 'show_paste.html', {'paste':p})

@require_GET
def show_raw(request, paste_id):
    p = get_object_or_404(Paste, pk=paste_id)
    return HttpResponse(p.body, content_type='text/plain')

@require_http_methods(['GET', 'POST'])
def make_paste(request):
    if request.method == 'POST':
        try:
            title, body = request.POST['title'].strip(), request.POST['body']
        except KeyError:
            return render(request, 'make_paste.html', {'error_message': 'Invalid submission'})
        else:
            if not title or not body:
                return render(request, 'make_paste.html', {'error_message': 'Empty field(s)'})
            exists = Paste.objects.filter(body=body)
            if exists:
                return HttpResponseRedirect(reverse(
                    'show_paste',
                    kwargs={'paste_id':exists.first().id},
                ))
            p = Paste(title=title, body=body)
            p.save()
            return HttpResponseRedirect(reverse(
                'show_paste',
                kwargs={'paste_id':p.id},
            ))
    else:
        return render(request, 'make_paste.html')
