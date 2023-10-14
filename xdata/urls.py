from django.urls import path, include
from .import views
urlpatterns = [
    #HOME
    path('', views.home, name='home'),
    #CLIENTS
    path('clients/', views.clients_form, name='clients_insert'), #GET & POST for clients INSERT
    path('clients/<int:id>/', views.clients_form, name='clients_update'), #GET & POST for clients UPDATE
    path('clients/delete/<int:id>/', views.clients_delete, name='clients_delete'), #POST for clients DELETE
    path('clients/list/', views.clients_list, name='clients_read'), #GET for clients READ

    #FILTERWORDS

    #NOTIFICATIONS

    #ARTICLES
    path('articles/', views.articles_list, name='articles_read'), #GET for articles READ
    path('articles/search/', views.search_articles, name='search_articles'), #GET for articles READ based on clients ID
]