from rest_framework import serializers
from .models import Product,Collection,Review,Cart,CartItem
from decimal import Decimal


# class CollectionSerializer(serializers.Serializer):
#     id=serializers.ImageField()
#     title=serializers.CharField(max_length=255)

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title','products_count']
    products_count=serializers.IntegerField(read_only=True)


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

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','date','name','description']

    def create(self,validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)
    

class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    product=CartItemProductSerializer()
    total_price=serializers.SerializerMethodField()

    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model=CartItem
        fields=['id','product','quantity','total_price']



class CartSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    items=CartItemSerializer(read_only=True,many=True)
    total_price=serializers.SerializerMethodField()
    def get_total_price(self,cart):
        return sum( [item.quanity * item.product.unit_price for item in cart.items.all()])
    class Meta:
        model=Cart
        fields=['id','items','total_price']


class AddCartItemSerializer(serializers.ModelSerializer):

    product_id=serializers.IntegerField()

    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No Product with the given ID was found.')
        return value

    def save(self, **kwargs):
        card_id=self.context['card_id']
        product_id=self.validated_data['product_id']
        quanity=self.validated_data['quanity']
        try:
            cart_item=CartItem.objects.get(card_id=card_id,product_id=product_id)
            cart_item.quantity+=cart_item.quantity
            cart_item.save()
            self.instance=cart_item
        except CartItem.DoesNotExist:
            self.instance=CartItem.objects.create(card_id=card_id,**self.validated_data)
        
        return self.instance
   
    class Meta:
        model=CartItem
        fields=['id','product_id','quanity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
     class Meta:
         model=CartItem
         fields=['quanity']


