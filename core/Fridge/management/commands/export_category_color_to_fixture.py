import json
import time
from pprint import pprint
from django.db import transaction
from django.core.management.base import BaseCommand
from core.Fridge.models import FridgeType
from core.Fridge import constants
from core.Utils.Exporter.exporter import CrmMixinJSONExporter


class Command(BaseCommand):
    help = "Export category colors as fixture"

    def add_arguments(self, parser):
        parser.add_argument(
            "--filepath",
            type=str,
            dest="filepath",
            help="Filepath",
        )
        parser.add_argument(
            "--print_only",
            type=bool,
            dest="print_only",
            help="Only print fixture",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        data = CrmMixinJSONExporter(model=FridgeType, export_fields=('name', 'slug')).export()

        if options.get('print_only', False):
            pprint(data)
            return

        stamp = int(time.time())
        filepath = options.get('filepath', None) or constants.FRIDGE_TYPE_DEFAULT_FIXTURE_PATH % stamp
        with open(filepath, "w+") as f:
            f.write(json.dumps(data))
