from rest_framework import viewsets, status
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response



# api with viewsets
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

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

