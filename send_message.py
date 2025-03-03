from cli_parser import CommandLineParser
import socket
from shemas import HttpResponse, HttpRequest
from config import Config
from enum import Enum
import json
from logging_config import setup_logging
import logging

setup_logging()

logger = logging.getLogger(__name__)


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


def send_http_request(http_request: HttpRequest) -> HttpResponse | str:
    """
    Отправляет HTTP-запрос и возвращает ответ.
    """
    try:
        logging.info(f'creating connect to {http_request.host} with socket.')
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((http_request.host, http_request.port))
        logging.info('transform http_request to bytes and send request.')
        client.sendall(http_request.to_bytes())
        response_bytes = b""

        logger.info('read response from server.')
        while True:
            data = client.recv(4096)
            if not data:
                break
            response_bytes += data

        client.close()
        return HttpResponse.from_bytes(response_bytes)

    except Exception as e:
        return f"Error while sending request: {e}"
    

if __name__ == "__main__":
    cli_parser = CommandLineParser()
    config = Config("config.toml")

    logging.info('creating HttpRequest object.')
    http_request: HttpRequest = HttpRequest(
        method=HttpMethod.POST.value,
        path=config.path,
        host=config.host,
        port=config.port,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {config.encoded_credentials}",
        },
        body=json.dumps({
            "recipient": cli_parser.get_recipient(),
            "sender": cli_parser.get_sender(),
            "message": cli_parser.get_message()
        })
    )

    response: HttpResponse = send_http_request(http_request)
    logging.info(f'{response.status_code=}')
    logging.info(f'{response.body=}')
