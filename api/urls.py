"""Library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from api.views import *
# from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token
from rest_framework_nested import routers

router = routers.SimpleRouter()

router.register(r'users', UserViewSet, base_name='user')
router.register(r'books', BookViewSet)
router.register(r'barcode', BarCodeViewSet)
router.register(r'borrowinfos', BorrowInfoViewSet)
router.register("book/search", BookSearchViewSet, base_name='book-search')
user_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
user_router.register(r'borrowinfos', UserBorrowInfo)
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(user_router.urls)),
    url(r'^api-token-refresh', refresh_jwt_token, name='refresh-token'),
    url(r'^api-token-verify', verify_jwt_token, name='verify-token'),
    # url(r'^books', views.BookViewSet)
]
# urlpatterns += router.urls
