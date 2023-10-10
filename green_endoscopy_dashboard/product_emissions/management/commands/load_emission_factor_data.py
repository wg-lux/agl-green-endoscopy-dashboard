from django.core.management.base import BaseCommand
from ...models import EmissionFactor
from agl_base_db.models import Unit
from agl_base_db.utils import load_model_data_from_yaml
from ...data import EMISSION_FACTOR_DATA_DIR

SOURCE_DIR = EMISSION_FACTOR_DATA_DIR # e.g. settings.DATA_DIR_INTERVENTION

MODEL_0 = EmissionFactor

IMPORT_MODELS = [ # string as model key, serves as key in IMPORT_METADATA
    MODEL_0.__name__,
]

IMPORT_METADATA = {
    MODEL_0.__name__: {
        "dir": SOURCE_DIR, # e.g. "interventions"
        "model": MODEL_0, # e.g. Intervention
        "foreign_keys": ["unit"], # e.g. ["intervention_types"]
        "foreign_key_models": [Unit] # e.g. [InterventionType]
    }
}

class Command(BaseCommand):
    help = """Load all .yaml files in the data/intervention directory
    into the Intervention and InterventionType model"""

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Display verbose output',
        )

    def handle(self, *args, **options):
        verbose = options['verbose']
        for model_name in IMPORT_MODELS:
            _metadata = IMPORT_METADATA[model_name]
            load_model_data_from_yaml(
                self,
                model_name,
                _metadata,
                verbose
            )