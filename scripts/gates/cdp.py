"""Minimal stdlib client for a local, isolated Chrome page target in CI."""
import base64
import hashlib
import json
import os
import socket
import struct
from urllib.parse import urlsplit


class Client:
    def __init__(self, url):
        parsed = urlsplit(url)
        if parsed.scheme != 'ws' or parsed.hostname not in {'127.0.0.1', 'localhost'}:
            raise ValueError('only a local test browser target is allowed')
        self.socket = socket.create_connection((parsed.hostname, parsed.port), timeout=15)
        self.buffer = b''
        self.events = []
        self.counter = 0
        key = base64.b64encode(os.urandom(16)).decode()
        request = f'GET {parsed.path} HTTP/1.1\r\nHost: {parsed.netloc}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'
        self.socket.sendall(request.encode())
        while b'\r\n\r\n' not in self.buffer:
            data = self.socket.recv(4096)
            if not data:
                raise OSError('Chrome closed the protocol handshake')
            self.buffer += data
        head, self.buffer = self.buffer.split(b'\r\n\r\n', 1)
        expected = base64.b64encode(hashlib.sha1((key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest())
        if b'101' not in head.split(b'\r\n', 1)[0] or expected not in head:
            raise OSError('Chrome did not accept the protocol handshake')

    def read(self, count):
        while len(self.buffer) < count:
            data = self.socket.recv(max(4096, count - len(self.buffer)))
            if not data:
                raise OSError('Chrome closed the page connection')
            self.buffer += data
        result, self.buffer = self.buffer[:count], self.buffer[count:]
        return result

    def send(self, payload, opcode=1):
        mask = os.urandom(4)
        size = len(payload)
        if size < 126:
            header = bytes([0x80 | opcode, 0x80 | size])
        elif size < 65536:
            header = bytes([0x80 | opcode, 0x80 | 126]) + struct.pack('!H', size)
        else:
            header = bytes([0x80 | opcode, 0x80 | 127]) + struct.pack('!Q', size)
        masked = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
        self.socket.sendall(header + mask + masked)

    def receive(self):
        chunks = []
        while True:
            first, second = self.read(2)
            size = second & 0x7f
            if size == 126:
                size = struct.unpack('!H', self.read(2))[0]
            elif size == 127:
                size = struct.unpack('!Q', self.read(8))[0]
            if size > 16 * 1024 * 1024:
                raise ValueError('unexpectedly large protocol frame')
            mask = self.read(4) if second & 0x80 else None
            payload = self.read(size)
            if mask:
                payload = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
            opcode = first & 0xf
            if opcode == 8:
                raise OSError('Chrome closed the protocol session')
            if opcode == 9:
                self.send(payload, opcode=10)
                continue
            if opcode == 10:
                continue
            chunks.append(payload)
            if first & 0x80:
                message = json.loads(b''.join(chunks))
                if 'method' in message:
                    self.events.append(message)
                return message

    def command(self, method, **params):
        self.counter += 1
        request_id = self.counter
        self.send(json.dumps({'id': request_id, 'method': method, 'params': params}).encode())
        while True:
            message = self.receive()
            if message.get('id') == request_id:
                if 'error' in message:
                    raise ValueError(f'{method}: {message["error"]}')
                return message.get('result', {})

    def wait_for(self, method, start=0, **params):
        while True:
            for event in self.events[start:]:
                if event.get('method') == method and all(event.get('params', {}).get(key) == value for key, value in params.items()):
                    return event
            start = len(self.events)
            self.receive()

    def close(self):
        self.socket.close()
