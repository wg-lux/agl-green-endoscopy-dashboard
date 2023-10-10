from rest_framework import serializers
from .models import ProductGroup, ReferenceProduct, ProductMaterial, Product, Material, EmissionFactor
from agl_base_db.models import Unit

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('name', 'abbreviation', "name_de", "name_en")

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('name', 'name_de', 'name_en')

class EmissionFactorSerializer(serializers.ModelSerializer):
    unit = UnitSerializer()

    class Meta:
        model = EmissionFactor
        fields = ('name', 'name_de', 'name_en', 'value', 'unit')

class ProductMaterialSerializer(serializers.ModelSerializer):
    unit = UnitSerializer()
    material = MaterialSerializer()
    emission = serializers.SerializerMethodField('get_emission_value')
    emission_unit = serializers.SerializerMethodField('get_emission_unit')

    def get_emission_value(self, obj):
        emission_value, _ = obj.get_emission()
        return emission_value

    def get_emission_unit(self, obj):
        _, emission_unit = obj.get_emission()
        return emission_unit.abbreviation  # Assuming name is the field you want to display

    class Meta:
        model = ProductMaterial
        fields = ('component', 'quantity', "unit", "material", "emission", "emission_unit")  # Add other fields if needed

class ProductSerializer(serializers.ModelSerializer):
    product_materials = ProductMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('name', "name_de", 'product_materials')

class ReferenceProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    emission_factor_total = EmissionFactorSerializer()
    emission_factor_package = EmissionFactorSerializer()
    emission_factor_product = EmissionFactorSerializer()

    class Meta:
        model = ReferenceProduct
        fields = (
            'product',
            'emission_factor_total',
            'emission_factor_package',
            'emission_factor_product'
        )

class ProductGroupSerializer(serializers.ModelSerializer):
    reference_product = ReferenceProductSerializer(read_only=True)

    class Meta:
        model = ProductGroup
        fields = ('name', 'reference_product')
