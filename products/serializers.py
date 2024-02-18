from rest_framework import serializers
from .models import Product, Category
from cloudinary.uploader import upload


def upload_file_to_cloudinary(image, filename):
    result = upload(image, folder="products")
    return result['secure_url']

class MyProductsCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500) 
    image = serializers.ImageField()
    price = serializers.CharField()
    length = serializers.CharField()
    breadth = serializers.CharField()
    height = serializers.CharField()
    weight = serializers.CharField()
    units = serializers.CharField(max_length=10)
    category = serializers.CharField(max_length=100)

    def create(self, validated_data):
        user = self.context.get('user')
        company = user.company
        category = Category.objects.get(id=validated_data.get('category'))
        url = upload_file_to_cloudinary(validated_data.get('image'), validated_data.get('image').name)
        product = Product.objects.create(
            name = validated_data.get('name'),
            description = validated_data.get('description'),
            image = url,
            price = validated_data.get('price'),
            length = validated_data.get('length'),
            breadth = validated_data.get('breadth'),
            height = validated_data.get('height'),
            units = validated_data.get('units'),
            weight = validated_data.get('weight'),
            category = category,
            company = company
        )

        return product
    
class MyProductsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image', 'price', 'length', 'breadth', 'height', 'units', 'weight', 'category', 'is_available', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        depth = 1

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image', 'price', 'length', 'breadth', 'height', 'units', 'weight', 'category', 'is_available', 'company', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        depth = 1