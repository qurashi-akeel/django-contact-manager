from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name=''),
    path('register', views.register_user, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),

    path('dashboard', views.user_dashboard, name='dashboard'),
    path('create_record', views.create_record, name='create_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('view_record/<int:pk>', views.view_record, name='view_record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
]
