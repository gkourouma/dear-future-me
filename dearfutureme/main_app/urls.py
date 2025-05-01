from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('capsules/', views.capsule_page, name='capsules'),
    path('capsule/create/', views.capsule_create, name='capsule_create'),
    path('capsule/<int:capsule_id>/', views.capsule_detail, name='capsule_detail'),
    path('capsules/<int:capsule_id>/add-memory/', views.add_memory, name='memory_form'),
    path('memories/<int:memory_id>/', views.memory_detail, name='memory_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)