############################################################################
## Django ORM Standalone Python Template
############################################################################
""" Here we'll import the parts of Django we need. It's recommended to leave
these settings as is, and skip to START OF APPLICATION section below """

# Turn off bytecode generation
import sys
sys.dont_write_bytecode = True

# Import settings
import os
import random 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

# setup django environment
import django
django.setup()

# Import your models for use in your script
from db.models import *

############################################################################
## START OF APPLICATION
############################################################################
""" Replace the code below with your own """

# Seed a from products.txt file
def seed_from_products_txt(path="products.txt"):
    if not os.path.exists(path):
        print("No products.txt found; skipping seed.")
        return
    created = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            #UPC Product Price, where Product is a single token in your file
            parts = s.split()
            if len(parts) < 3:
                continue
            upc = parts[0]
            name = parts[1]
            price_raw = " ".join(parts[2:]).replace("$", "").strip()
            try:
                price = Decimal(price_raw)
            except Exception:
                continue
            _, was_created = Product.objects.get_or_create(
                upc=upc,
                defaults={"name": name, "price": price}
            )
            if was_created:
                created += 1
    print(f"Seed complete. Created {created} new products. Total: {Product.objects.count()}")

# --- Cash Register logic (ORM-backed) ---
class CashRegister:
    def __init__(self):
        self.scanned = []  # list[Product]
        self.rnd = random.Random()

    def get_all_upcs(self):
        return list(Product.objects.values_list("upc", flat=True))

    def get_random_upc(self):
        upcs = self.get_all_upcs()
        if not upcs:
            return None
        return self.rnd.choice(upcs)

    def find_by_upc(self, upc):
        try:
            return Product.objects.get(upc=upc)
        except Product.DoesNotExist:
            return None

    def add_by_upc(self, upc):
        p = self.find_by_upc(upc)
        if p:
            self.scanned.append(p)
        return p

    def get_subtotal(self):
        total = sum((p.price for p in self.scanned), Decimal("0.00"))
        # round like display: two decimals
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

# Tkinter UI (Display + Scanner) 
import tkinter as tk
from tkinter import ttk
from decimal import Decimal, ROUND_HALF_UP

class DisplayUI:
    def __init__(self, master, title="Cash Register Display"):
        self.frame = tk.Toplevel(master)
        self.frame.title(title)
        self.listbox = tk.Listbox(self.frame, width=48, height=12)
        self.listbox.pack(padx=8, pady=8)
        self.subtotal_var = tk.StringVar(value="Subtotal: $0.00")
        tk.Label(self.frame, textvariable=self.subtotal_var).pack(padx=8, pady=(0,8))

    def add_line(self, text):
        self.listbox.insert(tk.END, text)

    def set_subtotal(self, value: Decimal):
        self.subtotal_var.set(f"Subtotal: ${value:.2f}")

class ScannerUI:
    def __init__(self, master, on_scan, get_random_upc):
        self.frame = tk.Toplevel(master)
        self.frame.title("Scanner")
        container = ttk.Frame(self.frame, padding=8)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Enter/Scan UPC (leave blank to select a random product):").grid(row=0, column=0, sticky="w")
        self.upc_var = tk.StringVar()
        self.entry = ttk.Entry(container, textvariable=self.upc_var, width=28)
        self.entry.grid(row=1, column=0, sticky="we", pady=(4,6))

        btns = ttk.Frame(container)
        btns.grid(row=2, column=0, sticky="we")
        scan_btn = ttk.Button(btns, text="Scan", command=lambda: on_scan(self.current_upc(get_random_upc)))
        scan_btn.pack(side="left")

        # focus quality of life
        self.entry.focus_set()

    def current_upc(self, get_random_upc):
        code = self.upc_var.get().strip()
        if code:
            self.upc_var.set("")  # clear after use
            return code
        # fall back to randomly generating a UPC
        return get_random_upc()

def main():
    seed_from_products_txt()  # safe if run multiple times
    register = CashRegister()

    root = tk.Tk()
    root.withdraw()  # hide root window; use Toplevels

    display = DisplayUI(root, "Cash Register Display")
    def handle_scan(upc):
        if not upc:
            # no products in DB
            display.add_line("(no UPCs available)")
            return
        p = register.add_by_upc(upc)
        if p:
            # Match Assignemnt 2 formatting via Product.__str__()
            display.add_line(str(p))
            display.set_subtotal(register.get_subtotal())
        else:
            display.add_line(f"{upc} (unknown)")

    scanner = ScannerUI(root, on_scan=handle_scan, get_random_upc=register.get_random_upc)

    # keep windows open
    root.mainloop()

if __name__ == "__main__":
    main()