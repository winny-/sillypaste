"""
Views that deal with Pastes.
"""


from django.core.exceptions import PermissionDenied, ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_GET, require_http_methods
from django.db.models import Q

from pygments import lexers, highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

import markdown
import orgpython

from sillypaste.core.permissions import user_can_edit_paste, admin_using_powers
from sillypaste.core.validators import validate_paste_sort_key
from sillypaste.core.models import Paste
from sillypaste.core.lazysignup import allow_lazy_user
from sillypaste.web.forms import PasteForm


__all__ = [
    'PasteDelete',
    'PasteUpdate',
    'show_paste',
    'render_paste',
    'show_raw',
    'make_paste',
    'ListPastes',
]


class AuthorAccessingPasteViewMixin:
    """Prevent non-owners or non-admins from modifying pastes that are not
    theirs."""

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
    """View a Paste with links to delete or edit if you're the appropriate
    user."""
    p = get_object_or_404(Paste, pk=paste_id)
    formatter = HtmlFormatter()
    try:
        body_html = highlight(
            p.body,
            lexers.find_lexer_class_by_name(p.language.name)(),
            formatter,
        )
    except (ClassNotFound, AttributeError):
        body_html = highlight(p.body, TextLexer(), formatter)
    return render(
        request,
        'show_paste.html',
        {
            'paste': p.view(),
            'paste_body_html': body_html,
            'can_edit': user_can_edit_paste(request.user, p),
            'is_admin': admin_using_powers(request.user, p),
            'rendered': False,
        },
    )


@require_GET
def render_paste(request, paste_id):
    """Render a Paste or redirect to the Paste's canonical address if not
    render-able."""
    p = get_object_or_404(Paste, pk=paste_id)
    if hasattr(p, 'language'):
        html = None
        if p.language.name == 'markdown':
            html = markdown.markdown(p.body)
        elif p.language.name == 'org-mode':
            html = orgpython.to_html(p.body)
        if html:
            return render(
                request,
                'show_paste.html',
                {
                    'paste': p.view(),
                    'paste_body_html': html,
                    'can_edit': user_can_edit_paste(request.user, p),
                    'is_admin': admin_using_powers(request.user, p),
                    'rendered': True,
                },
            )
    # Redirect to the canonical URL if it's not render-able.
    return redirect(p)


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
            return redirect(p)
    else:
        form = PasteForm()

    return render(request, 'make_paste.html', {'form': form})


class ListPastes(generic.ListView):
    """List all pastes on the site."""

    model = Paste
    context_object_name = 'pastes'
    paginate_by = 30
    template_name = 'paste_list.html'

    def get(self, *args, **kwargs):
        """Clean URL parameter 'sort'.

        When sort parameter is found invalid, just strip it out and set a
        default sort parameter instead.
        """
        try:
            validate_paste_sort_key(self.request.GET.get('sort') or 'id')
        except ValidationError:
            get = self.request.GET.copy()
            del get['sort']
            params = get.urlencode()
            return redirect(
                self.request.path + ('?' + params if params else '')
            )
        return super().get(*args, **kwargs)

    def get_ordering(self):
        sort_key = self.request.GET.get('sort', 'id')
        if sort_key.lstrip('-') not in (
            f.name for f in Paste._meta.get_fields()
        ):
            sort_key = 'id'  # Prevent sorting by bad input.
        return sort_key

    def get_queryset(self):
        objs = Paste.objects.filter_fulltext(self.request.GET.get('q'))

        # TODO Reevaluate if staff should be able to all pastes regardless of
        # privacy.  The Django Admin app can be used to administrate pastes
        # outside of this webapp.
        if (
            self.request.user.is_authenticated
            and not self.request.user.is_staff
        ):
            filter_author = Q(author=self.request.user)
            objs = objs.filter(Q(private=False) | filter_author)

        return objs.order_by(self.get_ordering())
