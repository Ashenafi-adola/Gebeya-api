from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.accounts.models import User
from apps.products.models import Category, Product
from .models import Report


class ReportModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="reporter@example.com", password="password123"
        )
        self.category = Category.objects.create(
            name="Electroics", description="Electronics items"
        )
        self.product = Product.objects.create(
            name="Test Product",
            price="19.99",
            description="A test product",
            category=self.category,
            seller=self.user,
        )

    def test_str_returns_reason(self):
        report = Report.objects.create(
            reporter=self.user,
            product=self.product,
            reason="Inappropriate listing",
            severity="high",
        )
        self.assertEqual(str(report), "Inappropriate listing")

    def test_get_recent_reports_limits_to_four(self):
        for i in range(6):
            Report.objects.create(
                reporter=self.user,
                product=self.product,
                reason=f"Report {i}",
                severity="medium",
            )

        recent_reports = Report.get_recent_reports()
        self.assertEqual(recent_reports[5].reason, "Report 5")
        self.assertEqual(recent_reports[2].reason, "Report 2")


class CreateReportAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="apiuser@example.com", password="password123"
        )
        self.category = Category.objects.create(
            name="Books", description="Book category"
        )
        self.product = Product.objects.create(
            name="Reportable Book",
            price="9.99",
            description="A book to report",
            category=self.category,
            seller=self.user,
        )
        self.client = APIClient()
        self.url = f"/reports/report/{self.product.id}/"

    def test_authenticated_user_can_create_report(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "reason": "Duplicate listing",
            "severity": "low",
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Report.objects.count(), 1)
        report = Report.objects.first()
        self.assertEqual(report.reason, payload["reason"])
        self.assertEqual(report.severity, payload["severity"])
        self.assertEqual(report.reporter, self.user)
        self.assertEqual(report.product, self.product)

    def test_unauthenticated_user_cannot_create_report(self):
        payload = {
            "reason": "Spam",
            "severity": "high",
        }
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Report.objects.count(), 0)
