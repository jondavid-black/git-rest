import base64


class BinaryUtils:
    @staticmethod
    def encode_to_base64(data: bytes) -> str:
        return base64.b64encode(data).decode("utf-8")

    @staticmethod
    def decode_from_base64(data: str) -> bytes:
        return base64.b64decode(data)
