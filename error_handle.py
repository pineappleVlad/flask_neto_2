from __future__ import annotations


class HttpError(Exception):
    def __int__(self, status_code: int, message: str | dict | list):
        self.status_code = status_code
        self.message = message