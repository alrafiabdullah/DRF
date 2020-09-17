from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/v1/products', views.ProductList.as_view()),
    path("api/v1/products/new", views.ProductCreate.as_view()),
    path("api/v1/products/<int:id>/update",
         views.ProductUpdateDestroy.as_view())
]
