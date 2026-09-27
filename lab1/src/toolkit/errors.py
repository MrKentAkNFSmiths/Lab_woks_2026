class my_custom_error(Exception):
    pass


class validation_error(my_custom_error):
    def __init__(self, message, field=None):
        super().__init__(message)
        self.field = field


# --- Ошибки калькулятора ---

class empty_expression_error(validation_error):
    def __init__(self, message="Empty expression", field="expression"):
        super().__init__(message, field)


class invalid_character_error(validation_error):
    def __init__(self, message="Unavailable symbol", field="expression"):
        super().__init__(message, field)


class missing_operand_error(validation_error):
    def __init__(self, message="Operand is missing", field="expression"):
        super().__init__(message, field)


class consecutive_operators_error(validation_error):
    def __init__(self, message="Two binary operators in a row", field="expression"):
        super().__init__(message, field)


class division_by_zero_error(validation_error):
    def __init__(self, message="Zero division", field="expression"):
        super().__init__(message, field)


# --- Ошибки конвертера ---

class unknown_unit_error(validation_error):
    def __init__(self, message="Unknown unit", field="unit"):
        super().__init__(message, field)


class incompatible_units_error(validation_error):
    def __init__(self, message="Incompatible units", field="unit"):
        super().__init__(message, field)

class below_absolute_zero_error(validation_error):
    def __init__(self, message="Value is below absolute zero", field="value"):
        super().__init__(message, field)

class invalid_value(validation_error):
    def __init__(self, message="Value is not digit", field="value"):
        super().__init__(message, field)