import customtkinter as ctk
import api_module, json

ctk.set_default_color_theme("color_theme.json")
ctk.set_appearance_mode("system")

class Domains(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.load_domains()

    def load_domains(self):
        try:
            with open("settings.json", "r") as f:
                data = json.load(f)
                domains = data.get("domains", [])

                for index, domain in enumerate(domains):
                    domain_label = ctk.CTkLabel(self, text=f"Domain {index + 1}: {domain['DOMAIN']}")
                    domain_label.grid(row=index, column=0, padx=10, pady=5, sticky="w")
                    
                    ttl_label = ctk.CTkLabel(self, text=f"TTL: {domain['TTL_TIME']}, Proxy: {domain['PROXY_TYPE']}")
                    ttl_label.grid(row=index, column=1, padx=10, pady=5, sticky="w")

        except FileNotFoundError:
            print(f"erro")

class AddDomain(ctk.CTk): 
    def __init__(self):
        super().__init__()
        self.title("Add New Domain")       
        self.geometry("400x400")

        for i in range(8):  
            self.grid_rowconfigure(i, weight=1, pad=5)
        self.grid_columnconfigure(0, weight=1, pad=5)
        self.grid_columnconfigure(1, weight=3, pad=5)

        self.create_label_entry("DNS Record ID:", 0)
        self.create_label_entry("Zone ID ():", 1)
        self.create_label_entry("Comment (leave empty if prefer):", 2)
        self.create_label_entry("Domain (example.com):", 3)
        
        ctk.CTkLabel(self, text="Proxy Type (True/False):").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.proxy_type_var = ctk.StringVar(value="True")
        self.combo_type_var = ctk.CTkComboBox(self, values=["True", "False"], variable=self.proxy_type_var)
        self.combo_type_var.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        self.create_label_entry("TTL Time (set 1 for Auto):", 5)
        self.create_label_entry("Type (A, AAAA, CNAME, etc.):", 6)
        self.create_label_entry("Email Token:", 7)

        submit_button = ctk.CTkButton(self, text="Submit Domain", command=self.submit_callback)
        submit_button.grid(row=8, column=0, columnspan=2, pady=20)

    def create_label_entry(self, label_text, row):
        label = ctk.CTkLabel(self, text=label_text)
        label.grid(row=row, column=0, sticky="e", padx=10, pady=5)
        
        entry = ctk.CTkEntry(self)
        entry.grid(row=row, column=1, sticky="w", padx=10, pady=5)
        
        setattr(self, f"entry_{label_text.lower().replace(' ', '_').replace(':', '')}", entry)

    def submit_callback(self):
        new_domain = {
            "DNS_RECORD_ID": self.entry_dns_record_id.get(),
            "ZONE_ID": self.entry_zone_id.get(),
            "COMMENT": self.entry_comment.get(),
            "DOMAIN": self.entry_domain.get(),
            "PROXY_TYPE": self.proxy_type_var.get(),
            "TTL_TIME": int(self.entry_ttl_time.get()),
            "TYPE": self.entry_type.get(),
            "EMAIL_TOKEN": self.entry_email_token.get()
        }
        api_module.saveData("domains", new_domain, "append")
        self.destroy()


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x300")
        self.title("Cloudflare DDNS Settings")

        self.data = {"ip": "", "interval": "", "globalkey": "", "notifications": "", "domains": []}

        self.label_globalkey= ctk.CTkLabel(self, text="Global API Key: ")
        self.label_globalkey.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_globalkey = ctk.CTkEntry(self, width=300, height=40, corner_radius=10, placeholder_text="Enter your Global API Key")
        self.entry_globalkey.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        self.label_notifications = ctk.CTkLabel(self, text="Enable notifications:")
        self.label_notifications.grid(row=1, column=0, padx=10, pady=20, sticky="e")
        self.notifications_var = ctk.StringVar(value="True")
        self.checkbox_notifications = ctk.CTkCheckBox(self, text="", command=self.checkbox_notifications_event, variable=self.notifications_var, onvalue=True, offvalue=False)
        self.checkbox_notifications.grid(row=1, column=1, padx=0, pady=20, sticky="w")
        
        self.domainsFrame = Domains(master=self, width=300, height=200, corner_radius=0, fg_color="transparent")
        self.domainsFrame.grid(row=2, column=0, sticky="nsew")

        self.adddomain_dialog = ctk.CTkButton(self, text="Add new domain", command=self.open_addnewdomain_callback)
        self.adddomain_dialog.grid(row=3, column=0, padx=10, pady=20, sticky="e")

        self.confirm_button = ctk.CTkButton(self, text="Confirm", command=self.confirm_callback)
        self.confirm_button.grid(row=4, column=0, padx=10, pady=30, sticky="e")
        
        self.exit_button = ctk.CTkButton(self, text="Exit", command=self.exit_callback)
        self.exit_button.grid(row=4, column=1, padx=10, pady=30, sticky="w")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.loadAllData()

    def loadAllData(self):
        global_data = api_module.loadData("globalkey")
        if global_data:
            self.entry_globalkey.insert(0, global_data)
            self.data["globalkey"] = global_data

        notifications_data = api_module.loadData("notifications")
        if notifications_data:
            self.notifications_var.set(notifications_data)
            self.checkbox_notifications.setvar(notifications_data)
            self.data["notifications"] = notifications_data
    
    def open_addnewdomain_callback(self):
        adddomain = AddDomain()
        adddomain.mainloop()
    def checkbox_notifications_event(self):
        self.data["notifications"] = self.notifications_var.get()
    def confirm_callback(self):
        api_module.saveData("globalkey", self.data["globalkey"], "update")
        api_module.saveData("notifications", self.data["notifications"], "update")
    def exit_callback(self):
        self.destroy()