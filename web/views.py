from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_http_methods
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
from django.db.models import Sum, Count
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.core.exceptions import PermissionDenied
from pygments import lexers, highlight
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound
from pygments.formatters import HtmlFormatter

from web.forms import PasteForm
from core.models import Paste, ExpiryLog


class Register(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'registration/register.html'

    # Via https://stackoverflow.com/questions/3222549/
    def form_valid(self, form):
        response = super().form_valid(form)
        new_user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        login(self.request, new_user)
        return response


class AuthorAccessingPasteViewMixin:
    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.author == self.request.user:
            raise PermissionDenied()
        return obj


class PasteDelete(AuthorAccessingPasteViewMixin, generic.DeleteView):
    model = Paste
    success_url = reverse_lazy('index')
    template_name = 'paste_confirm_delete.html'


class PasteUpdate(AuthorAccessingPasteViewMixin, generic.UpdateView):
    form_class = PasteForm
    model = Paste
    template_name = 'paste_update.html'

class PrivacyPolicy(generic.TemplateView):
    template_name = 'privacy_policy.html'

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
    formatter = HtmlFormatter()
    try:
        body_html = highlight(
            p.body,
            lexers.find_lexer_class_by_name(p.language.name)(),
            formatter,
        )
    except (ClassNotFound, AttributeError):
        body_html = highlight(
            p.body,
            TextLexer(),
            formatter
        )
    return render(request, 'show_paste.html', {
        'paste': p.view(),
        'paste_body_html': body_html,
        'owner': p.author is not None and p.author == request.user,
    })


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
            p = form.save()
            if request.user.is_authenticated:
                p.author = request.user
                p.save()
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


class ListPastes(generic.ListView):
    model = Paste
    template_name = 'paste_list.html'


class ListMyPastes(LoginRequiredMixin, ListPastes):
    def get_queryset(self):
        return Paste.objects.filter(author=self.request.user)



@require_GET
def show_site_stats(request):
    return render(request, 'show_site_stats.html', {
        'total_pastes_count': Paste.objects.count(),
        'total_pastes_size': Paste.objects.aggregate(total=Sum('size'))['total'],
        'last_expiry_log': ExpiryLog.objects.last(),
        'total_reclaimed_count': ExpiryLog.objects.aggregate(x=Count('count'))['x'],
        'total_reclaimed_space': ExpiryLog.objects.aggregate(x=Sum('reclaimed_space'))['x'],
    })
