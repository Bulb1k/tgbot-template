from texts.keyboards import CANCEL
from .consts import DefaultConstructor

cancel_kb = DefaultConstructor.create_kb(
    actions=[CANCEL],
    schema=[1]
)
