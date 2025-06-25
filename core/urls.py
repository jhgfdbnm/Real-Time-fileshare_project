from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file),
    path('download/<int:file_id>/', views.download_file),
    path('upload-form/', views.upload_form),
    path('drag-upload/', views.drag_upload),


]


