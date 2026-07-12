"""
============================================================
API Route Tests
============================================================
"""


def test_home(client):

    response = client.get("/")


    assert response.status_code == 200


    data = response.json()


    assert data["project"] == (
        "Astravon Live Arena"
    )



def test_health(client):

    response = client.get(
        "/health"
    )


    assert response.status_code == 200


    assert response.json()["success"] is True



def test_api_root(client):

    response = client.get(
        "/api/v1/"
    )


    assert response.status_code == 200