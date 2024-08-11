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
    path('products/<int:pk>',views.ProductDetail.as_view()),
    path('collection/',views.CollectionList.as_view()),
    path('collections/<int:pk>/',views.CollectionDetail.as_view(),name='collection-detail')
]
