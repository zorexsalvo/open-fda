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


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('identifier', 'name')


class ItemSerializer(serializers.ModelSerializer):
    plan = serializers.SlugRelatedField(queryset=Plan.objects.all(),
                                        slug_field='identifier')

    class Meta:
        model = Item
        fields = ('identifier', 'plan', 'payment_term', 'quantity')
        read_only_fields = ('cart', )

    def to_representation(self, obj):
        data = super(ItemSerializer, self).to_representation(obj)
        plan_serializer = PlanSerializer(
            Plan.objects.get(identifier=data['plan']))
        data['plan'] = plan_serializer.data
        return data


class CreateCartSerializer(serializers.ModelSerializer):
    cart_items = ItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('identifier', 'total_amount', 'cart_items', 'status')
        read_only_fields = ('total_amount', 'status')

    def to_representation(self, obj):
        data = super(CreateCartSerializer, self).to_representation(obj)
        data['total_amount'] = data['total_amount'] / 100
        return data

    def create(self, validated_data):
        items = validated_data.pop('cart_items', [])
        cart = Cart.objects.create(**validated_data)

        for item in items:
            cart = Cart.objects.get(identifier=cart)
            plan = Plan.objects.get(identifier=item['plan'].identifier)
            terms = Term.objects.filter(plan=plan, term=item['payment_term'])

            if not terms:
                raise serializers.ValidationError(
                    f"Payment term '{item['payment_term']}' is not available for {plan.name}"
                )

            item['cart_id'] = cart.id
            item['plan_id'] = plan.id
            Item.objects.create(**item)
            cart.total_amount = cart.total_amount + (terms.first().amount *
                                                     item['quantity'])
            cart.save()

        return cart
