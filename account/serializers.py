from rest_framework import serializers
from account.models import User, Company
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField(max_length=255, required=True)
    company_name = serializers.CharField(max_length=200)
    legal_name = serializers.CharField(max_length=200)
    gst_no = serializers.CharField(max_length=15)
    constitution = serializers.CharField(max_length=100)
    type = serializers.CharField(max_length=100)
    contact = serializers.CharField(max_length=10)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    pincode = serializers.CharField(max_length=6) 
    is_active = serializers.BooleanField(default=True)

    #validating password and confirm password

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if(password != password2):
            raise serializers.ValidationError("Password and Confirm Password does not match,")

        return attrs
    

    def create(self, validated_data):
        user = User.objects.create_user(username = validated_data['username'], password = validated_data['password'],)
        company = Company.objects.create(
            user = user,
            email = validated_data['email'],
            company_name = validated_data['company_name'],
            legal_name = validated_data['legal_name'],
            gst_no = validated_data['gst_no'],
            contact = validated_data['contact'],
            type = validated_data['type'],
            constitution = validated_data['constitution'],
            city = validated_data['city'],
            state = validated_data['state'],
            pincode = validated_data['pincode'],
            is_active = validated_data['is_active']
        )

        company.save()

        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username', 'password']
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'username', 'company_name', 'legal_name', 'email', 'gst_no', 'contact', 'type', 'constitution', 'city', 'state', 'pincode']

class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, style={
        'input_type': "password"
    }, write_only = True)
    password2 = serializers.CharField(max_length=255, style={
        'input_type': "password"
    }, write_only = True)
    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        if(password != password2):
            raise serializers.ValidationError("Password and Confirm Password does not match,")
        
        user.set_password(password)
        user.save()
        return attrs
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        
        if Company.objects.filter(email = email).exists():
            user = Company.objects.get(email = email).user
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:8000/api/user/reset-password/'+uid+'/'+token

            body = 'Click Following Link to reset your password ' + link
            data = {
                'subject': 'Reset your Password',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            #send email
            return attrs
        else:
            raise serializers.ValidationError("Ypu are not a registered user")
        
class UserResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, style={
        'input_type': "password"
    }, write_only = True)
    password2 = serializers.CharField(max_length=255, style={
        'input_type': "password"
    }, write_only = True)
    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')

            if(password != password2):
                raise serializers.ValidationError("Password and Confirm Password does not match,")
            
            id = smart_str(urlsafe_base64_decode(uid))
            
            user = User.objects.get(id = id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not valid or Expired")
            
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Token is not valid or Expired")

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'company_name', 'legal_name', 'email', 'gst_no', 'contact', 'type', 'constitution', 'city', 'state', 'pincode']