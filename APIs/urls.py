from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

#create custom response with auth token
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'is_admin': user.is_staff,
        })

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('products', views.ProductViewSet)
router.register('cudproducts', views.CUDProductViewSet)
router.register('reviews', views.ReviewViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('api-auth', include('rest_framework.urls')),
    path('api-token-auth', CustomAuthToken.as_view()),
    path('logout', views.LogoutView.as_view()),
]
