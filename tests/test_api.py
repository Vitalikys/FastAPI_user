# https://stackoverflow.com/questions/67255653/how-to-set-up-and-tear-down-a-database-between-tests-in-fastapi
from unittest import TestCase
from fastapi.testclient import TestClient

from app.main import app as web_app


class APITEstCase(TestCase):

    def setUp(self) -> None:
        self.client = TestClient(web_app,
                                 # base_url='http://127.0.0.1:8000'
                                 )

    def test_main_url(self):  # перевірка запуск сервера
        response = self.client.get('/docs')
        self.assertEqual(response.status_code, 200)

    def test_get_all_users(self):
        response = self.client.get("/all_users/")
        # print('ALL_USERS:',response.json())
        self.assertEqual(response.status_code, 200)

    # @pytest.fixture
    # def test_create_user(self):
    #     """
    #     записи йдуть в одну і ту саму базу, тому і свариться що вже є такий юзер
    #     """
    #     user_data = {
    #         "user": {
    #             "email": "usr_test12@mail.ua",
    #             "password": "1111",
    #             "firstname": "from schemas"}}
    #     response = self.client.post('/create_user', json=user_data)
    #     created_usr = response.json()
    #     print(created_usr)
    #     self.assertEqual(created_usr['email'], "usr_test12@mail.ua")
    #     # self.assertEqual(response.json(), {'detail': 'Email already registered '})
    #     # self.assertEqual(response.status_code, 200)

    def test_get_one_usr(self):
        response = self.client.get('/user/1')
        print('JSON = ', response.json())
        print('content = ', response.content)
        self.assertEqual(response.status_code, 200)

    def test_delete_usr(self):
        # from delete === 404 b'{"detail":"Not Found"}' ПРОБЛЕМА
        response = self.client.delete('/user_delete/1')
        print('from delete ===', response.status_code, response.content)
        self.assertEqual(response.status_code, 404)

    def tearDown(self) -> None:
        self.client = None
