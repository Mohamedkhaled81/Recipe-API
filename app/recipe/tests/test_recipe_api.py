"""
Testing Recipe CRUD OPerations.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag

from recipe.serializers import (
    RecipeReadSerializer,
    RecipeReadDetailsSerializer
)


RECIPES_URL = reverse('recipe:recipe-list')


def create_recipe(user, **params):
    """Create and return a sample reciepe"""
    defaults = {
        'title': 'sample recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'sample description',
        'link': 'https://example.com/recipe.pdf',
    }
    defaults.update(params)
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


def detail_url(recipe_id):
    """create and return a recipe detail URL."""
    return reverse('recipe:recipe-detail', args=[recipe_id])


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test Authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            name="Mohamed Khaled",
            email="test@example.com",
            password="123456test"
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeReadSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_recipes_specific_to_uesr(self):
        """Test retrieving a list of recipes"""
        other_user = create_user(
            name="MOMO",
            email="MOMOmMO@example.com",
            password="1234Testexample"
        )

        create_recipe(user=self.user)
        create_recipe(user=self.user)
        create_recipe(user=other_user)

        res = self.client.get(RECIPES_URL)
        recipes = self.user.recipes.order_by('-id')
        serializer = RecipeReadSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """Test get recipe detail."""
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeReadDetailsSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe_without_tags(self):
        """Tets creating a recipe."""
        payload = {
            'title': 'Sample recipe',
            'time_minutes': 30,
            'price': Decimal('5.99')
        }
        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        """Test a partial update of a recipe."""
        original_link = "https://example.com/recipe.pdf"
        recipe = create_recipe(
            user=self.user,
            title='Sample recipe title',
            link=original_link
        )
        payload = {'title': 'MOMO'}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    def test_full_update_fails(self):
        """Test Full update on recipes."""
        recipe = create_recipe(
            user=self.user,
            title="Original"
        )
        patrial_update_payload = {
            'time_minutes': 25,
            'price': Decimal('9')
        }
        res = self.client.put(
            detail_url(recipe.id),
            patrial_update_payload
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_full_update_succeeds(self):
        """Test that a full update is succeeds."""
        recipe = create_recipe(user=self.user)
        full_update_payload = {
            'title': 'New recipe title',
            'time_minutes': 23,
            'price': Decimal('5.00'),
            'description': 'new description',
            'link': 'https://example.com/recipe.pdf',
        }
        recipe_url = detail_url(recipe.id)
        res = self.client.put(recipe_url, full_update_payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in full_update_payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(self.user, recipe.user)

    def test_update_user_returns_error(self):
        """Test assures that the user can not be updated in the recipe"""
        new_user = create_user(email="MOMO@MOMO.com", password="1233455momo")
        recipe = create_recipe(user=self.user)

        payload = {'user': new_user.id}
        self.client.patch(detail_url(recipe.id), payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """Delete Recipe."""
        recipe = create_recipe(user=self.user)
        res = self.client.delete(detail_url(recipe.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        check_exist = Recipe.objects.filter(id=recipe.id).exists()
        self.assertFalse(check_exist)

    def test_create_recipe_with_existed_tags(self):
        """testing creating Recipe with punch of tags"""
        tag_1 = Tag.objects.create(user=self.user, name="Egyptian")
        tag_2 = Tag.objects.create(user=self.user, name="Magical")
        
        payload = {
            'title': "Koshary",
            'time_minutes': 30,
            'price': Decimal('2.50'),
            'tags': [tag_1.id, tag_2.id]
        }

        res = self.client.post(RECIPES_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(user=self.user)
        self.assertEqual(recipe.tags.count(), 2)

        for key, val in payload.items():
            if key == "tags":
                recipe_tag_ids = set(recipe.tags.values_list('id', flat=True))
                payload_tag_ids = set([tag_id for tag_id in val])
                self.assertEqual(recipe_tag_ids, payload_tag_ids)
            else:
                self.assertEqual(getattr(recipe, key), val)

