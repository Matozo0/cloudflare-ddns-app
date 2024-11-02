import customtkinter as ctk
import api_module, json
from tkinter import messagebox
from PIL import Image

ctk.set_default_color_theme("color_theme.json")
ctk.set_appearance_mode("light")

class IntervalWidget(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, bg_color="transparent")

        self.entry = ctk.CTkEntry(self, width=50, justify="center")
        self.entry.insert(0, "1")
        self.entry.grid(row=0, column=2, padx=5)

        self.button_increase = ctk.CTkButton(self, text="+", width=20, command=self.increase)
        self.button_increase.grid(row=0, column=3, padx=(5, 10))

        self.button_decrease = ctk.CTkButton(self, text="-", width=20, command=self.decrease)
        self.button_decrease.grid(row=0, column=1, padx=(10, 5))

    def increase(self):
        current_value = int(self.entry.get())
        self.entry.delete(0, ctk.END)
        self.entry.insert(0, str(current_value + 1))

    def decrease(self):
        current_value = int(self.entry.get())
        if current_value > 1: 
            self.entry.delete(0, ctk.END)
            self.entry.insert(0, str(current_value - 1))      

class Domains(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, label_text="Domains", **kwargs)
        self.switch_vars = []
        self.load_domains()

    def switch_enable_event(self, index):
        is_enabled = self.switch_vars[index].get()

    def delete_domain_event(self, data, target_domain):
        data["domains"] = [domain for domain in data["domains"] if domain.get("DNS_RECORD_ID") != target_domain["DNS_RECORD_ID"]]
        with open("settings.json", "w") as f:
            json.dump(data, f, indent=4)
        self.load_domains()

    def load_domains(self):
        for widgets in self.winfo_children():
            widgets.destroy()

        try:
            with open("settings.json", "r") as f:
                data = json.load(f)
                domains = data.get("domains", [])

                for index, domain in enumerate(domains):
                    label_domain = ctk.CTkLabel(self, text=f"Domain {index + 1}: {domain['DOMAIN']}")
                    label_domain.grid(row=index, column=0, padx=10, pady=5, sticky="w")
                    label_ttl = ctk.CTkLabel(self, text=f"TTL: {domain['TTL_TIME']}")
                    label_ttl.grid(row=index, column=1, padx=10, pady=5, sticky="w")
                    label_proxy = ctk.CTkLabel(self, text=f"Proxy: {domain['PROXY_TYPE']}")
                    label_proxy.grid(row=index, column=2, padx=10, pady=5, sticky="w")
                    label_type = ctk.CTkLabel(self, text=f"Type: {domain['TYPE']}")
                    label_type.grid(row=index, column=3, padx=10, pady=5, sticky="w")

                    switch_enable_var = ctk.BooleanVar(value=domain['ENABLE'])
                    self.switch_vars.append(switch_enable_var)
                    switch_enable = ctk.CTkSwitch(self, text="Enable", command=self.switch_enable_event(index), variable=switch_enable_var, onvalue=True, offvalue=False)
                    switch_enable.grid(row=index, column=4, padx=10, pady=5, sticky="w")

                    button_delete = ctk.CTkButton(self, text="", command=lambda data=data, domain=domain: self.delete_domain_event(data, domain), image=ctk.CTkImage(Image.open("delete.png")), width=32, height=32)
                    button_delete.grid(row=index, column=5, padx=0, pady=5, sticky="w")

        except FileNotFoundError:
            print(f"erro")

