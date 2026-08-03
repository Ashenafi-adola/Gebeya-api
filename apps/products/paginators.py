from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination

# Optional: Custom Django Paginator
class CustomDjangoPaginator(Paginator):
    def __init__(self, *args, **kwargs):
        # E.g., setting custom orphans or modified counting
        super().__init__(*args, **kwargs)

# DRF Pagination class referencing the Django Paginator
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size' 
    max_page_size = 100
    django_paginator_class = CustomDjangoPaginator