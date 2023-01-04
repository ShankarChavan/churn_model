from fastapi.testclient import TestClient
from fastapi import status,Request
from churn_api.predict import app

client=TestClient(app=app)

def test_index_page():
    response=client.get('/')
    assert response.status_code==status.HTTP_200_OK
    assert response.json()=={"healthcheck":"True"}


def test_predict_churn():
    expected_result={"prediction":"no"}
    data={
                "number_vmail_messages": 32.0,
                "total_day_calls": 15.0,
                "total_eve_minutes": 20.0,
                "total_eve_charge": 24.0,
                "total_intl_minutes": 3.0,
                "number_customer_service_calls":4.0,
    }
    response=client.post('/predict',json=data)
    assert response.status_code==status.HTTP_200_OK
    assert response.json()==expected_result

