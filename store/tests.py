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


class ProductDestroyTestCase(APITestCase):
    def test_delete_product(self):

        product_attrs = {
            'name': 'New Product',
            'description': 'Awesome product.',
            'price': 99.99,
        }
        response = self.client.post(
            '/api/v1/products/new', product_attrs, format='json')
        if response.status_code != 201:
            print(response.data)
        initial_product_count = Product.objects.count()
        product_id = Product.objects.first().id

        self.client.delete('/api/v1/products/{}/update'.format(product_id))
        self.assertEqual(
            Product.objects.count(),
            initial_product_count - 1,
        )
        self.assertRaises(
            Product.DoesNotExist,
            Product.objects.get, id=product_id,
        )


class ProductListTestCase(APITestCase):
    def test_list_products(self):
        products_count = Product.objects.count()

        response = self.client.get('/api/v1/products')
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(response.data['count'], products_count)
        self.assertEqual(len(response.data['results']), products_count)
