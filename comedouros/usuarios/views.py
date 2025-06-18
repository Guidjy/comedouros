from rest_framework import viewsets, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User
from .serializers import UserSerializer, RegisterUserSerializer, ChangePasswordSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def todos_usuarios(request):
    """
    Retorna todos os usuários criads
    """
    usuarios = User.objects.all()
    serializer = UserSerializer(usuarios, many=True)
    
    return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    | Metodo | Endpoint          | Ação           |
    | ------ | ----------------- | -------------- |
    | GET    | `/usuarios/`      | List users     |
    | POST   | `/usuarios/`      | Create user    |
    | GET    | `/usuarios/{id}/` | Retrieve user  |
    | PUT    | `/usuarios/{id}/` | Full update    |
    | PATCH  | `/usuarios/{id}/` | Partial update |
    | DELETE | `/usuarios/{id}/` | Delete user    |
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]
    

class ChangePasswordView(APIView):
    """
    perimte mudar a senha do usuário autenticado
    {
    "old_password": "your_current_password",
    "new_password": "your_new_password"
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data.get('old_password')):
                return Response({'old_password': 'Wrong password.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data.get('new_password'))
            user.save()

            return Response({'status': 'Password changed successfully.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    