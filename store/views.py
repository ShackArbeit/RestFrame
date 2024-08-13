from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
# 使用 class views 
from rest_framework.views import APIView
# 使用 Mixins, Generics
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product,Collection,OrderItem,Review
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer
from django.db.models import Count
# 使用 Views Set
from rest_framework.viewsets import ModelViewSet


class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def get_serializer_context(self):
        return {'request':self.request}
       
    def destory(self,request,*args,**kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response({'error':'Product can not be delete '})
        return super().destory(request,*args,**kwargs)

    # def delete(self,request,pk):
    #     product=get_object_or_404(Product,pk=pk)
    #     if product.orderitems.count()>0:
    #         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# 這裡是使用 class views 的樣式，因為使用 Views Set ，所以不需要再使用
# class ProductList(ListCreateAPIView):
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer
#     def get_serializer_context(self):
#         return {'request':self.request}
    
# 這裡是使用 class views 的樣式，因為使用 Views Set ，所以不需要再使用 
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer
#     def delete(self,request,pk):
#         product=get_object_or_404(Product,pk=pk)
#         if product.orderitems.count()>0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionViewSet(ModelViewSet):
    queryset=Collection.objects.annotate(
        products_count=Count('products')
    )
    serializer_class=CollectionSerializer

class ReivewViewSet(ModelViewSet):
    queryset=Review.objects.all()
    serializer=ReviewSerializer



# 這裡是使用 class views 的樣式，因為使用 Views Set ，所以不需要再使用 
# class CollectionList(ListCreateAPIView):
#     queryset=Collection.objects.annotate(
#         products_count=Count('products').all()
#     )
#     serializer_class=CollectionSerializer
#     def delete(self,request,pk):
#         collection=get_object_or_404(Collection,pk=pk)
#         if collection.products.count()>0:
#             return Response({'error':'Could not be deleted !'})
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# 這裡是使用 class views 的樣式，因為使用 Views Set ，所以不需要再使用 
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset=Collection.objects.annotate(
#         products_count=Count('products')
#     )
#     serializer_class=CollectionSerializer
#     def delete(self,request,pk):
#         collection=get_object_or_404(Collection,pk=pk)
#         if collection.products.count()>0:
#             return Response({'error':'Could not be deleted !'})
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def product_list(request):
    if request.method=='GET':
        queryset=Product.objects.all()
        serializer=ProductSerializer(queryset,many=True,context={
            'request':request
        })
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.validated_data)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

# @api_view()
# def product_detail(request,id):
#     try:
#         product=Product.objects.get(pk=id)
#         serializer=ProductSerializer(product)
#         return Response(serializer.data)
#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
@api_view(['GET','PUT','DELETE'])
def product_detail(request,id):
    product=get_object_or_404(Product,pk=id)
    if request.method=='GET':
        serializer=ProductSerializer(product)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer=ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method=='DELETE':
        if product.orderitems.count()>0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def collection_list(request):
    if request.method=='GET':
        queryset=Collection.objects.annotate(products_count=Count('products')).all()
        serializer=CollectionSerializer(queryset,many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)


@api_view(['GET','PUT','DELETE'])
def collection_detail(request,pk):
    collection=get_object_or_404(
        Collection.objects.annotate(produtcs_count=Count('products'),pk=pk)
    )
    if request.method=='GET':
        serializer=CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer=CollectionSerializer(collection,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method=='DELETE':
        if collection.products.count()>0:
            return Response({'error':'Collection can not be deleted'},status=status.HTTP_405_METHOD_NOT_ALLOWED)    
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    