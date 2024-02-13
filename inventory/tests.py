import json
from django.test import TestCase,  RequestFactory
from .models import User
from .views import RegisterView, LoginView, LogoutView, ItemsView, ItemView

# Create your tests here.

class RegisterViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = RegisterView.as_view()
        self.user = User(email="sample2@gmail.com", password="test", username="sample").save()
        
    def test_post(self):
        request = self.factory.post('/register/', {'email': 'sample@gmail.com', 'password': 'test', "username": "sample"})
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
    
    def test_post_invalid(self):
        request = self.factory.post('/register/', {'email': 'sample2@gmail.com', 'password': 'test', "username": "sample"})
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
    
    def test_post_invalid2(self):
        request = self.factory.post('/register/', {'email': 'bademail',  "username": "sample"})
        response = self.view(request)
        self.assertEqual(response.status_code, 400)

class LoginViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = LoginView.as_view()
        self.user = User(email="sample2@gmail.com", password="test", username="sample").save()
    
    def test_post(self):
        request = self.factory.post('/login/', {'email': 'sample2@gmail.com', 'password': 'test'})
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
    
    def test_post_invalid(self):
        request = self.factory.post('/login/', {'email': 'sample@gmail.com', 'password': 'test'})
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
    
    def test_post_invalid2(self):
        request = self.factory.post('/login/', {'email': 'sagr', 'password': 'test'})
        response = self.view(request)   
        self.assertEqual(response.status_code, 400)
        
class LogoutViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.loginview = LoginView.as_view()
        self.logoutview = LogoutView.as_view()
        self.user = User(email="sample2@gmail.com", password="test", username="sample").save()

    def test_post_invalid(self):
        request = self.factory.post('/logout/', {'email': 'sample2@gmail.com', 'password': 'test'})
        response = self.logoutview(request)
        self.assertEqual(response.status_code, 400)
    
    def test_post_valid(self):
        request = self.factory.post('/login/', {'email': 'sample2@gmail.com', 'password': 'test'})
        response = self.loginview(request)
        response = self.logoutview(request)
        self.assertEqual(response.status_code, 400)

class ItemsViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.loginview = LoginView.as_view()
        self.view = ItemsView.as_view()
        self.user = User(email="sample2@gmail.com", password="test", username="sample").save()
    
    def test_get(self):
        request = self.factory.post('/login/', {'email': 'sample2@gmail.com', 'password': 'test'})
        response = self.loginview(request)
        accessToken = response.cookies['access_token'].value
        refreshToken = response.cookies['refresh_token'].value
        
        request = self.factory.get('/items/')
        request.COOKIES['access_token'] = accessToken
        request.COOKIES['refresh_token'] = refreshToken
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

class ItemViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.loginview = LoginView.as_view()
        self.view = ItemView.as_view()
        self.user = User(email="sample2@gmail.com", password="test", username="sample").save()
    
    def test_get(self):
        request = self.factory.post('/login/', {'email': 'sample2@gmail.com', 'password': 'test'})
        response = self.loginview(request)
        accessToken = response.cookies['access_token'].value
        refreshToken = response.cookies['refresh_token'].value
        
        request = self.factory.post('/item/', {
    "SKU": "Y-S",
    "name":"Toyk street wrap",
    "units": "Wraps",
    "minimum_stock": "100",
    "desired_stock":"100",
    "in_stock": "86",
    "available_stock":"29", 
    "cost":"5.25",
    "category": "food",
    "tags": json.dumps(["food", "Toyk"])
})
        request.COOKIES['access_token'] = accessToken
        request.COOKIES['refresh_token'] = refreshToken
        response = self.view(request)
        response.render()
        print(response.content, response.status_code)
        itemID = json.loads(response.content)["itemID"]
        
        request = self.factory.get('/item/', {'itemID': itemID})
        request.COOKIES['access_token'] = accessToken
        request.COOKIES['refresh_token'] = refreshToken
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

