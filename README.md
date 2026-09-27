# CLI калькулятор с функцией конвертера
___

 Программа открывающаяся в терминале и высчитывающая арифметические выражения, так же с возможностью перевода чисел из одной системы единиц в другую
___
## Функции

>- Калькулятор: вычисление арифметичесиких выражений: `+`, `-`, `*`, `/`, `%`, `//`, `^`.
>- Конвертер длин: {`mm`,`cm`,`m`,`km`}
>- Конвертер масс: {`mg`, `g`, `kg`, `ton`}
>- Конвертер температур: {`c`, `f`, `k`}


## Установка

```bash
python3 -m venv venv
source venv/bin/activete 
pip3 intsall  ".[dev]"
```

## Команды

### Калькулятор 

```bash
python3 -m toolkit calc "(2+2*1.5)^2%4"
# Calculation result: 1.0
```

### Конвертер

```bash
python3 -m toolkit convert 520000 --from cm --to km
# Convertation result: 5.2 km
```

### Help
```bash
python3 -m toolkit --help 
#          Или
python3 -m toolkit
#Выведется меню помощи
```

## Структура
```
lab1/
├── src/
│   └── toolkit/
│       ├── __init__.py
│       ├── __main__.py      # Точка входа CLI и обработка аргументов 
│       ├── calculator.py    # Логика вычислений и ОПН
│       ├── converter.py     # Функция конвертации
│       ├── errors.py        # Файл с ошибками
│       └── tokenizer.py     # Токенизатор 
├── tests/
│   └── calculator_test.py   # Набор тестов pytest
├── pytest.ini               # Конфигурация pytest
├── .gitignore 
├── pyproject.toml           # Файл с настройками проекта
└── README.md

```


`
