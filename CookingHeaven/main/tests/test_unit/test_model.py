from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from CookingHeaven.main.models import Category, Unit

UserModel = get_user_model()



class UnitModelTests(TestCase):
    def test_unit_model__all_valid(self):
        unit = Unit.objects.create(name='gram')
        self.assertTrue(isinstance(unit, Unit))

    def test_category_model__all_valid_str(self):
        unit = Unit.objects.create(name='gram')
        self.assertEqual(str(unit), 'gram')

    def test_category_model__name_not_valid(self):
        unit = Unit.objects.create(name='gram123')
        with self.assertRaises(ValidationError) as context:
            unit.full_clean()
            unit.save()
        self.assertIsNotNone(context.exception)