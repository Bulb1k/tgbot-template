from .consts import DefaultConstructor
from texts import keyboards

menu_kb = DefaultConstructor.create_kb(
    actions=[
        keyboards.MY_PROFILE,
        keyboards.SETTINGS,
    ],
    schema=[1, 1]
)