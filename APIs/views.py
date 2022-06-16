from rest_framework import viewsets, status, filters
from rest_framework.views import APIView
from .models import Image, Order, Product, Review, User
from .serializers import CUDProductSerializer, OrderSerializer, ProductSerializer, ReviewSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


#user viewsets with CRUD operations
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        elif self.action == "update" or self.action == "partial_update":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


#Create Update Delete Products
class CUDProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = CUDProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images', None)
        _serializer = self.serializer_class(data=request.data)
        if _serializer.is_valid():
            _serializer.save()
            product=Product.objects.latest('id')
            for img in images:
                Image.objects.create(image=img,product=product)
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)  # NOQA
        return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        return Response({'error': "GET Metheod does not support on this api"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def retrieve(self, request, pk=None):
        return Response({'error': "GET Metheod does not support on this api"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



#Get all products with details
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'discription']

    def create(self, request):
        return Response({'error': "POST Metheod does not support on this api"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response({'error': "PUT Metheod does not support on this api"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({'error': "PUT Metheod does not support on this api"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response({'error': "DELETE Metheod does not support on this api"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


#CRUD Review
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#logout by changing token
class LogoutView(APIView):
    def post(self, request):
        if 'token' in request.data and 'username' in request.data:
            token = request.data['token']
            user = User.objects.get(username=str(request.data['username']))
            user_token = Token.objects.get(user=user)
            if user_token.key == token:
                user_token.delete()
                Token.objects.create(user=user)
                return Response({"message": "Logedout successfully"}, status=status.HTTP_201_CREATED)
        return Response({"error":"invalid data"}, status=status.HTTP_400_BAD_REQUEST)

