from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet


class CachedModelViewSet(ModelViewSet):
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(settings.CACHE_TTL))
    def dispatch(self, *args, **kwargs):
        return super(CachedModelViewSet, self).dispatch(*args, **kwargs)


class CachedGenericViewSet(ListModelMixin, GenericViewSet):
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(settings.CACHE_TTL))
    def dispatch(self, *args, **kwargs):
        return super(CachedGenericViewSet, self).dispatch(*args, **kwargs)
