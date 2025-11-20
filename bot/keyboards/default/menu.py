from texts import keyboards
from .consts import DefaultConstructor

menu_kb = DefaultConstructor.create_kb(
    actions=[
        keyboards.MY_PROFILE,
        keyboards.SETTINGS,
    ],
    schema=[1, 1]
)
