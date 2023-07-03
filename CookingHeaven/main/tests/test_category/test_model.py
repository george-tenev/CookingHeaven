from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from CookingHeaven.main.models import Category

UserModel = get_user_model()


class CategoryModelTests(TestCase):
    def test_category_model__all_valid(self):
        category = Category.objects.create(name="vegan")
        self.assertTrue(isinstance(category, Category))

    def test_category_model__all_valid_str(self):
        category = Category.objects.create(name="vegan")
        self.assertEqual(str(category), "vegan")

    def test_category_model__name_not_valid(self):
        category = Category.objects.create(name="vegan123")
        with self.assertRaises(ValidationError) as context:
            category.full_clean()
            category.save()
        self.assertIsNotNone(context.exception)
