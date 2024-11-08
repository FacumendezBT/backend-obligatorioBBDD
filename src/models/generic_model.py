class GenericModel:
    table: str  # Cada model hace override

    def __init__(self) -> None:
        pass


    @classmethod
    def get_all(cls) -> list[object]:
        pass

    @classmethod
    def get_row(cls, prim_keys: dict) -> None:
        pass

    def save(self) -> bool:
        pass

    def delete_self(self) -> bool:
        pass
