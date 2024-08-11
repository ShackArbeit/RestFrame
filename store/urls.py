from django.urls import path
from . import views

# URLConf
urlpatterns = [
    # 這是使用 function view 的樣式
    # path('products/',views.product_list),
    # 這是使用 class view 的樣式
    path('products/',views.ProductList.as_view()),
    # 這是使用 function view 的樣式
    # path('products/<int:id>/',views.product_detail),
    # 這是使用 class view 的樣式
    path('products/<int:id>',views.ProductDetail.as_view()),
    path('products/',views.collection_list),
    path('collections/<int:pk>/',views.collection_detail,name='collection-detail')
]
