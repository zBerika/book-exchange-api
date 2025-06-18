
from rest_framework import serializers
from .models import Book, Author, Genre, Condition, BookRequest
from users.serializers import UserSerializer # ვახდენთ UserSerializer-ის იმპორტს, თუ გსურთ მომხმარებლის დეტალების ჩვენება მოთხოვნებში/წიგნებში


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__' # მოიცავს ყველა ველს
        # read_only_fields = ['id']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    ავტორი_სახელი = serializers.CharField(source='ავტორი.სახელი', read_only=True) # ავტორის სახელის ჩვენება
    ჟანრი_სახელი = serializers.CharField(source='ჟანრი.სახელი', read_only=True) # ჟანრის სახელის ჩვენება
    მდგომარეობა_სახელი = serializers.CharField(source='მდგომარეობა.სახელი', read_only=True) # მდგომარეობის სახელის ჩვენება
    მფლობელი_username = serializers.CharField(source='მფლობელი.username', read_only=True) # მფლობელის username-ის ჩვენება
    მფლობელი_email = serializers.CharField(source='მფლობელი.ელ_ფოსტა', read_only=True) # მფლობელის email-ის ჩვენება

    class Meta:
        model = Book
        fields = [
            'id',
            'სათაური',
            'აღწერა',
            'ავტორი',
            'ავტორი_სახელი', # მხოლოდ წასაკითხი
            'ჟანრი',
            'ჟანრი_სახელი', # მხოლოდ წასაკითხი
            'მდგომარეობა',
            'მდგომარეობა_სახელი', # მხოლოდ წასაკითხი
            'მფლობელი',
            'მფლობელი_username', # მხოლოდ წასაკითხი
            'მფლობელი_email', # მხოლოდ წასაკითხი
            'სურათი',
            'შექმნის_თარიღი',
            'განახლების_თარიღი',
            'ხელმისაწვდომია',
            'მიღების_ლოკაციის_დეტალები',
        ]
        read_only_fields = ['მფლობელი', 'შექმნის_თარიღი', 'განახლების_თარიღი', 'ავტორი_სახელი', 'ჟანრი_სახელი', 'მდგომარეობა_სახელი', 'მფლობელი_username', 'მფლობელი_email']

class BookRequestSerializer(serializers.ModelSerializer):
    წიგნი_სათაური = serializers.CharField(source='წიგნი.სათაური', read_only=True)
    დაინტერესებული_მომხმარებელი_username = serializers.CharField(source='დაინტერესებული_მომხმარებელი.username', read_only=True)
    დაინტერესებული_მომხმარებელი_email = serializers.CharField(source='დაინტერესებული_მომხმარებელი.ელ_ფოსტა', read_only=True)

    class Meta:
        model = BookRequest
        fields = [
            'id',
            'წიგნი',
            'წიგნი_სათაური',
            'დაინტერესებული_მომხმარებელი',
            'დაინტერესებული_მომხმარებელი_username',
            'დაინტერესებული_მომხმარებელი_email',
            'შეტყობინება',
            'სტატუსი',
            'შექმნის_თარიღი',
        ]
        read_only_fields = ['სტატუსი', 'შექმნის_თარიღი']