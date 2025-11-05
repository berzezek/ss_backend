from rest_framework import serializers
from django.contrib.auth.models import User, Group

from ..models import Customer, Category, Job, Product, Lead, Part

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'groups',   # 👈 добавлено
        ]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'type', 'price']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    # Показываем связанные работы
    jobs = JobSerializer(many=True, read_only=True)
    job_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Job.objects.all(),
        source='jobs',
        write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_id', 'jobs', 'job_ids']



class PartSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(), source='job', write_only=True
    )
    lead_id = serializers.PrimaryKeyRelatedField(
        queryset=Lead.objects.all(), source='lead', write_only=True
    )

    class Meta:
        model = Part
        fields = ['id', 'job', 'job_id', 'lead_id', 'value']


class LeadSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True, allow_null=True, required=False
    )

    author = serializers.StringRelatedField(read_only=True, allow_null=True, default=None, required=False)

    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True, allow_null=True, required=False
    )

    parts = PartSerializer(source='part_set', many=True, read_only=True)

    class Meta:
        model = Lead
        fields = [
            'id', 'code', 'status', 'address', 'description',
            'customer', 'customer_id',
            'author',
            'product', 'product_id',
            'created_at', 'updated_at',
            'parts'
        ]
