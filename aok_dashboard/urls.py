from django.urls import path
from . import views

urlpatterns = [
    # path("/", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),  
    path("dashboard/", views.dashboard, name="dashboard"),
    path('business-profile/', views.business_profile, name='business_profile'),
    path('add-menu-item/', views.add_menu_item, name='add_menu_item'),
    path('change-password/', views.change_password, name='change_password'),
    path('get-items/', views.get_items_by_category, name='get_items_by_category'), 
    path('business-hours/', views.manage_business_hours, name='manage_business_hours'),
    path('balance/', views.admin_balance_dashboard, name='admin_balance_dashboard'),  
] 
