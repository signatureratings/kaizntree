from django.test import TestCase,  RequestFactory
from .views import RegisterView, LoginView, LogoutView, ItemsView, ItemView

# Create your tests here.

class AuthenticationTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.registerview = RegisterView.as_view()
        self.loginview = LoginView.as_view()
        self.itemsview = ItemsView.as_view()
        self.itemview = ItemView.as_view()
        self.logoutview = LogoutView.as_view()
    
    def test_register_post(self):
        request = self.factory.post('/register/', {'username': 'test', 'password': 'test', 'email': 'sample@gmail.com'})
        response = self.registerview(request)
        self.assertEqual(response.status_code, 201)


    def test_register_post_invalid(self):
        request = self.factory.post('/register/', {'username': 'test', 'password': 'test'})
        response = self.registerview(request)
        self.assertEqual(response.status_code, 400)

    
    def test_login_post_invalid(self):
        request = self.factory.post('/login/', {'password': 'test'})
        response = self.loginview(request)
        self.assertEqual(response.status_code, 400)
    
    def test_login_post_invalid_email(self):
        request = self.factory.post('/login/', {'password': 'test', 'email': 'sample'})
        response = self.loginview(request)
        self.assertEqual(response.status_code, 400)
    
    # cannot access items without token
    def test_get_items(self):
        request = self.factory.get('/items/')
        response = self.itemsview(request)
        self.assertEqual(response.status_code, 400)
    
    # cannot access item without token
    def test_get_item(self):
        request = self.factory.get('/items/?itemID=1')
        response = self.itemview(request)
        self.assertEqual(response.status_code, 400)

    # cannot access item without token
    def test_logout(self):
        request = self.factory.get('/logout/')
        response = self.logoutview(request)
        self.assertEqual(response.status_code, 405)

    

    
