from django.urls import path
from . import views

from rest_framework_nested import routers
from pprint import pprint


router=routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet)
router.register('cart',views.CartViewSet)


pprint(router.urls)

product_router=routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('review',views.ReivewViewSet,basename='product-reviews')


# urlpatterns = [
#     # 這是使用 function view 的樣式
#     # path('products/',views.product_list),
#     # 這是使用 class view 的樣式
#     path('products/',views.ProductList.as_view()),
#     # 這是使用 function view 的樣式
#     # path('products/<int:id>/',views.product_detail),
#     # 這是使用 class view 的樣式
#     path('products/<int:pk>',views.ProductDetail.as_view()),
#     path('collections/',views.CollectionList.as_view()),
#     path('collections/<int:pk>/',views.CollectionDetail.as_view(),name='collection-detail')
# ]
urlpatterns =router.urls+product_router.urls