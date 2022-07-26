from app.main import app


def test_read_main(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "Description": f"Please review the doc page: {app.openapi_url}"
    }
