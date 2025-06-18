
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Book, Author, Genre, Condition, BookRequest
from .serializers import BookSerializer, AuthorSerializer, GenreSerializer, ConditionSerializer, BookRequestSerializer
from .permissions import IsOwnerOrReadOnly, IsBookOwner

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class ConditionViewSet(viewsets.ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(ხელმისაწვდომია=True).select_related('ავტორი', 'ჟანრი', 'მდგომარეობა', 'მფლობელი').order_by('-შექმნის_თარიღი')
    serializer_class = BookSerializer
    # permission_classes = (IsOwnerOrReadOnly,)


    def get_permissions(self):

        if self.action == 'create':

            permission_classes = [permissions.IsAuthenticated]

        elif self.action in ['update', 'partial_update', 'destroy']:
            # მხოლოდ წიგნის მფლობელს შეუძლია მისი შეცვლა ან წაშლა.
            permission_classes = [IsOwnerOrReadOnly]
        # ყველა სხვა მოქმედებისთვის (მაგალითად, 'list' - სიის მისაღებად, 'retrieve' - დეტალების მისაღებად)
        else:
            # ყველასთვის ნებადართულია (მათ შორის არაავტორიზებული მომხმარებლებისთვის) წიგნების დათვალიერება.
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


    def perform_create(self, serializer):
        serializer.save(მფლობელი=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Book.objects.filter(მფლობელი=self.request.user).select_related('ავტორი', 'ჟანრი', 'მდგომარეობა', 'მფლობელი').order_by('-შექმნის_თარიღი') | \
                   Book.objects.filter(ხელმისაწვდომია=True).select_related('ავტორი', 'ჟანრი', 'მდგომარეობა', 'მფლობელი').order_by('-შექმნის_თარიღი')
        return self.queryset

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def express_interest(self, request, pk=None):
        წიგნი = self.get_object()
        if წიგნი.მფლობელი == request.user:
            return Response({'დეტალები': 'თქვენ არ შეგიძლიათ საკუთარი წიგნით დაინტერესება.'}, status=status.HTTP_400_BAD_REQUEST)
        if not წიგნი.ხელმისაწვდომია:
            return Response({'დეტალები': 'ეს წიგნი მიუწვდომელია.'}, status=status.HTTP_400_BAD_REQUEST)

        if BookRequest.objects.filter(წიგნი=წიგნი, დაინტერესებული_მომხმარებელი=request.user).exists():
            return Response({'დეტალები': 'თქვენ უკვე გამოხატეთ ინტერესი ამ წიგნის მიმართ.'}, status=status.HTTP_409_CONFLICT)

        serializer = BookRequestSerializer(data={'წიგნი': წიგნი.id, 'დაინტერესებული_მომხმარებელი': request.user.id, 'შეტყობინება': request.data.get('message', '')})
        serializer.is_valid(raise_exception=True)
        serializer.save(წიგნი=წიგნი, დაინტერესებული_მომხმარებელი=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], permission_classes=[IsBookOwner])
    def requests(self, request, pk=None):
        წიგნი = self.get_object()
        if წიგნი.მფლობელი != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        წიგნის_მოთხოვნები = წიგნი.მოთხოვნები.all().select_related('დაინტერესებული_მომხმარებელი')
        serializer = BookRequestSerializer(წიგნის_მოთხოვნები, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='requests/(?P<request_pk>[^/.]+)/accept', permission_classes=[IsBookOwner])
    def accept_request(self, request, pk=None, request_pk=None):
        წიგნი = self.get_object()
        try:
            წიგნის_მოთხოვნა = BookRequest.objects.get(pk=request_pk, წიგნი=წიგნი)
        except BookRequest.DoesNotExist:
            return Response({'დეტალები': 'წიგნის მოთხოვნა ვერ მოიძებნა.'}, status=status.HTTP_404_NOT_FOUND)

        if წიგნის_მოთხოვნა.სტატუსი != 'მოლოდინში':
            return Response({'დეტალები': 'ეს მოთხოვნა არ არის მოლოდინში.'}, status=status.HTTP_400_BAD_REQUEST)

        if not წიგნი.ხელმისაწვდომია:
            return Response({'დეტალები': 'წიგნი უკვე მონიშნულია როგორც მიუწვდომელი.'}, status=status.HTTP_400_BAD_REQUEST)

        წიგნის_მოთხოვნა.სტატუსი = 'მიღებულია'
        წიგნის_მოთხოვნა.save()

        წიგნი.ხელმისაწვდომია = False
        წიგნი.save()

        BookRequest.objects.filter(წიგნი=წიგნი, სტატუსი='მოლოდინში').exclude(pk=წიგნის_მოთხოვნა.pk).update(სტატუსი='უარყოფილია')

        return Response({'დეტალები': 'წიგნის მოთხოვნა მიღებულია და წიგნი მონიშნულია როგორც მიუწვდომელი.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='requests/(?P<request_pk>[^/.]+)/reject', permission_classes=[IsBookOwner])
    def reject_request(self, request, pk=None, request_pk=None):
        წიგნი = self.get_object()
        try:
            წიგნის_მოთხოვნა = BookRequest.objects.get(pk=request_pk, წიგნი=წიგნი)
        except BookRequest.DoesNotExist:
            return Response({'დეტალები': 'წიგნის მოთხოვნა ვერ მოიძებნა.'}, status=status.HTTP_404_NOT_FOUND)

        if წიგნის_მოთხოვნა.სტატუსი != 'მოლოდინში':
            return Response({'დეტალები': 'ეს მოთხოვნა არ არის მოლოდინში.'}, status=status.HTTP_400_BAD_REQUEST)

        წიგნის_მოთხოვნა.სტატუსი = 'უარყოფილია'
        წიგნის_მოთხოვნა.save()
        return Response({'დეტალები': 'წიგნის მოთხოვნა უარყოფილია.'}, status=status.HTTP_200_OK)
class BookRequestViewSet(viewsets.ModelViewSet):
    queryset = BookRequest.objects.all()
    serializer_class = BookRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(დაინტერესებული_მომხმარებელი=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return BookRequest.objects.filter(დაინტერესებული_მომხმარებელი=self.request.user) | \
                   BookRequest.objects.filter(წიგნი__მფლობელი=self.request.user)
        return BookRequest.objects.none()