class AddDomain(ctk.CTk): 
    def __init__(self, domains_frame):
        super().__init__()
        self.domains_frame = domains_frame
        self.title("Add New Domain")       
        self.geometry("400x400")
        self.iconbitmap("icon.ico")

        for i in range(8):  
            self.grid_rowconfigure(i, weight=1, pad=5)
        self.grid_columnconfigure(0, weight=1, pad=5)
        self.grid_columnconfigure(1, weight=3, pad=5)

        self.create_label_entry("entry_dns_record_id", "DNS Record ID:", 0)
        self.create_label_entry("entry_zone_id", "Zone ID:", 1)
        self.create_label_entry("entry_comment", "Comment (leave empty if prefer):", 2)
        self.create_label_entry("entry_domain", "Domain (example.com):", 3)
        
        ctk.CTkLabel(self, text="Proxy Type (True/False):").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.proxy_type_var = ctk.StringVar(value="True")
        self.combo_type_var = ctk.CTkComboBox(self, values=["True", "False"], variable=self.proxy_type_var)
        self.combo_type_var.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        self.create_label_entry("entry_ttl_time", "TTL Time (set 1 for Auto):", 5)
        self.create_label_entry("entry_type", "Type (A, AAAA, CNAME, etc.):", 6)
        self.create_label_entry("entry_email", "Email Token (your email account ):", 7)

        submit_button = ctk.CTkButton(self, text="Submit Domain", command=self.submit_callback)
        submit_button.grid(row=8, column=0, columnspan=2, pady=20)

    def create_label_entry(self, entry_name, label_text, row):
        label = ctk.CTkLabel(self, text=label_text)
        label.grid(row=row, column=0, sticky="e", padx=10, pady=5)
        
        entry = ctk.CTkEntry(self)
        entry.grid(row=row, column=1, sticky="w", padx=10, pady=5)
        
        setattr(self, entry_name, entry)

    def submit_callback(self):
        try:
            new_domain = {
                "ENABLE": True,
                "DNS_RECORD_ID": self.entry_dns_record_id.get(),
                "ZONE_ID": self.entry_zone_id.get(),
                "COMMENT": self.entry_comment.get(),
                "DOMAIN": self.entry_domain.get(),
                "PROXY_TYPE": self.proxy_type_var.get(),
                "TTL_TIME": int(self.entry_ttl_time.get()),
                "TYPE": self.entry_type.get(),
                "EMAIL_TOKEN": self.entry_email.get()
            }

            api_module.saveData("domains", new_domain, "append")
            self.domains_frame.load_domains()
            self.destroy() 
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid TTL time.")
        except Exception as e:
            messagebox.showerror("Submission Error", f"An error occurred: {e}")

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("650x525")
        self.title("Cloudflare DDNS Settings")
        self.iconbitmap("icon.ico")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.data = {"ip": "", "interval": "", "globalkey": "", "notifications": "", "domains": []}

        self.label_globalkey= ctk.CTkLabel(self, text="Global API Key: ")
        self.label_globalkey.grid(row=0, column=0, padx=10, pady=0, sticky="e")
        self.entry_globalkey = ctk.CTkEntry(self, width=300, height=30, corner_radius=10, placeholder_text="Enter your Global API Key")
        self.entry_globalkey.grid(row=0, column=1, padx=10, pady=0, sticky="w")
        
        self.label_interval = ctk.CTkLabel(self, text="Select interval minutes:")
        self.label_interval.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.frame_interval = IntervalWidget(self)
        self.frame_interval.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label_notifications = ctk.CTkLabel(self, text="Enable notifications:")
        self.label_notifications.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.notifications_var = ctk.BooleanVar(value=False)
        self.checkbox_notifications = ctk.CTkCheckBox(self, text="", variable=self.notifications_var, onvalue=True, offvalue=False)
        self.checkbox_notifications.grid(row=2, column=1, padx=0, pady=10, sticky="w")
        
        self.domainsFrame = Domains(master=self, width=300, height=200)
        self.domainsFrame.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="nsew")

        self.adddomain_dialog = ctk.CTkButton(self, text="Add new domain", command=self.open_addnewdomain_callback)
        self.adddomain_dialog.grid(row=4, column=0, columnspan=2, padx=(10, 0), pady=10)

        self.frame_buttons_confirm_exit = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_buttons_confirm_exit.grid(row=5, column=0, columnspan=2, sticky="ew")

        self.frame_buttons_confirm_exit.grid_columnconfigure(0, weight=1)
        self.frame_buttons_confirm_exit.grid_columnconfigure(1, weight=1)

        self.confirm_button = ctk.CTkButton(self.frame_buttons_confirm_exit, text="Confirm", command=self.confirm_callback)
        self.confirm_button.grid(row=0, column=0, padx=10, pady=20, sticky="e")
        
        self.exit_button = ctk.CTkButton(self.frame_buttons_confirm_exit, text="Exit", command=self.exit_callback)
        self.exit_button.grid(row=0, column=1, padx=10, pady=20, sticky="w")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.loadAllData()

    def loadAllData(self):
        global_data = api_module.loadData("globalkey")
        if global_data:
            self.entry_globalkey.insert(0, global_data)
            self.data["globalkey"] = global_data

        notifications_data = api_module.loadData("notifications")
        self.notifications_var.set(value=notifications_data)
        self.data["notifications"] = notifications_data
    
    def open_addnewdomain_callback(self):
        adddomain = AddDomain(self.domainsFrame)
        adddomain.mainloop()

    def confirm_callback(self):
        self.data["globalkey"] = self.entry_globalkey.get()
        self.data["notifications"] = self.notifications_var.get()
        self.data["interval"] = int(self.frame_interval.entry.get())

        api_module.saveData("globalkey", self.data["globalkey"], "update")
        api_module.saveData("interval", self.data["interval"], "update")
        api_module.saveData("notifications", self.data["notifications"], "update")

    def exit_callback(self):
        self.destroy()