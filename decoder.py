import base64

from encoder import Encoder


class Decoder:
    """Inverse of Encoder: recover the original string from Base64 text."""

    @staticmethod
    def decode(encoded: str) -> str:
        return base64.b64decode(encoded.encode("ascii")).decode("utf-8")


encoder = Encoder()
decoder = Decoder()
print(f"Encoder: {encoder.encode('hello')}")
print(f"Decoder: {decoder.decode(encoder.encode('hello'))}")
