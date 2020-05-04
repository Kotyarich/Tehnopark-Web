"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

from askme import settings
from questions import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='new_questions'),
    path('hot/', views.hot, name='hot'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.register, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('settings/', views.settings, name='settings'),
    path('question/<int:id>/', views.question, name='question'),
    path('tag/<str:tag>', views.tag, name='tag'),
    path('like/', views.like, name='like'),
    path('search/', views.search, name='search')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
