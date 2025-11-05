from rest_framework import viewsets, pagination, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from ..models import Customer, Category, Job, Product, Lead, Part
from .serializers import (
    CustomerSerializer,
    CategorySerializer,
    JobSerializer,
    ProductSerializer,
    LeadSerializer,
    PartSerializer,
    UserSerializer
)
class DefaultPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """Возвращает данные текущего пользователя"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    # def get_permissions(self):
    #     if self.action == 'list':
    #         self.permission_classes = [permissions.IsAuthenticated]
    #     return super().get_permissions()


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-id')
    serializer_class = CustomerSerializer
    pagination_class = DefaultPagination
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination
    permission_classes = [permissions.IsAuthenticated]


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('id')
    serializer_class = JobSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(products__id=product_id)
        return queryset

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('jobs').all()
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
    permission_classes = [permissions.IsAuthenticated]


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.prefetch_related('part_set', 'customer', 'product').all()
    serializer_class = LeadSerializer
    pagination_class = DefaultPagination
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(author=user)

class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.select_related('lead', 'job').all()
    serializer_class = PartSerializer
    pagination_class = DefaultPagination
    permission_classes = [permissions.IsAuthenticated]