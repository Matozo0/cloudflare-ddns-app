import app_module, api_module
from pystray import Icon, Menu, MenuItem
from PIL import Image

app = None
logo = Image.open('icon.png').convert('RGBA')

def update_now(icon, item):
    api_module.loadDomainsandUpdate()

def open_settings(icon, item):
    global app
    if app is None:
        app = app_module.Application()
        app.protocol("WM_DELETE_WINDOW", on_close)
        app.mainloop()
    else:
        app.lift() 

def on_close():
    global app
    if app is not None:
        app.destroy()
        app = None 

def exit_app(icon, item):
    global app
    if app is not None:
        app.destroy()
    app = None  
    icon.stop()

icon = Icon(
    'DNS Updater',
    icon=logo,
    title='DNS Updater',
    menu=Menu(
        MenuItem('Settings', open_settings, default=True),
        MenuItem('Update now', update_now),        
        MenuItem('Exit', exit_app)
    )
)

icon.run()