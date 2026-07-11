from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.products.models import Category, Favorities, Product


class ProductAppTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="seller@example.com",
            password="strongpass123",
            first_name="Seller",
            last_name="User",
        )
        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic items",
        )

    def create_product(self, **kwargs):
        defaults = {
            "name": "Phone",
            "price": "100.00",
            "description": "A great phone",
            "category": self.category,
            "seller": self.user,
        }
        defaults.update(kwargs)
        return Product.objects.create(**defaults)

    def test_product_model_defaults_and_string_representations(self):
        product = self.create_product()

        self.assertEqual(str(self.category), "Electronics")
        self.assertEqual(str(product), "Phone")
        self.assertEqual(product.condition, "New")
        self.assertEqual(product.status, "Pending")
        self.assertEqual(product.category, self.category)

    def test_get_all_products_only_returns_approved_products(self):
        self.create_product(name="Approved Product", status="Approved")
        self.create_product(name="Pending Product")

        response = self.client.get("/products/products/")

        self.assertEqual(response.status_code, 200)
        names = [item["name"] for item in response.json()]
        self.assertEqual(names, ["Approved Product"])

    def test_add_product_requires_authentication(self):
        payload = {
            "name": "Laptop",
            "price": "500.00",
            "description": "New laptop",
            "condition": "New",
            "category": self.category.name,
        }

        response = self.client.post("/products/products/new/", payload, format="json")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Product.objects.count(), 0)

    def test_add_product_creates_product_for_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "name": "Laptop",
            "price": "500.00",
            "description": "New laptop",
            "condition": "New",
            "category": self.category.name,
        }

        response = self.client.post("/products/products/new/", payload, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.get(name="Laptop")
        self.assertEqual(product.seller, self.user)
        self.assertEqual(product.category, self.category)

    def test_product_detail_view_adds_view_for_authenticated_user(self):
        product = self.create_product(name="Viewed Product", status="Approved")
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"/products/product-detail/{product.id}/")

        self.assertEqual(response.status_code, 200)
        product.refresh_from_db()
        self.assertIn(self.user, product.views.all())

    def test_favorites_endpoint_toggles_favorite_status(self):
        product = self.create_product(name="Favorite Product", status="Approved")
        self.client.force_authenticate(user=self.user)

        first_response = self.client.post(f"/products/pro-fav/{product.id}/")
        self.assertEqual(first_response.status_code, 200)
        favorites = Favorities.objects.get(user=self.user)
        self.assertIn(product, favorites.product.all())

        second_response = self.client.post(f"/products/pro-fav/{product.id}/")
        self.assertEqual(second_response.status_code, 200)
        favorites.refresh_from_db()
        self.assertNotIn(product, favorites.product.all())
