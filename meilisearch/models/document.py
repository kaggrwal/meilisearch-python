from __future__ import annotations

from typing import Any, Iterator


class Document:
    __doc: dict

    def __init__(self, doc: dict[str, Any]) -> None:
        self.__doc = doc
        for key in doc:
            setattr(self, key, doc[key])

    def __getattr__(self, attr: str) -> str:
        if attr in self.__doc.keys():
            return attr
        raise AttributeError(f"{self.__class__.__name__} object has no attribute {attr}")

    def __iter__(self) -> Iterator:
        return iter(self.__dict__.items())  # type: ignore

class DocumentsResults:
    def __init__(self, resp: dict[str, Any]) -> None:
        self.results: list[Document] = [Document(doc) for doc in resp['results']]
        self.offset: int = resp['offset']
        self.limit: int = resp['limit']
        self.total: int = resp['total']
