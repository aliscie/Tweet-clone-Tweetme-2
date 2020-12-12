"""vertualizor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from social.views import (home_view,
                          post_view,
                          posts_list_view,
                          post_create_view,
                          post_delete_view,
                          post_actions_view)

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from accounts.views import (
    login_view,
    logout_view,
    register_view,
)
urlpatterns = [
    path('posts/<int:postId>', post_view),  # dyanmic url
    path('create/', post_create_view),
    path('', home_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view),
    path('react/', TemplateView.as_view(template_name='react_via_dj.html')),
    path('admin/', admin.site.urls),
    # http://localhost:8000/posts/accounts/login/ don't work.
    path('accounts/', include('allauth.urls')),
    path('posts/', include("social.urls")),
    re_path(r'profiles?/', include('profiles.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
