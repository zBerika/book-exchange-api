
# ტესტირებისთვის საჭირო მოდულების იმპორტი
from django.test import TestCase
# Django-ს მომხმარებლის მოდელის იმპორტი
from django.contrib.auth import get_user_model
# ჩვენი მოდელების იმპორტი books აპლიკაციიდან
from .models import Book, Author, Genre, Condition

# Django-ს აქტიური მომხმარებლის მოდელის მიღება
User = get_user_model()

# Book მოდელის ტესტირების კლასი
class BookModelTest(TestCase):
    # მეთოდი, რომელიც სრულდება ყოველი ტესტის წინ
    def setUp(self):
        # ვქმნით სატესტო მომხმარებელს
        self.user = User.objects.create_user(username='testuser', ელ_ფოსტა='test@example.com', password='testpassword123')
        # ვქმნით სატესტო ავტორს
        #  'სახელი'
        self.author = Author.objects.create(სახელი='ტესტ ავტორი')
        # ვქმნით სატესტო ჟანრს
        #  'სახელი'
        self.genre = Genre.objects.create(სახელი='ფანტასტიკა')
        # ვქმნით სატესტო წიგნის მდგომარეობას
        # 'სახელი'
        self.condition = Condition.objects.create(სახელი='ახალი')

    # ტესტი წიგნის შექმნაზე
    def test_book_creation(self):
        # ვქმნით წიგნს,
        book = Book.objects.create(
            მფლობელი=self.user,       # 'owner'  'მფლობელი'
            სათაური='სატესტო წიგნი',   # 'title'  'სათაური'
            ავტორი=self.author,       # 'author'  'ავტორი'
            ჟანრი=self.genre,         # 'genre'  'ჟანრი'
            მდგომარეობა=self.condition, # 'condition'  'მდგომარეობა'
        )
        # ვამოწმებთ, რომ წიგნი შეიქმნა და მისი მონაცემები სწორია
        self.assertEqual(book.სათაური, 'სატესტო წიგნი') #'სათაური'
        self.assertEqual(book.მფლობელი, self.user)    #  'მფლობელი'
        self.assertEqual(book.ავტორი.სახელი, 'ტესტ ავტორი')
        self.assertTrue(book.ხელმისაწვდომია)

    # ტესტი წიგნის სტრიქონულ წარმოდგენაზე
    def test_book_str_representation(self):
        book = Book.objects.create(
            მფლობელი=self.user,
            სათაური='სატესტო წიგნი 2',
            ავტორი=self.author,
            ჟანრი=self.genre,
            მდგომარეობა=self.condition,
        )
        # ვამოწმებთ წიგნის სტრიქონულ წარმოდგენას
        self.assertEqual(str(book), "სატესტო წიგნი 2 ავტორი: ტესტ ავტორი")