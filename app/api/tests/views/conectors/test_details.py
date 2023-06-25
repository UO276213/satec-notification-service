import json
from unittest import mock
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.conectors import ConectorDetails
from rest_framework import status
from api.tests.views.util import FakeSerializer, create_conector, create_user
from api.serializers import ConectorsSerializer

endpoint = "/v1/conectors"


class TestDetailsServices(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_exist(self):
        '''Comprueba que se muestra el conector cuando el usuario esta autenticado y existe'''

        # Creamos un nuevo usario autenticado
        user, token = create_user()
        conector = create_conector("Conector1")

        with mock.patch("api.serializers.get_subscription_data_serializer") as mock_get_serializer:

            mock_get_serializer.return_value = FakeSerializer
            # Apuntamos el endpoint con el método get
            request = self.factory.get(f'{endpoint}/{conector.id}')
            force_authenticate(request, user, token)

            # Llamamos a la vista
            response = ConectorDetails.as_view()(request, conector_id=conector.id)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                response.data, ConectorsSerializer(conector).data)
            
            declared_fields = FakeSerializer.__dict__["_declared_fields"]
            field_pairs = {key:value for key, value in declared_fields.items()}
            self.assertEqual(
                response.data["interface"], str(field_pairs))


    def test_not_exist(self):
        '''Comprueba que se lanza un error cuando no existe el conector'''

        # Creamos un nuevo usario autenticado
        user, token = create_user()

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint + "/1")

        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = ConectorDetails.as_view()(request, conector_id=1)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"detail": f"Conector con id 1 no existe."})

    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint + "/1")

        # Llamamos a la vista
        response = ConectorDetails.as_view()(request, conector_id=1)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {"detail": f"Authentication credentials were not provided."})
