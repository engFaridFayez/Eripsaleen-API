from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import permissions

from users.models import CustomUser
from users.serializers import RegisterSerializer, UserSerializer
# Create your views here.
class NewUserView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    

class MeView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)