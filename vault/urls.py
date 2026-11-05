from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('upload/', views.upload_document, name='upload'),
    path('my-documents/', views.my_documents, name='my_documents'),
    path('share/', views.share_document, name='share'),

    path(
        'download/<int:document_id>/',
        views.download_document,
        name='download_document'
    ),

    path(
        'revoke/<int:permission_id>/',
        views.revoke_permission,
        name='revoke_permission'
    ),
    path(
    'shared-with-me/',
    views.shared_with_me,
    name='shared_with_me'
    ),
]