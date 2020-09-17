from rest_framework.test import APITestCase

from .models import Product
# Create your tests here.


class ProductCreateTestCase(APITestCase):
    def test_create_product(self):
        initial_product_count = Product.objects.count()
        product_attrs = {
            'name': 'New Product',
            'description': 'Awesome product.',
            'price': 99.99,
        }
        response = self.client.post(
            '/api/v1/products/new', product_attrs, format='json')
        if response.status_code != 201:
            print(response.data)
        self.assertEqual(
            Product.objects.count(),
            initial_product_count + 1,
        )
        for attr, expected_value in product_attrs.items():
            self.assertEqual(response.data[attr], expected_value)
