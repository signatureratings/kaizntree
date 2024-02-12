# Description: This file contains the views for the inventory app.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import jwt
from datetime import datetime, timedelta
from .serializers import UserSerializer, ItemSerializer, CategorySerializer, TokenSerializer
from .models import User, Item, Category, Token
from .utils import send_email, hash_token, verify_token

    

def is_authenticated(request):
    try:
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')
        # check if the access token and refresh token both are there and is valid
        if access_token  and refresh_token:
            d = jwt.decode(access_token, 'sairambalu', algorithms=['HS256'])
            return True
        # if accesstoken is not there but refresh token is there, then generate a new access token
        elif refresh_token:
            d = jwt.decode(refresh_token, 'sairambalu', algorithms=['HS256'])
            user = User.objects.get(userID=d.get('userID'))
            if user is not None:
                # if user.isVerified == False:
                #     return False
                access_token = jwt.encode({
                    'userID': user.userID,
                    'email': user.email,
                    'username': user.username,
                    'exp': datetime.utcnow() + timedelta(days=1)
                }, 'sairambalu')
                request.COOKIES['access_token'] = access_token
                return True
            else:
                print('User not found')
                return False
    except Exception as e:
        print(str(e))
        return False

class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                token = hash_token(serializer.data.get('password'))
                if token is not None:
                    url = f"/api/verify/?token={token}?email={serializer.data.get('email')}"
                    email_status = send_email('Welcome to Kaizntree', 'Thank you for registering with us', 'temp@rmail.address', [serializer.data.get('email')], url)
                    if email_status:
                        print('Email sent successfully')
                    else:
                        print('Email not sent')
                serializer.data.pop('password')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e.__str__())
            return Response({'detail': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class LoginView(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if user is not None:
                userData = UserSerializer(user).data
                if userData.get('password') == password:
                    # if userData.get('isVerified') == False:
                    #     return Response({'detail': 'Account not verified please verify the account'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    access_token = jwt.encode({
                        'userID': userData.get('userID'),
                        'email': userData.get('email'),
                        'username': userData.get('username'),
                        'exp': datetime.utcnow() + timedelta(days=1)
                    }, 'sairambalu')

                    refresh_token = jwt.encode({
                        'userID': userData.get('userID'),
                        'email': userData.get('email'),
                        'username': userData.get('username'),
                        'exp': datetime.utcnow() + timedelta(days=30)
                    }, 'sairambalu')

                    token = TokenSerializer(data={"userID": userData.get('userID'), "token": refresh_token})
                    if token.is_valid():
                        token.save()
                    else:
                        return Response({'detail': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    #add the tokens to the cookies
                    response = Response({
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'detail': 'Login successful'
                    }, status=status.HTTP_200_OK)
                    response.set_cookie('access_token', access_token)
                    response.set_cookie('refresh_token', refresh_token)
                    return response
                else:
                    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e.__str__())
            return Response({'detail': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):

    # this view is authenticated
    def post(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')
        if access_token is None or refresh_token is None:
            return Response({'detail': 'Should be authneticated to access this route'}, status=status.HTTP_400_BAD_REQUEST)
        d = jwt.decode(access_token, 'sairambalu', algorithms=['HS256'])
        user = User.objects.get(email=d.get('email'), userID=d.get('userID'))
        if user is not None:
            token = Token.objects.get(userID=user.userID, token=refresh_token)
            if token is not None:
                token.delete()
            else:
                return Response({'detail': 'Server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            response = Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        newpassword = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            
        except User.DoesNotExist:
            return Response({'message': 'server error'}, status=status.HTTP_500_BAD_REQUEST)
        
        if user is not None:
            userData = UserSerializer(user, data={"password":newpassword}, partial=True)
            if(not userData.is_valid()):
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
            
            if 'password' in userData.validated_data and userData.validated_data['password'] == user.password:
                return Response({'detail': 'New password should be different from the old password'}, status=status.HTTP_400_BAD_REQUEST)

            
            userData.save()
            return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid Email Address'}, status=status.HTTP_400_BAD_REQUEST)

class VerifyView(APIView):

    def get(self, request):
        try:
            token = request.query_params.get('token')
            email = request.query_params.get('email')
            if token is None and email is None:
                return Response({'detail': 'Invalid access'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(email=email)
            if user is not None:
                if user.isVerified == True:
                    return Response({'detail': 'Account already verified'}, status=status.HTTP_200_OK)
                if verify_token(user.password, token):
                    serializer = UserSerializer(user, data={"isVerified": True, "verifiedAt": datetime.now()}, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'detail': 'Account verified successfully'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'detail': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e.__str__())
            return Response({'detail': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ItemsView(APIView):
    
    def get(self, request):
        try:
            if not is_authenticated(request):
                return Response({'detail': 'Should be authenticated to access this route'}, status=status.HTTP_400_BAD_REQUEST)
            
            items = Item.objects.all()
            # filtering
            name = request.query_params.get('name', None)
            if name is not None:
                items = items.filter(name__icontains=name)

            category = request.query_params.get('category', None)
            if category is not None:
                items = items.filter(category__icontains=category)
            
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Item.DoesNotExist:
            return Response({'detail': 'No items found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class ItemView(APIView):
    
    def get(self, request):
        try:
            if not is_authenticated(request):
                return Response({'detail': 'Should be authenticated to access this route'}, status=status.HTTP_400_BAD_REQUEST)
            itemID = request.query_params.get('itemID')
            if itemID is None:
                return Response({'detail': 'ItemID is required'}, status=status.HTTP_400_BAD_REQUEST)
            item = Item.objects.get(itemID=itemID)
            serializer = ItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response({'detail': 'Item not found'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            if not is_authenticated(request):
                return Response({'detail': 'Should be authenticated to access this route'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e.__str__())
            return Response({'detail': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def put(self, request):
    #     try:
    #         if not is_authenticated(request):
    #             return Response({'detail': 'Should be authenticated to access this route'}, status=status.HTTP_400_BAD_REQUEST)
    #         itemID = request.query_params.get('itemID')
    #         if itemID is None:
    #             return Response({'detail': 'ItemID is required'}, status=status.HTTP_400_BAD_REQUEST)
    #         item = Item.objects.get(itemID=itemID)
    #         serializer = ItemSerializer(item, data=request.data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response({"message":"data saved successfully"}, status=status.HTTP_200_OK)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except Item.DoesNotExist:
    #         return Response({'detail': 'Item not found'}, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'detail': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def delete(self, request):
    #     try:
    #         if not is_authenticated(request):
    #             return Response({'detail': 'Should be authenticated to access this route'}, status=status.HTTP_400_BAD_REQUEST)
    #         itemID = request.query_params.get('itemID')
    #         if itemID is None:
    #             return Response({'detail': 'ItemID is required'}, status=status.HTTP_400_BAD_REQUEST)
    #         item = Item.objects.get(itemID=itemID)
    #         item.delete()
    #         return Response({'detail': 'Item deleted successfully'}, status=status.HTTP_200_OK)
    #     except Item.DoesNotExist:
    #         return Response({'detail': 'Item not found'}, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'detail': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryView(APIView):
    
    def get(self, request):
        try:
            if not is_authenticated(request):
                return Response({'detail': 'Should be authenticated to access this route'}, status=status.HTTP_400_BAD_REQUEST)
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'detail': 'No categories found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            if not is_authenticated(request):
                return Response({'detail': 'Should be authenticated to access this route'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                serializer.data.message = 'Category added successfully'
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e.__str__() + 'error')
            return Response({'detail': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
