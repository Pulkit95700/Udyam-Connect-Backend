from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import MyProductsCreateSerializer, MyProductsListSerializer, CategorySerializer, ProductListSerializer
from .models import Product, Category
from django.db.models import Q
from cloudinary.uploader import upload

# Create your views here.

def upload_file_to_cloudinary(image, filename):
    result = upload(image, folder="products")
    return result['secure_url']

class MyProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.query_params.get('search', None)
        category = request.query_params.get('category', None)
        
        if(search == '' and category == ''):
            products = request.user.company.products.filter()
            serializer = MyProductsListSerializer(products, many=True)
            return Response({'message': 'Entries Fetched Successfully!', 'status': status.HTTP_200_OK, 'count': len(serializer.data), 'data': serializer.data,})
        
        if(search and category):
            products = request.user.company.products.filter(Q(name__icontains=search) & Q(category__id=category))
            serializer = MyProductsListSerializer(products, many=True)
            return Response({'message': 'Entries Fetched Successfully!', 'status': status.HTTP_200_OK, 'count': len(serializer.data), 'data': serializer.data,})
        
        if(category):
            products = request.user.company.products.filter(category__id=category)
        
        if(search):
            products = request.user.company.products.filter(name__icontains=search)

        serializer = MyProductsListSerializer(products, many=True)
        return Response({'message': 'Entries Fetched Successfully!', 'status': status.HTTP_200_OK, 'count': len(serializer.data), 'data': serializer.data,})


    def post(self, request):
        serializer = MyProductsCreateSerializer(data=request.data, context = {'user': request.user})
        if(serializer.is_valid(raise_exception=True)):
            serializer.save()
            return Response({'message': 'Product Created Successfully!', 'status': status.HTTP_200_OK, 'data': serializer.data}) 

        return Response({'message': 'Product Creation Failed!', 'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors})
    

class MyProductDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        product = request.user.company.products.filter(id=pk).first()
        if(product):
            serializer = MyProductsListSerializer(product)
            return Response({'message': 'Entry Fetched Successfully!', 'status': status.HTTP_200_OK, 'data': serializer.data})
        return Response({'message': 'Entry Not Found!', 'status': status.HTTP_404_NOT_FOUND})
    
    def patch(self, request, pk):
        product = request.user.company.products.filter(id=pk).first()
        if(product):
            # serializer = MyProductsListSerializer(product, data=request.data, partial=True)
            output = Product.objects.update(
                name = request.data.get('name'),
                description = request.data.get('description'),
                image = upload_file_to_cloudinary(request.data.get('image'), request.data.get('image').name),
                price = request.data.get('price'),
                length = request.data.get('length'),
                breadth = request.data.get('breadth'),
                height = request.data.get('height'),
                units = request.data.get('units'),
                weight = request.data.get('weight'),
                category = Category.objects.get(id=request.data.get('category')),
                company = request.user.company
            )
            Response({'message': 'Entry Updated Successfully!', 'status': status.HTTP_200_OK, 'data': request.data})
        return Response({'message': 'Entry Not Found!', 'status': status.HTTP_404_NOT_FOUND})
    
    def delete(self, request, pk):
        product = request.user.company.products.filter(id=pk).first()
        if(product):
            product.delete()
            return Response({'message': 'Entry Deleted Successfully!', 'status': status.HTTP_200_OK})
        return Response({'message': 'Entry Not Found!', 'status': status.HTTP_404_NOT_FOUND})

class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        product = Product.objects.filter(id=pk).first()
        if(product):
            serializer = ProductListSerializer(product)
            return Response({'message': 'Entry Fetched Successfully!', 'status': status.HTTP_200_OK, 'data': serializer.data})
        return Response({'message': 'Entry Not Found!', 'status': status.HTTP_404_NOT_FOUND})
    
class CompanyProductsListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        search = request.query_params.get('search', None)
        c_id = request.query_params.get('c_id', None)

        print(c_id)
        if(search == '' and c_id == ''):
            products = Product.objects.filter()
            serializer = MyProductsListSerializer(products, many=True)
            return Response({'message': 'Entries Fetched Successfully!', 'status': status.HTTP_200_OK, 'count': len(serializer.data), 'data': serializer.data,})
        
        if(search and c_id):
            products = Product.objects.filter(name__icontains=search, company__id=c_id)
            serializer = MyProductsListSerializer(products, many=True)
            return Response({'message': 'Entries Fetched Successfully!', 'status': status.HTTP_200_OK, 'count': len(serializer.data), 'data': serializer.data,})
        
        if(c_id):
            products = Product.objects.filter(company__id=c_id)
            serializer = MyProductsListSerializer(products, many=True)
            return Response({'message': 'Entries Fetched Successfully!', 'status': status.HTTP_200_OK, 'count': len(serializer.data), 'data': serializer.data,})

        if(search):
            products = Product.objects.filter(name__icontains=search)
            serializer = MyProductsListSerializer(products, many=True)
            return Response({'message': 'Entries Fetched Successfully!', 'status': status.HTTP_200_OK, 'count': len(serializer.data), 'data': serializer.data,})
        
        products = Product.objects.filter()
        serializer = MyProductsListSerializer(products, many=True)
        return Response({'message': 'Entries Fetched Successfully!', 'status': status.HTTP_200_OK, 'count': len(serializer.data), 'data': serializer.data,})


class ProductsListSearchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        search = request.query_params.get('search', None)
        category = request.query_params.get('category', None)
        
        if(search == '' and category == ''):
            products = Product.objects.filter()
            serializer = ProductListSerializer(products, many=True)
            return Response({'message': 'Entries Fetched Successfully!', 'status': status.HTTP_200_OK, 'count': len(serializer.data), 'data': serializer.data,})
        
        if(search and category):
            products = Product.objects.filter(Q(name__icontains=search) & Q(category__id=category))
            serializer = ProductListSerializer(products, many=True)
            return Response({'message': 'Entries Fetched Successfully!', 'status': status.HTTP_200_OK, 'count': len(serializer.data), 'data': serializer.data,})
        
        if(category):
            products = Product.objects.filter(category__id=category)
            serializer = ProductListSerializer(products, many=True)
            return Response({'message': 'Entries Fetched Successfully!', 'status': status.HTTP_200_OK, 'count': len(serializer.data), 'data': serializer.data,})
        
        if(search):
            products = Product.objects.filter(name__icontains=search)
            serializer = ProductListSerializer(products, many=True)
            return Response({'message': 'Entries Fetched Successfully!', 'status': status.HTTP_200_OK, 'count': len(serializer.data), 'data': serializer.data,})

        products = Product.objects.filter()
        serializer = ProductListSerializer(products, many=True)
        return Response({'message': 'Entries Fetched Successfully!', 'status': status.HTTP_200_OK, 'count': len(serializer.data), 'data': serializer.data,})    

class CategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter()
        serializer = CategorySerializer(categories, many=True)
        return Response({'message': 'Categories Fetched Successfully!', 'status': status.HTTP_200_OK, 'count': len(serializer.data), 'data': serializer.data,})