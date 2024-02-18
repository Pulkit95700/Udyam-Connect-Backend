from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 
from account.models import User
from account.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer, UserResetPasswordSerializer, CompanySerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from account.models import Company
from django.db.models import Q

# Generate Token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer,]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data = request.data)

        if(serializer.is_valid(raise_exception = True)):
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            company = model_to_dict(user.company, fields=['company_name', 'legal_name', 'gst_no', 'contact', 'type', 'constitution', 'city', 'state', 'pincode',])
            return Response({'msg': 'Registration Successful', "token": tokens, 'status': status.HTTP_201_CREATED, "company": company})
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    renderer_classes = [UserRenderer,]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data = request.data)
    
        if(serializer.is_valid(raise_exception=True)):
            username = serializer.data.get('username')
            password = serializer.data.get('password')
           
            user = authenticate(username=username, password=password)
            
            if(user is not None):
                tokens = get_tokens_for_user(user)
                company = model_to_dict(user.company, fields=['company_name', 'legal_name', 'gst_no', 'contact', 'type', 'constitution', 'city', 'state', 'pincode', 'email', 'id'])
                return Response({'msg': 'Login Success', "token": tokens, "company": company}, status=status.HTTP_200_OK)
            else:
                Response({
                    "errors": {
                        'non_field_errors': ['Username or Password is not valid']
                    }
                }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
                    "errors": {
                        'non_field_errors': ['User not Found with following details']
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None):
        serializer = UserProfileSerializer(request.user)

        # if(serializer.is_valid()):
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data = request.data, context={'user': request.user})

        if(serializer.is_valid(raise_exception=True)):
              return Response({'msg': 'Password Changed Successfully',}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data = request.data)

        if(serializer.is_valid(raise_exception=True)):
            return Response({'msg': 'Password Reset link send. Please Check your Email', "status": status.HTTP_200_OK})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        
        serializer = UserResetPasswordSerializer(data = request.data, context={'uid': uid, 'token': token})

        if(serializer.is_valid(raise_exception=True)):
              return Response({'msg': 'Password Reset Successfully',}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        search = request.query_params.get('search', None)
        if(search):
            companies = Company.objects.filter(Q(company_name__icontains=search) | Q(legal_name__icontains=search) | Q(gst_no__icontains=search))
            serializer = CompanySerializer(companies, many=True)
            return Response({'msg': 'Companies fetched successfully', 'data': serializer.data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response({'msg': 'Companies fetched successfully', 'data': serializer.data, 'status': status.HTTP_200_OK }, status=status.HTTP_200_OK)

class CompanyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        company = Company.objects.filter(id=pk).first()
        if(company):
            serializer = CompanySerializer(company)
            return Response({'msg': 'Company fetched successfully', 'data': serializer.data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({'msg': 'Company not found', 'status': status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)