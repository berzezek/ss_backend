from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet,
    CategoryViewSet,
    JobViewSet,
    ProductViewSet,
    LeadViewSet,
    PartViewSet,
    UserViewSet
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'leads', LeadViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'parts', PartViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls
