from django.urls import path
from . import views

urlpatterns = [
    path('pay/<int:course_id>/', views.create_order, name='create_order'),
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('payment-success/<int:course_id>/', views.payment_success, name='payment_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('login-otp/', views.send_otp_view, name='send_otp'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
]