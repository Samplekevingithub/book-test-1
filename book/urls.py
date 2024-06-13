from django.urls import path, include
from book import views
urlpatterns = [
    path('', views.index, name='index'), 
    path('register/', views.Registers, name='register'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('rental/', views.rental, name='rental'),
    path('rental/<str:title>/', views.rental, name='rental'),
    path('checkout/', views.checkout, name='checkout'),
    path('search_book/', views.search_book, name='search_book'),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('success/', views.success, name='success'),
    path('latest-books/', views.latest_books, name='latest_books'),
    path('delete_book/', views.delete_book, name='delete_book'),
]
