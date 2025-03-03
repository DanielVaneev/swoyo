import pytest
from shemas import HttpRequest, HttpResponse


def test_http_request_serialization():
    """Тест сериализации HTTP-запроса в байты."""
    request = HttpRequest(
        method="POST",
        path="/test",
        host="example.com",
        headers={"Content-Type": "application/json"},
        body='{"message": "Hello, world!"}',
        port=8080
    )

    request_bytes = request.to_bytes()
    request_str = request_bytes.decode('utf-8')

    assert "POST /test HTTP/1.1" in request_str
    assert "Host: example.com" in request_str
    assert "Content-Type: application/json" in request_str

    expected_length = len(request.body.encode('utf-8'))
    assert f"Content-Length: {expected_length}" in request_str

    assert '{"message": "Hello, world!"}' in request_str


def test_http_response_deserialization():
    """Тест десериализации HTTP-ответа из байтов."""
    raw_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: 27\r\n"
        "\r\n"
        '{"message": "Hello, world!"}'
    ).encode('utf-8')

    response = HttpResponse.from_bytes(raw_response)

    assert response.status_code == 200
    assert response.status_message == "OK"
    assert response.headers["Content-Type"] == "application/json"
    assert response.headers["Content-Length"] == "27"
    assert response.body == '{"message": "Hello, world!"}'


def test_http_request_defaults():
    """Тест значений по умолчанию в HttpRequest."""
    request = HttpRequest(method="GET", path="/", host="example.com", headers={})

    assert request.port == 80
    assert request.body == ""
    assert request.headers == {}

    request_bytes = request.to_bytes()
    request_str = request_bytes.decode('utf-8')

    assert "GET / HTTP/1.1" in request_str
    assert "Host: example.com" in request_str
    assert "Content-Length: 0" in request_str
