"""
Custom conversion logic that is intended to be used in both new user
creation, and merging lazy users with existing users (on login).
"""


from lazysignup.utils import is_lazy_user


__all__ = ['convert']


def convert(old_user, new_user):
    """Helper to convert a lazy into a full user."""
    if is_lazy_user(old_user):
        for p in old_user.paste_set.all():
            p.author = new_user
            p.save()
