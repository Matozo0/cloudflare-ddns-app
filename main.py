import app_module, api_module
from pystray import Icon, Menu, MenuItem
from PIL import Image

app = None
logo = Image.open('icon.png').convert('RGBA')

def update_now(icon, item):
    print("update")

def open_settings(icon, item):
    global app
    if app is None or not app.winfo_exists():
        app = app_module.Application()
        app.mainloop()

def exit_app(icon, item):
    global app
    if app is not None and app.winfo_exists():
        app.destroy()
    icon.stop()

icon = Icon(
    'DNS Updater',
    icon=logo,
    title='DNS Updater',
    menu=Menu(
    MenuItem('Update now', update_now),
    MenuItem('Settings', open_settings, default=True),
    MenuItem('Exit', exit_app)
    )
).run()