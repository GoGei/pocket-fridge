import json
from pprint import pprint
from django.db import transaction
from django.core.management.base import BaseCommand
from core.Fridge.models import FridgeType
from core.Fridge import constants
from core.Utils.Exporter.importer import CrmMixinJSONLoader


class Command(BaseCommand):
    help = "Load default fixture for category colors"

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
        parser.add_argument(
            "--print_saved",
            type=bool,
            dest="print_saved",
            help="Print saved fixture",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        filepath = options.get('filepath') or constants.FRIDGE_TYPE_DEFAULT_FIXTURE_PATH
        with open(filepath, "r+") as f:
            data = json.load(f)

        if options.get('print_only', False):
            pprint(data)
            return

        can_be_imported = True
        for item in data:
            name = item.get('name', None)
            slug = item.get('slug', None)

            if name:
                name = name.strip().capitalize()

            try:
                slug = slug or FridgeType.value_to_slug(name)
            except Exception as e:
                self.stdout.write(str(e), style_func=self.style.ERROR)
                can_be_imported = False
                continue

            item.update({'name': name or slug, 'slug': slug})

        if not can_be_imported:
            self.stdout.write('Data can not be imported', style_func=self.style.WARNING)
            return

        load_fields = ('name', 'slug')
        get_by_fields = ('slug',)
        try:
            items, created_count = CrmMixinJSONLoader(model=FridgeType,
                                                      load_fields=load_fields,
                                                      get_by_fields=get_by_fields,
                                                      with_clear=False,
                                                      set_activity=False).load(data)
        except Exception as e:
            msg = 'During import error was raised: %s' % str(e)
            self.stdout.write(msg, style_func=self.style.ERROR)
            return

        if options.get('print_saved', False):
            for item in items:
                self.stdout.write(f'{item.name} - {item.slug}')

        self.stdout.write('Updated %s items' % (len(items) - created_count), style_func=self.style.SUCCESS)
        self.stdout.write('Created %s items' % created_count, style_func=self.style.SUCCESS)
