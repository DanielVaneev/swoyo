from dataclasses import dataclass


@dataclass
class HttpRequest:
    method: str
    path: str
    headers: dict[str, str]
    host: str
    body: str = ""
    port: int = 80

    def to_bytes(self) -> bytes:
        """Сериализует HTTP-запрос в байты."""
        request_line = f"{self.method} {self.path} HTTP/1.1\r\n"

        if "Host" not in self.headers:
            self.headers["Host"] = self.host

        content_length = len(self.body.encode('utf-8'))
        self.headers["Content-Length"] = str(content_length)

        headers = ''.join(f"{key}: {value}\r\n" for key, value in self.headers.items())

        return (request_line + headers + "\r\n" + self.body).encode('utf-8')


@dataclass
class HttpResponse:
    status_code: int
    status_message: str
    headers: dict[str, str]
    body: str = ""

    @staticmethod
    def from_bytes(data: bytes) -> 'HttpResponse':
        """Десериализует HTTP-ответ из байтов."""
        data_str = data.decode('utf-8')
        lines = data_str.split("\r\n")

        _, status_code, status_message = lines[0].split(" ", 2)
        headers = {}
        i = 1
        while lines[i]:
            header_key, header_value = lines[i].split(":", 1)
            headers[header_key.strip()] = header_value.strip()
            i += 1

        body = "\n".join(lines[i+1:])
        return HttpResponse(
            status_code=int(status_code), 
            status_message=status_message, 
            headers=headers, 
            body=body
        )
