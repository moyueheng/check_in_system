"""check_in_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path
from . import views

app_name = 'check_in'

urlpatterns = [
    re_path('face_identify', view=views.FaceIdentifyView.as_view(), name='face_identify'),
    re_path('mask_det', view=views.MaskDetView.as_view(), name='face_identify'),
    re_path('students', view=views.StudentsView.as_view(), name='students'),
]
