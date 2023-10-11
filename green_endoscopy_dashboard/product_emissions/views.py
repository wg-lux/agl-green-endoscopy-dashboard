from django.shortcuts import render
from .models import ProductGroup, ReferenceProduct, ProductMaterial
import json
from rest_framework.renderers import JSONRenderer
from .serializers import ProductGroupSerializer
from .center_product_utils import (
    delete_all_center_products,
    create_center_products,
    calculate_product_metrics
)

def round_floats(obj):
    if isinstance(obj, float):
        return round(obj, 5)
    elif isinstance(obj, dict):
        return {key: round_floats(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [round_floats(element) for element in obj]
    else:
        return obj


def home_view(request):
    product_groups = ProductGroup.objects.prefetch_related(
        'reference_product__product__product_materials').all()

    ref_product = ReferenceProduct.objects.filter(product_group=product_groups[0]).first()

    if not ref_product.emission_factor_total:
        for product_group in product_groups:
            print(f"set_emission_factors for {product_group}")
            ref_product.set_emission_factors()


    serializer = ProductGroupSerializer(product_groups, many=True)
    product_group_data = json.loads(JSONRenderer().render(serializer.data).decode('utf-8'))  # This should be a Python list of dictionaries
    rounded_product_group_data = round_floats(product_group_data)

    # Render the dashboard HTML template
    return render(request, 'home.html', {"product_groups": rounded_product_group_data})

def instrument_emissions_view(request):
    df = calculate_product_metrics()
    df_json = df.to_json(orient='records')
    
    # send the dataframe to the template so we can use it with dataTable and plotly
    return render(request, 'instrument_emissions.html', {"df_json": json.dumps(df_json)})

def product_groups_materials_view(request):
    product_groups = ProductGroup.objects.prefetch_related(
        'reference_product__product__product_materials').all()
    serializer = ProductGroupSerializer(product_groups, many=True)
    json_data = JSONRenderer().render(serializer.data)
    return render(request, 'product_groups_materials.html', {'data': json_data.decode("utf-8")})

def product_groups_emissions_view(request):
    product_groups = ProductGroup.objects.prefetch_related(
        'reference_product__product__product_materials').all()
    serializer = ProductGroupSerializer(product_groups, many=True)
    json_data = JSONRenderer().render(serializer.data)
    return render(request, 'product_groups_emissions.html', {'data': json_data.decode("utf-8")})

from django.http import JsonResponse

def reset_center_products(request):
    print("reset_center_products")
    delete_all_center_products()
    create_center_products()

    # return home_view(request)
    # return JSON Success response
    return JsonResponse({'success': True})


