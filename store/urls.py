from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter
from pprint import pprint


router=SimpleRouter()
router.register('products',views.ProductViewSet)
router.register('collections',views.CollectionViewSet)
pprint(router.urls)


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
urlpatterns =router.urls