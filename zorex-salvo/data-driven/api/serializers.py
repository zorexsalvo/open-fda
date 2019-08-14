from rest_framework import serializers
from organization.models import Organization
from plan.models import Plan, Term
from cart.models import Cart, Item


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', )


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = (
            'term',
            'amount',
        )

    def to_representation(self, obj):
        data = super(TermSerializer, self).to_representation(obj)
        data.update({'amount': data['amount'] / 100})
        return data


class ListPlanSerializer(serializers.ModelSerializer):
    hmo = OrganizationSerializer()
    payment_terms = TermSerializer(many=True)

    class Meta:
        model = Plan
        fields = ('identifier', 'name', 'hmo', 'payment_terms', 'created',
                  'modified')


class ItemSerializer(serializers.ModelSerializer):
    plan = serializers.SlugRelatedField(queryset=Plan.objects.all(),
                                        slug_field='identifier')

    class Meta:
        model = Item
        fields = ('cart', 'identifier', 'plan', 'payment_term', 'quantity')
        read_only_fields = ('cart', )


class CreateCartSerializer(serializers.ModelSerializer):
    cart_items = ItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = (
            'identifier',
            'cart_items',
        )

    def create(self, validated_data):
        items = validated_data.pop('cart_items', [])
        cart = Cart(**validated_data)
        cart.save()

        for item in items:
            item['card'] = cart.id
            item['plan'] = item['plan'].identifier
            serializer = ItemSerializer(data=item)
            serializer.is_valid(raise_exception=True)
            # serializer.save()

        return cart
