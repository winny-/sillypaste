"""
Views that deal with Pastes.
"""


from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_GET, require_http_methods

from pygments import lexers, highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

from core.permissions import user_can_edit_paste, admin_using_powers
from core.models import Paste
from core.lazysignup import allow_lazy_user
from web.forms import PasteForm


__all__ = ['PasteDelete', 'PasteUpdate', 'show_paste', 'show_raw', 'make_paste', 'ListPastes']


class AuthorAccessingPasteViewMixin:
    """Prevent non-owners or non-admins from modifying pastes that are not theirs."""
    def get_object(self, queryset=None):
        obj = super().get_object()
        if not user_can_edit_paste(self.request.user, obj):
            raise PermissionDenied()
        return obj


class PasteDelete(AuthorAccessingPasteViewMixin, generic.DeleteView):
    """Delete Paste confirmation page."""
    model = Paste
    success_url = reverse_lazy('index')
    template_name = 'paste_confirm_delete.html'


class PasteUpdate(AuthorAccessingPasteViewMixin, generic.UpdateView):
    """Update an existing Paste."""
    form_class = PasteForm
    model = Paste
    template_name = 'paste_update.html'


@require_GET
def show_paste(request, paste_id):
    """View a Paste with links to delete or edit if you're the appropriate user."""
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
        'can_edit': user_can_edit_paste(request.user, p),
        'is_admin': admin_using_powers(request.user, p),
    })


@require_GET
def show_raw(request, paste_id):
    """Get the raw contents of the Paste."""
    p = get_object_or_404(Paste, pk=paste_id)
    p.view()
    return HttpResponse(p.body, content_type='text/plain; charset=utf-8')


@allow_lazy_user
@require_http_methods(['GET', 'POST'])
def make_paste(request):
    """Create a new Paste."""
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
    })


class ListPastes(generic.ListView):
    """List all pastes on the site."""
    model = Paste
    context_object_name = 'pastes'
    paginate_by = 30
    template_name = 'paste_list.html'

    def get_queryset(self):
        return Paste.objects.filter_fulltext(self.request.GET.get('q'))

