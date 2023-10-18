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
    path('filterwords/', views.filterwords_list, name='filterwords_read'), #GET for filterwords READ
    path('filterwords/<int:clientid>/', views.filterwords_list, name='filterwords_read_id'), #GET for filterwords READ
    path('filterwords/insert/<int:clientid>/', views.filterwords_insert, name='filterwords_insert'), # GET & POST for filterwords INSERT
    path('filterwords/update/<int:filterword_id>/', views.filterwords_update, name='filterwords_update'),# GET & POST for filterwords UPDATE
    path('filterwords/delete/<int:id>/', views.filterwords_delete, name='filterwords_delete'), # GET & POST for filterwords DELETE

    #NOTIFICATIONS
    path('notifications/', views.notifications_list, name='notifications_read'), #GET for notifications READ
    path('notifications/<int:clientid>/', views.notifications_list, name='notifications_read_id'), #GET for notifications READ
    path('notifications/insert/<int:clientid>/', views.notifications_insert, name='notifications_insert'), # GET & POST for notifications INSERT
    path('notifications/update/<int:notification_id>/', views.notifications_update, name='notifications_update'),  # GET & POST for notifications UPDATE
    path('notifications/delete/<int:id>/', views.notifications_delete, name='notifications_delete'),# GET & POST for notifications DELETE

    #ARTICLES
    path('articles/', views.articles_list, name='articles_read'), #GET for articles READ
    path('articles/search/', views.search_articles, name='search_articles'), #GET for articles READ based on clients ID
]