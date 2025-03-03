import toml
import base64


class Config:
    def __init__(self, config_path: str):
        self.config = self._read_config(config_path)
        self.host = self.config.get("sms-service", {}).get("url")
        self.path = self.config.get("sms-service", {}).get("path")
        self.port = self.config.get("sms-service", {}).get("port")
        self.user = self.config.get("sms-service", {}).get("user")
        self.password = self.config.get("sms-service", {}).get("password")
        self.encoded_credentials = self.encode_credentials()

    @staticmethod
    def _read_config(config_path: str) -> dict:
        """Читает конфиг из TOML-файла и возвращает в виде словаря."""
        try:
            with open(config_path, "r", encoding="utf-8") as file:
                config = toml.load(file)
            return config
        except Exception as e:
            print(f"Error while readinng config: {e}")
            return {}

    def encode_credentials(self) -> str:
        """Кодирует учетные данные в Base64."""
        credentials = f"{self.user}:{self.password}".encode("utf-8")
        return base64.b64encode(credentials).decode("utf-8")
