from rest_framework import serializers
from .models import User, Item, Category, Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userID', 'username', 'email', 'password', 'role', 'isVerified', 'verifiedAt', 'createdAt']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'SKU', 'category', 'tag', 'cost', 'available_stock']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'categoryID']

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['userID', 'token', 'createdAt']