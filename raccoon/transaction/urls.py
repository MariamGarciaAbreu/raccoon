from django.urls import path
from . import views

urlpatterns = [
    path('hello-world/', views.hello_world, name='hello_world'),
    path('create-transaction/', views.add_transaction, name='add-transaction'),
    path('view-transactions/', views.view_transactions, name='view-transactions'),
    path('view-transaction/<int:pk>/', views.view_transaction, name='view-transaction'),
    path('view/category/', views.view_category, name='view-category-all'),
    path('update-transaction/<int:pk>/', views.update_transaction, name='update-transaction'),
    path('delete-transaction/<int:pk>/', views.delete_transaction, name='delete-transaction'),
]
