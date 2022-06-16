from rest_framework import serializers
from .models import Brand, Category, Image, Product, ProductState, Review, User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True
            },
            'email': {
                'required': True,
            }
        }
    
    def create(self, validated_data):
        #encrypting the password
        user = User.objects.create_user(**validated_data)
        #creat token automaticly
        Token.objects.create(user=user)
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =  Category
        fields = ['name']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Brand
        fields = ['name']

class ProductStateSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ProductState
        fields = ['state']

class ImageListSerializer ( serializers.Serializer ) :
    image = serializers.ListField(child=serializers.FileField())

    def create(self, validated_data):
        product=Product.objects.latest('created_at')
        image=validated_data.pop('image')
        for img in image:
            photo=Image.objects.create(image=img,product=product,**validated_data)
        return photo


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image_url']
        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Review
        fields = ['buyer','product', 'rating', 'comment', 'created_at']

class CUDProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  Product
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    buyers = UserSerializer(many=True, required=False, read_only=True)
    images = ImageSerializer(many=True, required=False, read_only=True,)
    reviews = ReviewSerializer(many=True, required=False, read_only=True)

    class Meta:
        model =  Product
        fields = "__all__"
        depth = 2

        