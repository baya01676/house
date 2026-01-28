from rest_framework import serializers
from .models import (
    UserProfile, Property, PropertyImage, PropertyDocument, Review, City, District
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'role']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name', 'city_image']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class PropertyListSerializer(serializers.ModelSerializer):
    property_image = PropertyImageSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()
    get_price_property = serializers.SerializerMethodField()
    city = CityListSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ['id', 'title', 'city',
                  'property_image',
                  'avg_rating', 'count_people', 'get_price_property']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()

    def get_price_property(self, obj):
        return obj.get_price_property()


class PropertyDetailSerializer(serializers.ModelSerializer):
    property_image = PropertyImageSerializer(many=True, read_only=True)
    city = CityListSerializer(many=True, read_only=True)
    district = DistrictSerializer(read_only=True)
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()
    get_price_property = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ['id','description', 'title', 'property_image',
                  'district', 'address', 'price', 'rooms', 'condition',
                  'created_at', 'updated_at', 'city', 'avg_rating',
                  'count_people', 'get_price_property']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()

    def get_price_property(self, obj):
        return obj.get_price_property()

class CityDetailSerializer(serializers.ModelSerializer):
    property = PropertyListSerializer(many=True,read_only=True)

    class Meta:
        model = City
        fields = ['city_name','property']


class PropertyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDocument
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'