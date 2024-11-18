from rest_framework import serializers
from .models import Profile, Review, ProductPhotos, Categories, Product, Rating, CartItem, Cart
from django.contrib.auth import authenticate


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    age = serializers.IntegerField(min_value=18)
    phone_number = serializers.CharField(max_length=15)
    status = serializers.BooleanField()
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = Profile.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            age=validated_data['age'],
            phone_number=validated_data['phone_number'],
            status=validated_data['status'],
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Неверные учетные данные.")
        return user


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name']


class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'age', 'phone_number', 'status']


class ReviewSerializer(serializers.ModelSerializer):
    author = ProfileListSerializer()
    created_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta:
        model = Review
        fields = ['author', 'text', 'created_date']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhotos
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['product_name', 'price', 'category']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    owner = ProfileListSerializer()
    date = serializers.DateField(format="%d-%m-%Y")
    reviews = ReviewSerializer(many=True, read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['product_name', 'price', 'description', 'date', 'active', 'photos', 'category', 'owner', 'reviews',
                  'product_video']


class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhotos
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'get_total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_price', 'items']

    def get_total_price(self, obj):
        return obj.get_total_price()
