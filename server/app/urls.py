"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]


from django.urls import include, path
from rest_framework import routers

from app          import views
from viewer.views import DirectoryViewSet,StlViewSet

router = routers.DefaultRouter()
router.register(r'users'      , views.UserViewSet)
router.register(r'groups'     , views.GroupViewSet)
router.register(r'stls'       , DirectoryViewSet)
router.register(r'directories', StlViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/'   , admin.site.urls),
    path('api/'     , include(router.urls)),
    # path('api-auth/', csrf_exempt(include('rest_framework.urls', namespace='rest_framework'))),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('csrf-token/', views.csrf_token, name='csrf_token'),
    path('api-token-auth/', views.CustomAuthToken.as_view()),
]

# from rest_framework.authtoken import views
# urlpatterns += [
#     path('api-token-auth2/', csrf_exempt(views.obtain_auth_token))
# ]