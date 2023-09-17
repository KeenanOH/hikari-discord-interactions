import dataclasses


__all__: list[str] = [
    "Image"
]


@dataclasses.dataclass
class Image:
    url: str
