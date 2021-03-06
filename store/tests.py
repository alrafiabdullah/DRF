import os.path
from django.conf import settings

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


class ProductUpdateTestCase(APITestCase):
    def test_update_product(self):
        product_attrs = {
            'name': 'First Product',
            'description': 'Awesome first product.',
            'price': 99.99,
        }
        response = self.client.post(
            '/api/v1/products/new', product_attrs, format='json')
        if response.status_code != 201:
            print(response.data)
        product = Product.objects.first()
        response = self.client.patch(
            '/api/v1/products/{}/update'.format(product.id), {
                'name': 'New Product',
                'description': 'Awesome Product',
                'price': 77.99,
            },
            format='json',
        )
        updated = Product.objects.get(id=product.id)

        self.assertEqual(updated.name, 'New Product')

    def test_upload_product_photo(self):
        # initial_photo_path = os.path.join(
        #     settings.MEDIA_ROOT, 'images', 'Abdullah_Al_Rafi.jpg')
        product_attrs = {
            'name': 'First Product',
            'description': 'Awesome first product.',
            'price': 99.99,
            # 'photo': initial_photo_path,
        }
        response = self.client.post(
            '/api/v1/products/new', product_attrs, format='json')
        if response.status_code != 201:
            print(response.data)

        product = Product.objects.first()
        original_photo = product.photo
        photo_path = os.path.join(
            settings.MEDIA_ROOT, 'images', 'Abdullah_Al_Rafi.jpg')

        with open(photo_path, 'rb') as photo_data:
            response = self.client.patch(
                '/api/v1/products/{}/update'.format(product.id), {
                    'photo': photo_data
                }, format='multipart',
            )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['photo'], original_photo)

        try:
            updated = Product.objects.get(id=product.id)
            expected_photo = os.path.join(
                settings.MEDIA_ROOT, 'images', 'Abdullah_Al_Rafi'
            )

            self.assertTrue(
                updated.photo.path.startswith(expected_photo)
            )
        finally:
            os.remove(updated.photo.path)
