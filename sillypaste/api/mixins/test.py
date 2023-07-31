from django.test import TestCase
from . import ActionPermissionMixin
from rest_framework.permissions import IsAuthenticated
from sillypaste.api.permissions import DenyAll, ReadOnly


def make_viewset(
    *, permission_classes=None, permission_classes_by_action=None, action=None
):
    pcs = permission_classes if permission_classes is not None else []
    pcs_byaction = (
        permission_classes_by_action
        if permission_classes_by_action is not None
        else {}
    )
    act = action if action is not None else 'get'

    class MyViewSet(ActionPermissionMixin, object):
        permission_classes = pcs
        permission_classes_by_action = pcs_byaction
        action = act

    return MyViewSet()


class TestActionPermissionMixin(TestCase):
    def test_no_permission(self):
        self.assertEqual([], make_viewset().get_permissions())

    def test_permission_classes(self):
        pcs = [DenyAll, ReadOnly, IsAuthenticated]
        perms = make_viewset(permission_classes=pcs).get_permissions()
        for klass, instance in zip(pcs, perms):
            self.assertIsInstance(instance, klass)

    def test_permission_by_action(self):
        pcs = [DenyAll, ReadOnly, IsAuthenticated]
        vs = make_viewset(
            permission_classes_by_action={'get': pcs}, action='get'
        )
        perms = vs.get_permissions()
        for klass, instance in zip(pcs, perms):
            self.assertIsInstance(instance, klass)
