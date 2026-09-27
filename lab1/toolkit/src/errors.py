class MyCustomError(Exception):
    pass

class ValidationError(Exception):
    def __init__(self, message, field=None):
        super().__init__(message)
        self.field = field

class DatabaseError(Exception):
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code

# Простое исключение
raise MyCustomError("Что-то пошло не так")

# С дополнительными атрибутами
raise ValidationError("Неверный формат email", field="email")
raise DatabaseError("Соединение потеряно", error_code=500)

# Обработка
try:
    raise ValidationError("Ошибка валидации", field="username")
except ValidationError as e:
    print(f"Ошибка в поле {e.field}: {e}")