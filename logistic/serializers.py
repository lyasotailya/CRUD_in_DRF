from rest_framework import serializers

from logistic.models import Product, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['id', 'stock', 'product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            create = StockProduct(
                stock=stock,
                product=position['product'],
                quantity=position['quantity'],
                price=position['price']
            )
            create.save()

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            update = StockProduct.objects.update_or_create(
                stock=stock,
                product=position["product"],
                defaults={"quantity": position["quantity"], "price": position["price"]}
            )

        return stock