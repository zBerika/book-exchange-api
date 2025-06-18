# users/serializers.py
from rest_framework import serializers
from .models import User # ვახდენთ User მოდელის იმპორტს
from django.contrib.auth import authenticate # დარწმუნდით, რომ ეს იმპორტირებულია
from django.contrib.auth.password_validation import validate_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True) # პაროლის დადასტურების ველი

    class Meta:
        model = User
        # ვიყენებთ ველების ქართულ სახელებს
        fields = ('ელ_ფოსტა', 'username', 'password', 'password2', 'ტელეფონის_ნომერი', 'ლოკაციის_დეტალები')
        extra_kwargs = {
            'password': {'write_only': True},
            'ელ_ფოსტა': {'required': True}, # დარწმუნდით, რომ ელ. ფოსტა სავალდებულოა რეგისტრაციისას
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "პაროლები არ ემთხვევა."}) # პაროლები არ ემთხვევა
        return attrs

    def create(self, validated_data):
        # ვშლით password2-ს, რადგან ის არ არის მოდელის ველი
        validated_data.pop('password2')
        # ვქმნით მომხმარებელს, ელ_ფოსტას ვიყენებთ როგორც USERNAME_FIELD
        user = User.objects.create_user(
            ელ_ფოსტა=validated_data['ელ_ფოსტა'],
            username=validated_data.get('username', validated_data['ელ_ფოსტა']), # თუ username არჩევითია, გამოიყენეთ ელ. ფოსტა
            password=validated_data['password'],
            ტელეფონის_ნომერი=validated_data.get('ტელეფონის_ნომერი', ''),
            ლოკაციის_დეტალები=validated_data.get('ლოკაციის_დეტალები', '')
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    ელ_ფოსტა = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        ელ_ფოსტა = attrs.get('ელ_ფოსტა')
        password = attrs.get('password')

        if not ელ_ფოსტა or not password:
            msg = 'უნდა შეიცავდეს "ელ. ფოსტას" და "პაროლს".' # უნდა შეიცავდეს "ელ. ფოსტას" და "პაროლს"
            raise serializers.ValidationError(msg, code='authorization')

        # მთავარი ცვლილება: ვიყენებთ Django-ს authenticate ფუნქციას
        user = authenticate(request=self.context.get('request'), username=ელ_ფოსტა, password=password)

        if not user:
            msg = 'ვერ მოხერხდა შესვლა მითითებული მონაცემებით.' # ვერ მოხერხდა შესვლა მითითებული მონაცემებით
            raise serializers.ValidationError(msg, code='authorization')

        if not user.is_active:
            msg = 'მომხმარებლის ანგარიში გამორთულია.' # მომხმარებლის ანგარიში გამორთულია
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

# --- UserSerializer (ახალი დამატება) ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User # დარწმუნდით, რომ User იმპორტირებულია .models-დან
        # ველები, რომელთა ჩვენება/განახლება გსურთ მომხმარებლის პროფილში.
        # არ შეიტანოთ 'password' აქ.
        fields = ('ელ_ფოსტა', 'username', 'ტელეფონის_ნომერი', 'ლოკაციის_დეტალები')
        # თუ არ გსურთ ამ ველების API-ს მეშვეობით შეცვლა (მხოლოდ წასაკითხი)
        # read_only_fields = ('username', 'ელ_ფოსტა') # ჩვეულებრივ, ელ. ფოსტა და username არ იცვლება რეგისტრაციის შემდეგ
        # თუ ნებას რთავთ ელ. ფოსტის შეცვლას, წაშალეთ იგი read_only_fields-დან