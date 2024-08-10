from rest_framework import serializers
from .models import Product,Collection
from decimal import Decimal


# class CollectionSerializer(serializers.Serializer):
#     id=serializers.ImageField()
#     title=serializers.CharField(max_length=255)

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title']



class ProductSerializer(serializers.ModelSerializer):
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    class Meta:
        model=Product
        # 可以額外定義 Product class 裡面所沒有定義的 fileds
        fields=['id','title','slug','description','inventory','unit_price','price_with_tax','collection']
    def calculate_tax(self,product:Product):
         return product.unit_price*Decimal(1.2)
    # def create(self,validated_data):
    #     product=Product(**validated_data)
    #     product.other=1
    #     product.save()
    #     return product


# class ProductSerializer(serializers.Serializer):
#     id=serializers.IntegerField()
#     title=serializers.CharField(max_length=255)
#     # 這裡要加上 source ，是因為在 serializers 預設的名稱會是 .models 中 Product class 的項目
#     # 若在 serializers 的項目與前述有差異，要加上 source ，告訴是使用 unit_price 項目
#     price=serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
#     price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
#     # 這裡將 Collection class 內的主鍵給取出
#     # collection=serializers.PrimaryKeyRelatedField(
#     #     queryset=Collection.objects.all()
#     # )
#     # collection=CollectionSerializer()
#     # 將 Collection class 當作 url 顯示在 API 中
#     collection=serializers.HyperlinkedRelatedField(
#         queryset=Collection.objects.all(),
#         view_name='collection-detail'

#     )
#     def calculate_tax(self,product:Product):
#         return product.unit_price*Decimal(1.2)