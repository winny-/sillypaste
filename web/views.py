from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_http_methods
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
from django.db.models import Sum, Count

from web.forms import PasteForm
from core.models import Paste, ExpiryLog


@require_GET
def index(request):
    return render(request, 'index.html', {
        'recent': Paste.objects.order_by('-timestamp')[:20],
        'top': Paste.objects.filter(hits__gt=0).order_by('-hits')[:5],
    })


@require_GET
def all_pastes(request):
    return render(request, 'all_pastes.html', {
        'pastes': Paste.objects.order_by('-timestamp'),
    })


@require_GET
def show_paste(request, paste_id):
    p = get_object_or_404(Paste, pk=paste_id)
    return render(request, 'show_paste.html', {'paste':p.view()})


@require_GET
def show_raw(request, paste_id):
    p = get_object_or_404(Paste, pk=paste_id)
    p.view()
    return HttpResponse(p.body, content_type='text/plain; charset=utf-8')


@require_http_methods(['GET', 'POST'])
def make_paste(request):
    if request.method == 'POST':
        form = PasteForm(request.POST)
        if form.is_valid():
            try:
                p = Paste.objects.get(body=form.cleaned_data['body'])
            except ObjectDoesNotExist:
                p = form.save()
            return HttpResponseRedirect(reverse(
                'show_paste',
                kwargs={'paste_id':p.id},
            ))
    else:
        form = PasteForm()

    return render(request, 'make_paste.html', {
        'form': form,
        'error_message': '; '.join(f"{what}: {','.join(messages)}"
                                   for (what, messages)
                                   in form.errors.items()),
    })


@require_GET
def show_site_stats(request):
    return render(request, 'show_site_stats.html', {
        'total_pastes_count': Paste.objects.count(),
        'total_pastes_size': Paste.objects.aggregate(total=Sum('size'))['total'],
        'last_expiry_log': ExpiryLog.objects.last(),
        'total_reclaimed_count': ExpiryLog.objects.aggregate(x=Count('count'))['x'],
        'total_reclaimed_space': ExpiryLog.objects.aggregate(x=Sum('reclaimed_space'))['x'],
    })
