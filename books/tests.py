from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book

class BookAPITest(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

        # Sample data
        self.book_data = {"title": "Test Book", "author": "John Doe", "published_date": "2023-01-01"}

    def test_create_book(self):
        response = self.client.post("/api/books/", self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)

    def test_get_books(self):
        Book.objects.create(**self.book_data)
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_book(self):
        book = Book.objects.create(**self.book_data)
        updated_data = {"title": "Updated Title", "author": "Jane Doe", "published_date": "2023-05-01"}
        response = self.client.put(f"/api/books/{book.id}/", updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")

    def test_delete_book(self):
        book = Book.objects.create(**self.book_data)
        response = self.client.delete(f"/api/books/{book.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
