from rest_framework.generics import CreateAPIView
from rest_framework import permissions

from users.models import CustomUser
from users.serializers import RegisterSerializer
# Create your views here.
class NewUserView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    