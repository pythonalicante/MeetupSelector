from http import HTTPStatus


def test_healthcheck(client, reverse_url):
    url = reverse_url("healthcheck")
    expected_payload = {"healthy": True}

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_payload
