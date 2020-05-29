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
from django.urls import path

from askme import settings
from questions import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.QuestionsList.as_view(), name='new_questions'),
    path('hot/', views.HotQuestionsList.as_view(), name='hot'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('ask/', views.AskView.as_view(), name='ask'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('question/<int:id>/', views.QuestionView.as_view(), name='question'),
    path('tag/<str:tag>', views.TaggedQuestionsList.as_view(), name='tag'),
    path('like/', views.LikeView.as_view(), name='like'),
    path('search/', views.SearchView.as_view(), name='search')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
