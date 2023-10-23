import io

import requests
from PIL import Image
from pyzbar.pyzbar import decode
from django.conf import settings

from rest_framework import serializers
from core.Fridge.models import FridgeProduct


class BarcodeScannedPostSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def read_barcode(self):
        image = self.validated_data.get('image')
        image_data = image.read()
        decoded_objects = decode(Image.open(io.BytesIO(image_data)))
        for obj in decoded_objects:
            return obj.data.decode('utf-8')
        return None

    def get_barcode_data(self):
        barcode = self.read_barcode()
        data = {'barcode': barcode}
        if not barcode:
            return data

        token = settings.FOODREPO_API_KEY
        url = 'https://www.foodrepo.org/api/v3/products'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Token {token}'
        }
        params = {
            'barcodes': barcode
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return data

        result = response.json()['data']
        if not result:
            return data

        try:
            choices = FridgeProduct.FridgeProductUnits
            unit_map = {
                'g': choices.GRAMM,
                'kg': choices.KILOGRAM,
                'ml': choices.MILLITER,
                'l': choices.LITER,
                'cl': choices.MILLITER,
                'i': choices.ITEMS,
            }
            item = result[0]
            names = item['display_name_translations']

            name = None
            for lang, label in settings.LANGUAGES:
                try:
                    name = names[lang]
                    break
                except KeyError:
                    continue

            unit = unit_map.get(item.get('unit'), None)
            qty = item.get('portion_quantity') or item.get('quantity')
            if item['unit'] == 'cl':
                qty *= 10

            data.update({
                'name': name,
                'unit': unit,
                'qty': qty,
            })
        except Exception as e:
            print(e)

        return data
