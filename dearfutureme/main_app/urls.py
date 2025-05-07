from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<int:profile_id>/delete/', views.profile_delete, name='profile_delete'),
    path("search/", views.search_user, name="search_user"),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('capsules/', views.capsule_page, name='capsules'),
    path('capsule/create/', views.capsule_create, name='capsule_create'),
    path('capsule/<int:capsule_id>/delete/', views.capsule_delete, name='capsule_delete'),
    path('capsule/<int:capsule_id>/edit/', views.capsule_edit, name='capsule_edit'),
    path('capsule/<int:capsule_id>/', views.capsule_detail, name='capsule_detail'),
    path('users/<int:user_id>/albums/', views.user_capsules, name='user_capsules'),
    path('capsules/<int:capsule_id>/add-memory/', views.add_memory, name='memory_form'),
    path('memories/<int:memory_id>/', views.memory_detail, name='memory_detail'),
    path('memories/<int:memory_id>/delete/', views.memory_delete, name='memory_delete'),
    path('memories/<int:memory_id>/edit/', views.memory_edit, name='memory_edit'),
    path('memory/<int:memory_id>/like/', views.like_memory, name='like_memory'),
    path('memory/<int:memory_id>/comment/', views.add_comment, name='add_comment'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)