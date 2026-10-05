from typing import Union

import flet as ft


def border_all(width: Union[int, float], color: str) -> ft.Border:
    """Create a uniform border on all four sides."""
    return ft.Border(
        left=ft.BorderSide(width, color),
        right=ft.BorderSide(width, color),
        top=ft.BorderSide(width, color),
        bottom=ft.BorderSide(width, color),
    )
