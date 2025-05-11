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
import viewer.views as viewer

router = routers.DefaultRouter()
router.register(r'users'      , views.UserViewSet)
router.register(r'groups'     , views.GroupViewSet)
router.register(r'stls'       , StlViewSet)
router.register(r'directories', DirectoryViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/'   , admin.site.urls),
    path('api/'     , include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', views.CustomAuthToken.as_view()),
    path('api/stls/name/<str:name>/', viewer.StlByNameViewSet.as_view({'get': 'list'}), name='stl-by-name'),
    path('api/stls/dirid/<int:dirid>/', viewer.StlByParentIdViewSet.as_view({'get': 'list'}), name='stl-by-dirid'),
    path('api/directories/dirid/<int:dirid>/', viewer.DirByParentIdViewSet.as_view({'get': 'list'}), name='dir-by-dirid'),
    path('api/stl/<int:id>/', viewer.get_stl_file, name='get_stl_file'),
]

# from rest_framework.authtoken import views
# urlpatterns += [
#     path('api-token-auth2/', csrf_exempt(views.obtain_auth_token))
# ]