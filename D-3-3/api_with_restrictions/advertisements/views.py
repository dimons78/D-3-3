from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from django_filters.rest_framework import DjangoFilterBackend
from advertisements.filters import AdvertisementFilter
from advertisements.permissions import AccessPermission


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()

    serializer_class = AdvertisementSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_class = AdvertisementFilter

    def list(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            self.queryset = Advertisement.objects.filter(~Q(status="DRAFT"))
        elif request.user.is_superuser:
            self.queryset = Advertisement.objects.all()
        else:
            self.queryset = Advertisement.objects.filter(~Q(status="DRAFT") | Q(creator=request.user))

        return super().list(self, request, *args, **kwargs)


    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ["create"]:
            permissions = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            permissions = [AccessPermission]
        else:
            permissions = []

        return [permission() for permission in permissions]


