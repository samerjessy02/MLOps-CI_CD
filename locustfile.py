from locust import HttpUser, between, task


class LoanApplicantUser(HttpUser):
    wait_time = between(1, 5)
    payload = {"CreditScore": 619,
               "Geography": "France",
               "Gender": "Female",
               "Age": 42,
               "Tenure": 2,
               "Balance": 0.0,
               "NumOfProducts": 1,
               "HasCrCard": 1,
               "IsActiveMember": 1,
               "EstimatedSalary": 101348.9}
    headers = {"Content-Type": "application/json"}

    @task(5)
    def predict(self):
        self.client.post("/predict", json=self.payload, headers=self.headers)

    @task
    def visit_index(self):
        self.client.get("/")


class LoanApplicantUser2(HttpUser):
    wait_time = between(1, 5)

    @task
    def visit_index(self):
        self.client.get("/")