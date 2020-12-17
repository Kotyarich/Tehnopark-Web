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
from django.views.decorators.csrf import csrf_exempt

from askme import settings
from questions import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', csrf_exempt(views.QuestionsList.as_view()), name='new_questions'),
    path('hot/', csrf_exempt(views.HotQuestionsList.as_view()), name='hot'),
    path('login/', csrf_exempt(views.LoginView.as_view()), name='login'),
    path('logout/', csrf_exempt(views.LogoutView.as_view()), name='logout'),
    path('signup/', csrf_exempt(views.RegisterView.as_view()), name='signup'),
    path('ask/', csrf_exempt(views.AskView.as_view()), name='ask'),
    path('settings/', csrf_exempt(views.SettingsView.as_view()), name='settings'),
    path('question/<int:id>/', csrf_exempt(views.QuestionView.as_view()), name='question'),
    path('tag/<str:tag>', csrf_exempt(views.TaggedQuestionsList.as_view()), name='tag'),
    path('like/', csrf_exempt(views.LikeView.as_view()), name='like'),
    path('like_answer/', csrf_exempt(views.LikeAnswerView.as_view()), name='like_answer'),
    path('search/', csrf_exempt(views.SearchView.as_view()), name='search')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
