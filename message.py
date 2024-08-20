from datetime import datetime


def parse_raw(bytes: list[str], signed: bool = True) -> int:
    val = int("".join(bytes[::-1]), 16)
    if not signed: return val

    if val & (1 << (len(bytes) * 8 - 1)):
        val -= 1 << (len(bytes) * 8)
    return val


class Message:

    def __init__(self, rawMessage: str):
        # Separate timestamp from data
        [timestamp_str, info] = rawMessage.split(")")

        # Parse timestamp
        timestamp_str: str = timestamp_str.strip()[1:]
        self.timestamp: datetime = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
        
        # Split data stream into different parts
        stream: list[str] = info.split()

        # Parse data stream
        self.interface: str = stream[0]
        self.channel: int = int(stream[1]) // 10
        self.drive: int = int(stream[1]) % 10
        self.data_length: int = int(stream[2][1:-1])
        self.raw_bytes: list[str] = stream[3:]

        if len(self.raw_bytes) != self.data_length:
            self.malformed: bool = True
            return

        # Parse raw bytes depending on channel format
        if self.channel == 18:
            self.data: list[int] = [
                parse_raw(self.raw_bytes[0:2], False),
                parse_raw(self.raw_bytes[2:4], True),
                parse_raw(self.raw_bytes[4:8], True)
            ]
        elif self.channel == 28 or self.channel == 38:
            self.data: list[int] = [
                parse_raw(self.raw_bytes[0:4], True),
                parse_raw(self.raw_bytes[4:8], True)
            ]