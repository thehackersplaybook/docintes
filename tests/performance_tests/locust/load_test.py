from locust import HttpUser, task, between

from app.constants import CONVERT_FILE_TO_MARKDOWN_ENDPOINT

#Have added a dummy.pdf to test the API
class MyUser(HttpUser):
    wait_time = between(1, 2)  # Simulate user wait time between requests (1-5 seconds)

    @task
    def load_test(self):
        self.client.post(CONVERT_FILE_TO_MARKDOWN_ENDPOINT, files={"uploaded_file": open("dummy.pdf", "rb")})  # Replace with the correct file and URL
