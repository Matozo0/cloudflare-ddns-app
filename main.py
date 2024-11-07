from app_module import Application
from api_module import loadData, loadDomainsandUpdate, resource_path
from pystray import Icon, Menu, MenuItem
from PIL import Image
from datetime import datetime, timedelta
from timeloop import Timeloop

app_icon = Image.open(resource_path("icons/icon.ico")).convert("RGBA")
app = None
last_update = None
next_update = None
tl = Timeloop()

@tl.job(interval=timedelta(seconds=int(loadData("interval"))*60))
def update():
    global last_update, next_update

    loadDomainsandUpdate(icon)
    last_update = datetime.now()
    print(f"Last Update: {last_update}")
    next_update = last_update + timedelta(seconds=int(loadData("interval"))*60)
    print(f"Next Update: {next_update}")

def update_now_item(icon, item):
    global last_update
    loadDomainsandUpdate(icon)
    last_update = datetime.now()
    print(f"Manual Update: {last_update}")

def on_close():
    global app
    app = None 

def open_settings(icon, item):
    global app
    if app is None:
        app = Application(on_exit_callback=on_close)
        app.mainloop()
    else:
        app.lift() 

def exit_app(icon, item):
    global app, tl
    if app is not None:
        app.destroy()
    app = None
    tl.stop()
    icon.stop() 

icon = Icon(
    "DNS Updater",
    icon=app_icon,
    title="DNS Updater",
    menu=Menu(
        MenuItem("Settings", open_settings, default=True),
        MenuItem("Update now", update_now_item),        
        MenuItem("Exit", exit_app)
    )
)

if __name__ in '__main__':
    tl.start()
    icon.run()