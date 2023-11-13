from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)  # Время ожидания между запросами

    @task(1)
    def create_invoice(self):
        url = "https://testapi.paspay.kz/api/v4/invoice/create"

        payload = {
            "operation_id": "8971601652321811171",
            "request_url": "https://paspay.kz/",
            "back_url": "https://paspay.kz/",
            "description": "sdsdsdsdasdasdasd",
            "amount": 4000,
            "currency": "KZT"
        }

        headers = {
            'system-name': 'omarket',
            'merchant-token': '123',
            'operation-id': '8971601652321811171',
            'Content-Type': 'application/json'
        }

        try:
            response = self.client.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Генерирует исключение для неудачного статуса ответа
        except Exception as e:
            # Обработка ошибок. Можете вывести сообщение об ошибке или выполнить другие действия
            print(f"Error during request: {e}")
            # Дополнительно, если вы хотите отметить, что запрос завершился неудачей
            # self.failure("create_invoice", str(e))
        else:
            # Если запрос завершился успешно, вы можете выполнить какие-то дополнительные действия
            print("Request was successful")

        # Также можно вывести результат запроса в консоль
        print(response.text)
