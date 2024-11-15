class GenericModel:
    table: str  # Cada model hace override

    def to_dict(self) -> dict:
        pass

    def __init__(self) -> None:
        pass

    @classmethod
    def get_all(cls) -> list[object]:
        pass

    @classmethod
    def get_row(cls, prim_keys: dict) -> None:
        pass

    @classmethod
    def from_request(cls, request_data: dict, is_new: bool) -> object:
        pass

    def save(self) -> bool:
        pass

    def delete_self(self) -> bool:
        pass
