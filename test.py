from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(59,60)
    host = "https://testapi.paspay.kz"
    current_operation_id = 11111121223123123121212121221212212211234213421

    @classmethod
    def increment_operation_id(cls):
        cls.current_operation_id += 1
        return cls.current_operation_id

    @task(1)
    def create_and_check_invoice(self):
        create_operation_id = self.increment_operation_id()

        create_url = "https://testapi.paspay.kz/api/v4/invoice/create"
        create_payload = {
            "operation_id": str(create_operation_id),
            "request_url": "https://paspay.kz/",
            "back_url": "https://paspay.kz/",
            "description": "sdsdsdsdasdasdasd",
            "amount": 4000,
            "currency": "KZT"
        }
        create_headers = {
            'system-name': 'omarket',
            'merchant-token': '123',
            'operation-id': str(create_operation_id),
            'Content-Type': 'application/json'
        }

        try:
            create_response = self.client.post(create_url, json=create_payload, headers=create_headers)
            create_response.raise_for_status()
        except Exception as e:
            print(f"Ошибка create_invoice request: {e}")
        else:
            print(f"Успешно. operation_id: {create_operation_id}")

            # Сохранение текущего operation_id для проверки статуса сразу после создания инвойса
            self.current_operation_id = create_operation_id

            # Проверка статуса сразу после создания инвойса
            self.check_payment_status()

            # Ожидание 60 секунд перед выполнением следующей задачи
            self.wait()

            # Проверка статуса через 60 секунд после создания инвойса
            self.check_payment_status()

    def check_payment_status(self):
        if self.current_operation_id is not None:
            url = "https://testapi.paspay.kz/api/v4/payment/check-status"
            payload = {
                "operation_id": str(self.current_operation_id)
            }
            headers = {
                'operation-id': str(self.current_operation_id),
                'system-name': 'omarket',
                'merchant-token': '123',
                'Content-Type': 'application/json'
            }

            try:
                response = self.client.post(url, json=payload, headers=headers)
                response.raise_for_status()
            except Exception as e:
                print(f"Ошибка check_payment_status request: {e}")
            else:
                print(f"Статус проверен. operation_id: {self.current_operation_id}")
                print(response.text)
        else:
            print("Сначала создай инвойс.")
