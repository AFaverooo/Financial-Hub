from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('', views.getRoutes),
    path('firstname/', views.getFirstName),
    path('token/', MyTokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('investment_categories/', views.investment_categories, name='investment_categories'),
    path('investment_category_breakdown/', views.investment_category_breakdown, name='investment_category_breakdown'),
    path('exchange_public_token/', views.exchange_public_token, name='exchange_public_token'),
    path('cache_assets/', views.cache_assets),
    path('api/get_balances_data/', views.get_balances_data, name='get_balances_data'),
    path('api/select_account/', views.select_account, name='select_account'),
]
