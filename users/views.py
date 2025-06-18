# users/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .models import User # ვახდენთ User მოდელის იმპორტს
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] # რეგისტრაციის უფლების მიცემა აუთენტიფიკაციის გარეშე

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.get_or_create(user=user) # ახალი მომხმარებლისთვის ტოკენის ავტომატურად შექმნა

class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        try:
            # ვცდილობთ სერიალიზატორის ვალიდაციას. თუ ვალიდაცია არ შესრულდა,
            # (მაგალითად, authenticate() დააბრუნა None), დაერეგისტრირდება ValidationError.
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            # თუ ვალიდაცია არ შესრულდა, ჩვენ ნათლად ვაბრუნებთ API-პასუხს შეცდომით.
            # ამან ხელი უნდა შეუშალოს Django-ს შაბლონის ძებნას.
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'ელ_ფოსტა': user.ელ_ფოსტა # ვიყენებთ ელ. ფოსტის ველის ქართულ სახელს
        }, status=status.HTTP_200_OK) # ნათლად ვაბრუნებთ 200 OK სტატუსს

# --- Новые View для Logout и UserProfile ---
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,) # მხოლოდ ავტორიზებულ მომხმარებლებს შეუძლიათ გასვლა

    def post(self, request, *args, **kwargs):
        try:
            # ვშლით მომხმარებლის ტოკენს
            request.user.auth_token.delete()
        except Exception:
            # ტოკენი შესაძლოა უკვე წაშლილია ან არ არსებობს
            pass
        # თუ იყენებთ სესიის აუთენტიფიკაციას (მაგალითად, Django browsable API-სთვის), შეგიძლიათ გამოიყენოთ logout
        # from django.contrib.auth import logout
        # logout(request)
        return Response(status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer # დარწმუნდით, რომ UserSerializer აბრუნებს საჭირო მომხმარებლის მონაცემებს
    permission_classes = (IsAuthenticated,) # მხოლოდ ავტორიზებულ მომხმარებლებს შეუძლიათ თავიანთი პროფილის ნახვა/განახლება

    def get_object(self):
        # ვუბრუნებთ მიმდინარე აუთენტიფიცირებულ მომხმარებელს
        return self.request.user