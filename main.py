from app_module import Application
from api_module import loadData, loadDomainsandUpdate, resource_path
from pystray import Icon, Menu, MenuItem
from PIL import Image
from threading import Thread, Event
from datetime import datetime, timedelta

app = None
logo = Image.open(resource_path("icon.ico")).convert("RGBA")
stop_event = Event()
last_update = None
next_update = None

def update_now_item(icon, item):
    global last_update

    update()

def update():
    global last_update, icon

    status_code = loadDomainsandUpdate()
    if status_code == 200 and loadData("notifications"):
        icon.notify("Domains updated successfully!", "DNS Updater")
    elif status_code != 200 and loadData("notifications"):
        icon.notify("Domains not updated!", "DNS Updater") 
    last_update = datetime.now()

def periodic_update():
    global last_update, next_update
    update_interval = int(loadData("interval"))*60

    while not stop_event.is_set():
        update()
        
        last_update = datetime.now()
        print(f"Last Update: {last_update}")
        next_update = last_update + timedelta(seconds=update_interval)
        print(f"Next Update: {next_update}")
        stop_event.wait(update_interval)
        update_interval = int(loadData("interval"))*60

def start_periodic_update():
    update_thread = Thread(target=periodic_update, daemon=True)
    update_thread.start()

def on_close():
    global app
    app = None 

def open_settings(icon, item):
    global app
    if app is None:
        app = Application(on_exit_callback=on_close)
        app.protocol("WM_DELETE_WINDOW", on_close)
        app.mainloop()
    else:
        app.lift() 

def exit_app(icon, item):
    global app
    if app is not None:
        app.destroy()
    app = None
    stop_event.set()
    icon.stop() 

icon = Icon(
    "DNS Updater",
    icon=logo,
    title="DNS Updater",
    menu=Menu(
        MenuItem("Settings", open_settings, default=True),
        MenuItem("Update now", update_now_item),        
        MenuItem("Exit", exit_app)
    )
)

icon.run_detached = start_periodic_update
icon.run()