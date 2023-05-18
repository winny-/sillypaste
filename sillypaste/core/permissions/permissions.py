"""
Permissions for core objects.
"""


__all__ = ['user_can_edit_paste', 'admin_can_edit_paste', 'admin_using_powers']


def user_can_edit_paste(user, paste):
    """Can user edit pastes?

    - They are owner
    - They are admin with appropriate permissions."""
    return (
        paste.author is not None and paste.author == user
    ) or admin_can_edit_paste(user, paste)


def admin_can_edit_paste(user, paste):
    """Can the user using admin permission to edit the paste?"""
    return user.has_perm('core.change_paste') and user.has_perm(
        'core.delete_paste'
    )


def admin_using_powers(user, paste):
    """Is the admin using their permissions to edit this paste?"""
    return (
        paste.author is None or paste.author != user
    ) and admin_can_edit_paste(user, paste)
