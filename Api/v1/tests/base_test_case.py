from uuid import uuid4

from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.User.factories import UserFactory


class BaseTestCase(object):
    class HttpMethod(object):
        GET = 'get'
        POST = 'post'
        PUT = 'put'
        PATCH = 'patch'
        DELETE = 'delete'
        OPTIONS = 'options'
        HEAD = 'head'

    class APIActions(object):
        LIST = 'list'
        DETAIL = 'detail'

    def setUp(self) -> None:
        self.setup_user()

        self.ver = 'v1'
        self.base_url = f'api-{self.ver}:%s-%s'
        self.base_route = ''

        self.instance = None

    def setup_user(self):
        password = str(uuid4())
        user = UserFactory.create()
        user.set_password(password)
        user.save()

        client = APIClient()
        client.login(email=user.email, password=password)

        self.user = user
        self.client = client

    def get_base_url(self, action):
        return self.base_url % (self.base_route, action)

    def get_reverse(self, action, *args, **kwargs):
        return reverse(self.get_base_url(action), *args, **kwargs, host='api')

    def get_list_url(self, action=None, *args, **kwargs):
        action = action or self.APIActions.LIST
        return self.get_reverse(action, *args, **kwargs)

    def get_detail_url(self, action=None, *args, **kwargs):
        action = action or self.APIActions.DETAIL
        return self.get_reverse(action, (self.instance.id,), *args, **kwargs)

    def archive_instance(self):
        self.instance.archive()

    def check_key_equality(self, result, data):
        for key in data.keys():
            self.assertEqual(str(result[key]), str(data[key]))


class ListTestMixin(BaseTestCase):
    def test_list(self):
        response = self.client.get(self.get_list_url(), HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.instance.id)

    def test_list_not_found(self):
        self.archive_instance()
        response = self.client.get(self.get_list_url(), HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response, self.instance.id)


class RetrieveTestMixin(BaseTestCase):
    def test_detail(self):
        response = self.client.get(self.get_detail_url(),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.instance.id)

    def test_detail_not_found(self):
        self.archive_instance()
        response = self.client.get(self.get_detail_url(),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class InteractTestMixin(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.data = {}
        self.model = None


class CreateTestMixin(InteractTestMixin):
    def test_create(self):
        prev_counter = self.model.objects.all().count()

        response = self.client.post(self.get_list_url(), data=self.data, HTTP_HOST='api',
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.check_key_equality(response.data, self.data)

        new_counter = self.model.objects.all().count()
        self.assertEqual(new_counter, prev_counter + 1)


class UpdateTestMixin(InteractTestMixin):
    def test_update(self):
        prev_counter = self.model.objects.all().count()

        response = self.client.put(self.get_detail_url(),
                                   data=self.data, HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_key_equality(response.data, self.data)

        new_counter = self.model.objects.all().count()
        self.assertEqual(new_counter, prev_counter)

    def test_partial_update(self):
        prev_counter = self.model.objects.all().count()

        response = self.client.patch(self.get_detail_url(),
                                     data=self.data, HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_key_equality(response.data, self.data)

        new_counter = self.model.objects.all().count()
        self.assertEqual(new_counter, prev_counter)


class DestroyTestMixin(InteractTestMixin):
    def test_destroy(self):
        prev_counter = self.model.objects.all().count()
        instance = self.instance

        self.assertTrue(instance.is_active())
        response = self.client.delete(self.get_detail_url(),
                                      data=self.data, HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        instance.refresh_from_db()
        self.assertFalse(instance.is_active())

        new_counter = self.model.objects.all().count()
        self.assertEqual(new_counter, prev_counter)


class ReadOnlyViewSetMixinTestCase(ListTestMixin, RetrieveTestMixin):
    pass


class ModelViewSetTestCase(CreateTestMixin, UpdateTestMixin, DestroyTestMixin, ListTestMixin, RetrieveTestMixin):
    pass
