from django.urls import path

from .views import UploadView

urlpatterns = [
    path('upload/image/', UploadView.as_view({'post': 'upload_image'})),
]
