from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from v1.app_store.urls import router as app_store_router
from v1.authentication.views.login import LoginView
from v1.feedback.urls import router as feedback_router
from v1.openings.urls import router as openings_router
from v1.projects.urls import router as projects_router
from v1.repositories.urls import router as repositories_router
from v1.roadmap.urls import router as roadmap_router
from v1.tasks.urls import router as tasks_router
from v1.teams.urls import router as teams_router
from v1.trusted_banks.urls import router as trusted_banks_router
from v1.users.urls import router as users_router
from v1.users.views.user import UserViewSet
from v1.videos.urls import router as videos_router


admin.site.index_title = 'Admin'
admin.site.site_header = 'thenewboston'
admin.site.site_title = 'thenewboston'

verify_user = UserViewSet.as_view({
    'get': 'verify'
})
generate_new_link = UserViewSet.as_view({
    'post': 'generate_new_link'
})

urlpatterns = [

    # Core
    path('admin/', admin.site.urls),

    # Auth
    path('login', LoginView.as_view(), name='login'),
    path('refresh_token', TokenRefreshView.as_view(), name='refresh_token'),
    path('users/verify/<uid>/<token>', verify_user, name='verify_user'),
    path('users/new-link', generate_new_link, name='generate_new_link'),

    # OpenAPI Schema UI
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

router = DefaultRouter(trailing_slash=False)

router.registry.extend(openings_router.registry)
router.registry.extend(tasks_router.registry)
router.registry.extend(teams_router.registry)
router.registry.extend(repositories_router.registry)
router.registry.extend(users_router.registry)
router.registry.extend(videos_router.registry)
router.registry.extend(projects_router.registry)
router.registry.extend(feedback_router.registry)
router.registry.extend(roadmap_router.registry)
router.registry.extend(app_store_router.registry)
router.registry.extend(trusted_banks_router.registry)

urlpatterns += router.urls

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
