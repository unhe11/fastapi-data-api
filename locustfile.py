from locust import HttpUser, task, between
import random

class DeviceUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def send_data(self):
        device_id = f"device_{random.randint(1, 100)}"
        payload = {
            "x": random.uniform(-10, 10),
            "y": random.uniform(-10, 10),
            "z": random.uniform(-10, 10)
        }
        self.client.post(f"/api/v1/data/{device_id}", json=payload)

    @task(3)
    def analyze_data(self):
        device_id = f"device_{random.randint(1, 100)}"
        self.client.get(f"/api/v1/analyze/{device_id}")
