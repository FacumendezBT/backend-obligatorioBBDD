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

    def insert_row(self, row: dict) -> bool:
        pass

    def save(self, new_attributes: dict, condition: dict) -> None:
        pass

    def delete_self(self, condition: dict) -> None:
        pass
