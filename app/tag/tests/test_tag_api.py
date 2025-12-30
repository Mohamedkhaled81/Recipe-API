from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from tag.serializers import (
    TagSerializer
)

TAGS_URL = reverse('tag:tag-list')

def create_tag(user, name):
    """Creating and return tag object"""
    tag = Tag.objects.create(user=user, name=name)
    return tag

def create_user(email="momo@gmail.com", password="momo"):
    """helper function to create a user"""
    user = get_user_model().objects.create_user(email=email, password=password)
    return user

def get_certain_tag(tag_id):
    return reverse('tag:tag-detail', args=[tag_id])


class PuplicTagAPITests(TestCase):
    """Test un-auth access denied"""
    def setUp(self):
        """setting up the client that calls the req.."""
        self.client = APIClient()
    
    def test_auth_required(self):
        """Test auth required to access the tag-endpoint.."""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class privateTagAPITests(TestCase):
    """Tests applied on auth users"""
    def setUp(self):
        """Setting up the test suite"""
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)
    
    def test_list_tags(self):
        """Testing getting a list of tags"""
        create_tag(user=self.user, name="Egy")
        create_tag(user=self.user, name="African")

        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        res = self.client.get(TAGS_URL)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_listing_tags_specific_to_user(self):
        """
        Testing that all the tags retrieved
        belong to the user created them
        """
        usr_2 = create_user(email="soso@gmail.com", password="812002")
        
        create_tag(user=self.user, name="Sweet")
        create_tag(user=self.user, name="Salty")
        create_tag(user=usr_2, name="italian")

        tags = self.user.tags.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        res = self.client.get(TAGS_URL)

        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_tag(self):
        """Test Creating a tag"""
        payload = {
            'name': 'Fruity'
        }
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], payload["name"])
    
    def test_update_tag(self):
        """Testing that the tag is updated"""
        tag = create_tag(user=self.user, name="FFF")
        payload = {
            'name': "MMM"
        }
        res = self.client.put(get_certain_tag(tag.id), payload)
        tag.refresh_from_db()
        self.assertEqual(res.data["name"], tag.name)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_delete_tag(self):
        """testing deleting a tag"""
        tag = create_tag(user=self.user, name="MOMO")
        tag_detail_url = get_certain_tag(tag.id)
        res = self.client.delete(tag_detail_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        check_exists = Tag.objects.filter(id=tag.id).exists()
        self.assertFalse(check_exists)
        

        



        


