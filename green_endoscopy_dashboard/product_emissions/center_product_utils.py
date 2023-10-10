from .models.center_product import CenterProduct

# extraction_balloon_escort_2
# esophageal_dilator
# visiglide_2
# peg_freka_15_ch
# biopsy_grasper_hot_radial_jaw_4
# nitinol_stent_aix_oel
# biliary_stent_cotton_leung_sof_flex
# bite_protector
# pressure_syringe_60_ml
# foliodress_gown_standard
# absorbant_pad

PRODUCT_GENERATE_DICT = {
    "extraction_balloon_escort_2": {
        "probability": 0.01,
        "product_name": "extraction_balloon_escort_2",
    },
    "esophageal_dilator": {
        "probability": 0.007,
        "product_name": "esophageal_dilator",
    },
    "visiglide_2": {
        "probability": 0.02,
        "product_name": "visiglide_2",
    },
    "peg_freka_15_ch": {
        "probability": 0.02,
        "product_name": "peg_freka_15_ch",
    },
    "biopsy_grasper_hot_radial_jaw_4": {
        "probability": 0.5,
        "product_name": "biopsy_grasper_hot_radial_jaw_4",
    },
    "nitinol_stent_aix_oel": {
        "probability": 0.005,
        "product_name": "nitinol_stent_aix_oel",
    },
    "biliary_stent_cotton_leung_sof_flex": {
        "probability": 0.01,
        "product_name": "biliary_stent_cotton_leung_sof_flex",
    },
    "bite_protector": {
        "probability": 0.6,
        "product_name": "bite_protector",
    },
    "pressure_syringe_60_ml": {
        "probability": 0.3,
        "product_name": "pressure_syringe_60_ml",
    }
}

def delete_all_center_products():
    center_products = CenterProduct.objects.all()
    center_products.delete()

from datetime import date
import random
from django.utils import timezone
from .models import Product
from agl_base_db.models import Center

def create_center_products():
    N_EXAM = 4000
    START_DATE = date(2022, 1, 1)
    END_DATE = date(2022, 12, 31)
    center_products = []  # List to hold CenterProduct instances

    CENTER_NAME = "university_hospital_wuerzburg"
    center = Center.objects.get(name=CENTER_NAME)

    # Helper function to generate a random date
    def random_date(start_date, end_date):
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return start_date + timezone.timedelta(days=random_days)
    
    #  get products from product database by name (natural key)
    lookup_product_options = {}
    for key in PRODUCT_GENERATE_DICT.keys():
        _product = Product.objects.get_by_natural_key(key)
        lookup_product_options[key] = _product

    # Create products for each examination
    for _ in range(N_EXAM):
        # Generate a list of products based on their probabilities
        product_list = [
            product_dict["product_name"]
            for product_name, product_dict in PRODUCT_GENERATE_DICT.items()
            if random.random() < product_dict["probability"]
        ]

        # Generate a random exam date
        exam_date = random_date(START_DATE, END_DATE)

        # Create CenterProduct instances and add them to the list
        center_products.extend(
            CenterProduct(
                product = lookup_product_options[product_name],
                date_used=exam_date,
                center=center,
            )
            for product_name in product_list
        )

    # Bulk create to save all objects in one database hit
    CenterProduct.objects.bulk_create(center_products)

from collections import Counter
import pandas as pd

from .models.transport_route import TransportRoute

def calculate_product_metrics(center_name="university_hospital_wuerzburg"):
    center = Center.objects.get(name=center_name)
    center_products = CenterProduct.objects.filter(center=center)
    product_names = [_.product.name for _ in center_products]
    product_counter = Counter(product_names)
    aggregated_products = []
    for product_name, quantity in product_counter.items():
        product = Product.objects.get_by_natural_key(product_name)
        product_group = product.product_group
        reference_product = product_group.reference_product

        product_weight, product_unit = product.get_product_weight()
        package_weight, package_unit = product.get_package_weight()

        total_product_weight = product_weight * quantity
        total_package_weight = package_weight * quantity
        total_weight = total_product_weight + total_package_weight

        product_emission_factor = reference_product.emission_factor_product
        product_emission_factor_unit = product_emission_factor.unit
        package_emission_factor = reference_product.emission_factor_package
        package_emission_factor_unit = package_emission_factor.unit

        product_emission = product_emission_factor.value * total_product_weight
        package_emission = package_emission_factor.value * total_package_weight
        total_emission = product_emission + package_emission

        reference_unit = product_unit
        assert reference_unit == package_unit, "Package weight units do not match"
        assert reference_unit == product_emission_factor_unit, "Product emission units do not match"
        assert reference_unit == package_emission_factor_unit, "Package emission units do not match"

        transport_route_europe = TransportRoute.objects.get_by_natural_key("generic_europe")
        transport_route_overseas = TransportRoute.objects.get_by_natural_key("generic_overseas")

        transport_emission_europe = transport_route_europe.emission_factor.value * total_weight
        
        transport_emission_overseas = transport_route_overseas.emission_factor.value * total_weight

        product_dict = {}
        product_dict["ProductName"] = product.name_de
        product_dict["Quantity"] = quantity
        product_dict["ProductWeight"] = total_product_weight
        product_dict["PackageWeight"] = total_package_weight
        product_dict["TotalWeight"] = total_weight
        product_dict["ProductEmission"] = product_emission
        product_dict["PackageEmission"] = package_emission
        product_dict["TotalEmission"] = total_emission
        product_dict["TransportEmissionEurope"] = transport_emission_europe
        product_dict["TransportEmissionOverseas"] = transport_emission_overseas
        product_dict["Unit"] = reference_unit.abbreviation

        print(product)
        print("pachage-weight", product.get_package_material_weight())
        print("product-weight", product.get_product_material_weight())

        aggregated_products.append(product_dict)

    # Convert the QuerySet to a DataFrame
    df = pd.DataFrame.from_records(aggregated_products)

    # Add similar calculations for emissions

    print(df)

    return df
