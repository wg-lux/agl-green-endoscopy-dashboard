from django.core.management import BaseCommand, call_command

class Command(BaseCommand):
    help = 'Run all data loading commands in the correct order'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Display verbose output for all commands',
        )

    def handle(self, *args, **options):
        verbose = options['verbose']

        self.stdout.write(self.style.SUCCESS("Calling populate base db data from agl_base_db..."))
        call_command('load_base_db_data', verbose=verbose)

        self.stdout.write(self.style.SUCCESS("Running load_emission_factor_data..."))
        call_command('load_emission_factor_data', verbose=verbose)

        self.stdout.write(self.style.SUCCESS("Running load_resource_data..."))
        call_command('load_resource_data', verbose=verbose)

        self.stdout.write(self.style.SUCCESS("Running load_waste_data..."))
        call_command('load_waste_data', verbose=verbose)

        self.stdout.write(self.style.SUCCESS("Running load_material_data..."))
        call_command('load_material_data', verbose=verbose)

        self.stdout.write(self.style.SUCCESS("Running load_product_group_data..."))
        call_command('load_product_group_data', verbose=verbose)

        # Requires unit, emission_factor
        self.stdout.write(self.style.SUCCESS("Running load_transport_route_data..."))
        call_command('load_transport_route_data', verbose=verbose)     

        # Requires product_group, transport_route
        self.stdout.write(self.style.SUCCESS("Running load_product_data..."))
        call_command('load_product_data', verbose=verbose)

        

        # Requires product_group_data, product_data
        self.stdout.write(self.style.SUCCESS("Running load_reference_product_data..."))
        call_command('load_reference_product_data', verbose=verbose)

        # Requires center, unit (both from agl_base_db) and emission_factor, waste
        self.stdout.write(self.style.SUCCESS("Running load_center_waste_data..."))
        call_command('load_center_waste_data', verbose=verbose)

        #  Requires center, unit (both from agl_base_db) and resource, emission_factor
        self.stdout.write(self.style.SUCCESS("Running load_center_resource_data..."))
        call_command('load_center_resource_data', verbose=verbose)

        # Requires material, product, unit
        self.stdout.write(self.style.SUCCESS("Running load_product_material_data..."))
        call_command('load_product_material_data', verbose=verbose)

        # Load product weight data, requires product, unit
        self.stdout.write(self.style.SUCCESS("Running load_product_weight_data..."))
        call_command('load_product_weight_data', verbose=verbose)

        # # Run the load_information_source command
        # self.stdout.write(self.style.SUCCESS("Running load_information_source..."))
        # call_command('load_information_source', verbose=verbose)

        # # Run the load_center_data command
        # self.stdout.write(self.style.SUCCESS("Running load_center_data..."))
        # call_command('load_center_data', verbose=verbose)

        self.stdout.write(self.style.SUCCESS("All data loading commands executed successfully."))
