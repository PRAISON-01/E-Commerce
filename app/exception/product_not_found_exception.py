class ProductNotFoundException(Exception):
    def __init__(self, message: str = "Product stock Error Occurred") -> None:
        self.message = message
        super().__init__(self.message)