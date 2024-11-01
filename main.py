from pystray import Icon, Menu, MenuItem
from PIL import Image

logo = Image.open('icone.png').convert('RGBA')

icon = Icon(
    'DNS Updater',
    icon=logo,
    title='DNS Updater',
    menu=Menu(
    MenuItem(
        'Update now',
    ),
    MenuItem(
        'Settings',
    ),
    MenuItem(
        'Exit',
        lambda icon, item: icon.stop()
    )
    )
).run()