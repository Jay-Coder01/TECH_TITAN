from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('scholarships/', views.scholarships, name='scholarships'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('forum/', views.forum, name='forum'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('refresh-recommendations/', views.refresh_recommendations, name='refresh_recommendations'),
    path('api/scholarships/', views.api_scholarships, name='api_scholarships'),

]