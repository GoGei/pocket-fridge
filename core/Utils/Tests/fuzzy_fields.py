import string
from io import BytesIO
from PIL import Image
from faker import Faker
from factory import fuzzy
from django.conf import settings
from django.core.files import File

LANGUAGES = settings.LANGUAGES
faker = Faker()


class FuzzyEmail(fuzzy.FuzzyText):
    def __init__(self, domain: str = None, *args, **kwargs):
        self.domain = domain
        super().__init__(*args, **kwargs)

    def fuzz(self):
        domain = self.domain
        kwargs = {'domain': domain}
        kwargs = {k: v for k, v in kwargs.items() if v}
        return faker.email(**kwargs)


class FuzzyPhone(fuzzy.FuzzyText):
    def __init__(self, country_code: str = '', with_plus: bool = False, *args, **kwargs):
        self.country_code = country_code
        self.with_plus = with_plus
        super().__init__(*args, **kwargs)

    def fuzz(self):
        phone = fuzzy.FuzzyText(chars=string.digits, length=self.length).fuzz()
        if self.country_code:
            phone = self.country_code + phone
        if self.with_plus:
            phone = '+' + phone
        return phone


class FuzzyParagraph(fuzzy.FuzzyText):
    def __init__(self, nb_sentences=10, *args, **kwargs):
        self.nb_sentences = nb_sentences
        super().__init__(*args, **kwargs)

    def fuzz(self):
        nb_sentences = self.nb_sentences
        length = self.length
        result = ''
        while len(result) < length:
            paragraph = faker.paragraph(nb_sentences=nb_sentences)
            result += paragraph
        if len(result) > length:
            result = result[:length]
        return result


class FuzzyColor(fuzzy.FuzzyText):
    def __init__(self, with_hex=True, *args, **kwargs):
        self.with_hex = with_hex
        super().__init__(*args, **kwargs)

    def fuzz(self):
        color = faker.hex_color()
        color = color.upper()
        if not self.with_hex:
            color = color.replace('#', '')
        return color


class FuzzyLanguage(fuzzy.BaseFuzzyAttribute):
    def __init__(self, fuzzy_class, languages=LANGUAGES, *args, **kwargs):
        self.languages = languages
        self.fuzzy_class = fuzzy_class(*args, **kwargs)
        super().__init__()

    def fuzz(self):
        languages = [item[0] for item in self.languages]
        data = {lang: self.fuzzy_class.fuzz() for lang in languages}
        return data


class FuzzyImage(fuzzy.BaseFuzzyAttribute):

    def __init__(self, name=None, ext='png', size_x=100, size_y=100, **kwargs):
        self.name = name or fuzzy.FuzzyText(length=10).fuzz()
        self.ext = ext
        self.size_x = size_x
        self.size_y = size_y
        super().__init__(**kwargs)

    def fuzz(self):
        image = Image.new('RGB', (self.size_x, self.size_y))
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes.seek(0)

        django_file = File(image_bytes, name=f'{self.name}.{self.ext}')
        return django_file


class FuzzyBoolean(fuzzy.FuzzyChoice):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', (True, False))
        super().__init__(*args, **kwargs)
