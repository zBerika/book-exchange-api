
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

# Django-ს აქტიური მომხმარებლის მოდელის მიღება
User = get_user_model()


# მომხმარებლის ავთენტიფიკაციის ტესტები
class UserAuthTest(APITestCase): #
    # მეთოდი, რომელიც სრულდება ყოველი ტესტის წინ
    def setUp(self):
        self.client = APIClient()  # API კლიენტის ინიციალიზაცია ტესტირებისთვის
        self.register_url = reverse('register')  # URL რეგისტრაციისთვის
        self.login_url = reverse('login')  # URL ავტორიზაციისთვის

    # ტესტი მომხმარებლის წარმატებულ რეგისტრაციაზე
    def test_user_registration_success(self):
        data = {
            'username': 'testuser1',
            'ელ_ფოსტა': 'test1@example.com',
            'password': 'strongpassword123',
            'password2': 'strongpassword123',
            'ტელეფონის_ნომერი': '123456789',
            'ლოკაციის_დეტალები': 'თბილისი'
        }
        response = self.client.post(self.register_url, data, format='json')
        # Ожидаем 201 Created статус
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         f"მოსალოდნელი იყო 201, მიღებულია {response.status_code}. პასუხი: {response.data}")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser1')

    # ტესტი რეგისტრაციის შეცდომაზე, როცა პაროლები არ ემთხვევა
    def test_user_registration_password_mismatch(self):
        data = {
            'username': 'testuser2',
            'ელ_ფოსტა': 'test2@example.com',
            'password': 'strongpassword123',
            'password2': 'differentpassword',
            'ტელეფონის_ნომერი': '987654321',
            'ლოკაციის_დეტალები': 'ბათუმი'
        }
        response = self.client.post(self.register_url, data, format='json')
        # 400 Bad Request სტატუსს
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f"მოსალოდნელი იყო 400, მიღებულია {response.status_code}. პასუხი: {response.data}")
        # ვამოწმებთ, რომ პასუხის მონაცემებში არის შეცდომა, რომელიც დაკავშირებულია 'password'-თან (როგორც მითითებულია თქვენს სერიალიზატორში).
        self.assertIn('password', response.data, f"Response data: {response.data}")

    # ტესტი მომხმარებლის წარმატებულ ავტორიზაციაზე
    def test_user_login_success(self):
        # ჯერ ვქმნით მომხმარებელს, რომ შესაძლებელი გახდეს ავტორიზაცია.
        # მომხმარებლის შექმნისას 'ელ_ფოსტა' ვიყენებთ როგორც ელფოსტის ველს.
        User.objects.create_user(username='testuser_login', ელ_ფოსტა='login@example.com', password='testpassword123')
        data = {
            'ელ_ფოსტა': 'login@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data, format='json')
        # Ожидаем 200 OK статус
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f"მოსალოდნელი იყო 200, მიღებულია {response.status_code}. პასუხი: {response.data}")
        self.assertIn('token', response.data)  # ვამოწმებთ, რომ პასუხი შეიცავს ტოკენს.

    # ტესტი ავტორიზაციის შეცდომაზე, არასწორი პაროლით
    def test_user_login_invalid_password(self):
        # Создаем пользователя для теста
        User.objects.create_user(username='testuser_invalid_pass', ელ_ფოსტა='invalid@example.com',
                                 password='correctpassword')
        data = {
            'ელ_ფოსტა': 'invalid@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        # 400 Bad Request статус
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f"მოსალოდნელი იყო 400, მიღებულია {response.status_code}. პასუხი: {response.data}")
        #  'non_field_errors' / 'detail'
        self.assertTrue('non_field_errors' in response.data or 'detail' in response.data,
                        f"პასუხში მოსალოდნელი იყო 'non_field_errors' ან 'detail': {response.data}")

    # ახალი ტესტი: რეგისტრაცია დუბლირებული ელ_ფოსტით
    def test_user_registration_duplicate_email(self):
        User.objects.create_user(username='existinguser', ელ_ფოსტა='duplicate@example.com', password='password123')
        data = {
            'username': 'anotheruser',
            'ელ_ფოსტა': 'duplicate@example.com',
            'password': 'newpassword',
            'password2': 'newpassword'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f"მოსალოდნელი იყო 400, მიღებულია {response.status_code}. პასუხი: {response.data}")
        self.assertIn('ელ_ფოსტა', response.data, f"Response data: {response.data}")  # 404 'эл_ფოსტა'

    # ახალი ტესტი: რეგისტრაცია ელ_ფოსტის გარეშე (თუ ელ_ფოსტა სავალდებულოა)
    def test_user_registration_missing_email(self):
        data = {
            'username': 'noemailuser',
            'password': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f"მოსალოდნელი იყო 400, მიღებულია {response.status_code}. პასუხი: {response.data}")
        self.assertIn('ელ_ფოსტა', response.data, f"Response data: {response.data}")