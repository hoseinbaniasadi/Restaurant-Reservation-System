from django.urls import path

from . import views

urlpatterns = [
    path('', views.TableList.as_view(), name='table_list'),
    path('<int:pk>/', views.reserve_table, name='reserve_table'),
    path('review/<int:pk>/', views.table_review, name='review'),
    path('reservation/<int:reservation_id>/create_payment/', views.create_payment, name='create_payment'),
    path('callback/', views.verify_payment, name='verify_payment'),
]