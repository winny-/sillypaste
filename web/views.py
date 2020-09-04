from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_http_methods
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

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
    return HttpResponse(p.body, content_type='text/plain; charset=utf-8')

@require_http_methods(['GET', 'POST'])
def make_paste(request):
    if request.method == 'POST':
        try:
            title = request.POST['title'].strip()
            body = request.POST['body']
            expiry = request.POST.get('expiry', '1day').strip()
        except KeyError:
            return render(request, 'make_paste.html', {'error_message': 'Invalid submission'})
        else:
            if not title or not body:
                return render(request, 'make_paste.html', {'error_message': 'Empty field(s)'})
            if expiry not in ('never', '1day', ):
                return render(request, 'make_paste.html', {'error_message': 'Bad expiry value'})
            exists = Paste.objects.filter(body=body)
            if exists:
                return HttpResponseRedirect(reverse(
                    'show_paste',
                    kwargs={'paste_id':exists.first().id},
                ))
            expiry_time = None
            if expiry == '1day':
                expiry_time = timezone.now() + timedelta(days=1)
            p = Paste(title=title, body=body, expiry=expiry_time)
            p.save()
            return HttpResponseRedirect(reverse(
                'show_paste',
                kwargs={'paste_id':p.id},
            ))
    else:
        return render(request, 'make_paste.html')
