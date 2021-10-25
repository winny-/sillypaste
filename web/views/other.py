"""
Views that do not belong in the other files.
"""


from lazysignup.models import LazyUser
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count
from django.shortcuts import render
from django.views import generic
from django.views.decorators.http import require_GET


from core.models import Paste, ExpiryLog


__all__ = ['PrivacyPolicy', 'index', 'show_site_stats']


class PrivacyPolicy(generic.TemplateView):
    """Privacy policy link at bottom of page."""

    template_name = 'privacy_policy.html'


@require_GET
def index(request):
    """Homepage."""
    return render(
        request,
        'index.html',
        {
            'recent': Paste.objects.order_by('-timestamp')[:20],
            'top': Paste.objects.filter(hits__gt=0).order_by('-hits')[:5],
        },
    )


@require_GET
def show_site_stats(request):
    """Statistics about site usage."""
    lazy_user_count = LazyUser.objects.all().count()
    return render(
        request,
        'show_site_stats.html',
        {
            'total_pastes_count': Paste.objects.count(),
            'total_pastes_size': Paste.objects.aggregate(total=Sum('size'))[
                'total'
            ],
            'last_expiry_log': ExpiryLog.objects.last(),
            'total_reclaimed_count': ExpiryLog.objects.aggregate(
                x=Count('paste_count')
            )['x'],
            'total_reclaimed_space': ExpiryLog.objects.aggregate(
                x=Sum('reclaimed_space')
            )['x'],
            'total_pruned_user_count': ExpiryLog.objects.aggregate(
                x=Sum('user_count')
            )['x'],
            'total_anonymous_user_count': lazy_user_count,
            'total_registered_user_count': get_user_model()
            .objects.all()
            .count()
            - lazy_user_count,
            'total_user_count': get_user_model().objects.all().count(),
        },
    )
