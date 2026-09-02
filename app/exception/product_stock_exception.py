class ProductStockException(Exception):
    def __init__(self, message: str = "Product stock Error Occured") -> None:
        self.message = message
        super().__init__(self.message)