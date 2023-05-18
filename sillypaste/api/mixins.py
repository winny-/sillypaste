class ActionPermissionMixin(object):
    """
    Set permissions per action (falling back on permission_classes)

    To use define permission_classes_by_action:

    permission_classes_by_action = {
        'action_name': (AllowAny, ),
        ...
    }
    """

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[
                    self.action
                ]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]
