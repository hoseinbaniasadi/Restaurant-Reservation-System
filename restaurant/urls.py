from django.urls import path

from . import views

urlpatterns = [
    path('', views.TableList.as_view(), name='table_list'),
    path('<int:pk>/', views.reserve_table, name='reserve_table'),
]