import base64
import zlib


class ZebraFontEncoder:
    @staticmethod
    def crc16(data: bytes, poly=0x8408):
        """
        CRC-16-CCITT Algorithm
        """
        data = bytearray(data)
        crc = 0xFFFF
        for b in data:
            cur_byte = 0xFF & b
            for _ in range(0, 8):
                if (crc & 0x0001) ^ (cur_byte & 0x0001):
                    crc = (crc >> 1) ^ poly
                else:
                    crc >>= 1
                cur_byte >>= 1
        crc = ~crc & 0xFFFF
        crc = (crc << 8) | ((crc >> 8) & 0xFF)

        bytes_ = crc & 0xFFFF
        return f"{bytes_:#06x}"[2:]

    def generate_command(
        self,
        font_path,
        font_filename,
        font_extension="TTF",
        output_path="out.txt",
        method="ascii",
    ):
        with open(font_path, "rb") as f:
            content = f.read()

        encoder = {
            "ascii": self.ascii_encode,
            "b64": self.base64_encode,
            "z64": self.z64_encode,
        }[method]

        data = encoder(content)

        if method == "ascii":
            head = f"~DUR:{font_filename}.{font_extension}"
        else:
            head = f"~DT{font_filename}"

        output = f"{head},{len(content)},{data}"

        with open(output_path, "w") as f:
            f.write(output)

    def ascii_encode(self, content):
        return content.hex().upper()

    def base64_encode(self, content):
        base64_bytes = base64.b64encode(content)
        base64_string = base64_bytes.decode("ascii")
        crc = self.crc16(base64_bytes)
        return f":B64:{base64_string}:{crc}"

    def z64_encode(self, content):
        compressed = zlib.compress(content)
        base64_bytes = base64.b64encode(compressed)
        base64_string = base64_bytes.decode("ascii")
        crc = self.crc16(base64_bytes)
        return f":Z64:{base64_string}:{crc}"


if __name__ == "__main__":
    fonts = ZebraFontEncoder()
    fonts.generate_command("./ROBOTO.TTF", font_filename="ROBOTO", method="ascii")
