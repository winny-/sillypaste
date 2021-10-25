from rest_framework import viewsets
from core.models import Paste, ExpiryLog, Language
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    PasteSerializer,
    ExpiryLogSerializer,
    LanguageSerializer,
)
from .permissions import ReadOnly, IsSameUser, IsOwnerOrReadOnly, DenyAll
from .mixins import ActionPermissionMixin
from rest_framework.permissions import IsAuthenticated


class UserViewSet(ActionPermissionMixin, viewsets.ModelViewSet):
    # Via https://stackoverflow.com/a/35987077/2720026
    permission_classes_by_action = {
        'retrieve': (IsAuthenticated,),
        'create': (DenyAll,),
        'update': (IsSameUser,),
        'me': (IsAuthenticated,),
    }
    permission_classes = (DenyAll,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        # See https://stackoverflow.com/questions/51149599/
        if request.method == 'GET':
            view = UserViewSet.as_view({'get': 'retrieve'})
            return view(request._request, pk=request.user.id)
        elif request.method == 'PUT':
            view = UserViewSet.as_view({'put': 'update'})
            return view(request._request, pk=request.user.id)
        assert False, 'Should not reach'


class PasteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PasteSerializer
    queryset = Paste.objects.all()

    def get_queryset(self):
        return Paste.objects.filter_fulltext(
            self.request.query_params.get('q')
        )


class LanguageViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class ExpiryLogViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = ExpiryLog.objects.all()
    serializer_class = ExpiryLogSerializer


@api_view(['POST'])
def logout(request):
    request.auth.delete()
    return Response({'logged_out': True})
