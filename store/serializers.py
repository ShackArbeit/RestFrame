from rest_framework import serializers
from .models import Product,Collection
from decimal import Decimal

class ProductSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    title=serializers.CharField(max_length=255)
    # 這裡要加上 source ，是因為在 serializers 預設的名稱會是 .models 中 Product class 的項目
    # 若在 serializers 的項目與前述有差異，要加上 source ，告訴是使用 unit_price 項目
    price=serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    # 這裡將 Collection class 內的主鍵給取出
    collection=serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all()
    )
    def calculate_tax(self,product:Product):
        return product.unit_price*Decimal(1.2)