from uuid import uuid4

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import User

# Create your tests here.


class TestUser(APITestCase):
    """Test User Model"""

    def setUp(self) -> None:

        self.user: User = User.objects.create(
            uid=uuid4(),
            first_name="Naruto",
            last_name="Uzumaki",
            phone_number="+919876543210",
            email="testuser@email.tld",
        )

        self.client = APIClient()

    def force_authenticate_user(self):
        # Force Authenticate the user.
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):

        user: User = User.objects.create(
            uid=uuid4(),
            first_name="Sasuke",
            last_name="Uchiha",
            phone_number="+919998887776",
        )

        assert str(user), "Sasuke Uchiha"

        # assert user.is_staff is False
        # assert user.is_superuser is False
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_get_user(self):

        url = reverse("user-me")
        self.force_authenticate_user()
        response = self.client.get(url, args=[self.user.id])

        assert response.status_code == status.HTTP_200_OK

    def test_update_user(self):

        url = reverse("user-me")
        data = {"display_name": "Seventh Hokage"}
        response = self.client.patch(url, data, args=[self.user.id], format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        self.force_authenticate_user()

        response = self.client.patch(url, data, args=[self.user.id], format="json")
        assert response.status_code == status.HTTP_200_OK
