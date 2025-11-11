[![Q2 here]([https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg](https://docs.google.com/document/d/1L-s9s19BQOKfgrm2tnJvWxjtgAwN1mSLKELJnmP6k4A/edit?tab=t.0))]
Assignment 3 – Cash Register using Django ORM
=====================

**Course:** <SOFE 3650>  
**Group:** Group 16 – CRN 45740  
**Author(s):** Samuel Ajoku , Omar Ahmed , Zeyad Ghazal 

This small, **standalone Python app** uses **Django ORM** (without a web server) to:
1) **Populate** an SQLite database with product **UPC, name, price**  
2) **Scan** a product via a GUI **input box** and **display** its name & price  
3) Maintain a running **Subtotal** (that matches follow the cash register requirements and follows a similar behavior as in Assignment 2)

:open_file_folder: Updated File Structure
---------------------------------
```
django-orm/
├── db/
│   ├── __init__.py
│   └── models.py
├── main.py
├── manage.py
├── README.md
├── settings.py
├── ScreenDumps/
│   ├── screen1.png
│   ├── screen2.png
│   ├── screen3.png
│   ├── screen4.png
│   └── screen5.png
└── products.txt
```

### Where we configured **Django ORM** using Django models
- **Model:** `db/models.py`
  ```python
  class Product(models.Model):
      upc = models.CharField(max_length=32, unique=True)
      name = models.CharField(max_length=120)
      price = models.DecimalField(max_digits=10, decimal_places=2)
  
- **Migrations:** created/applied via python3 manage.py makemigrations db and python3 manage.py migrate.
- **Querries:** in main.py

:rocket: How to Run after cloning repo locally (using macOS)
--------------------
# From repo root
```
python3 -m venv venv
venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install django
```

# To initialize DB schema
```
python3 manage.py makemigrations db
python3 manage.py migrate
```

# To run the app
```
python3 main.py
```

**NB:** "python 3 used because of python version



📸: Screen Dumps
----------------------

**1. DB populated (seed complete)**
    : Terminal output showing seed count and totals.
    ![Seed complete](ScreenDumps/screen1.png)


    
**2. Scan – known UPC (displays name & price)**
    : Scanner window after entering 11111 (or any UPC from products.txt).
    ![Known UPC](ScreenDumps/screen2.png)
    

    
**3. Scan – unknown UPC**
    : Enter a UPC not in DB; Display shows 31214 (unknown)
    ![Unknown UPC](ScreenDumps/screen3.png)


    
**4. Scan – without entering a UPC**
    : Click scan without typing a UPC; Generates a random UPC from DB
    ![Clear UPC](ScreenDumps/screen4.png)
    

    
**5. Subtotal updates after multiple scans**
    : Display shows multiple lines and Subtotal updated.
    ![Subtotal](ScreenDumps/screen5.png)
    

🧠: main.py- Application Logic Overview
----------------------
The main.py file contains the entire functional logic of the cash register system.
It brings together **database population, Django ORM usage**, and the **Tkinter GUI** (Scanner + Display), mirroring the MVC-style behavior from Assignment 2 but implemented with Django’s ORM instead of in-memory data.

**1. Setup and initialization**
```pyhton
import os, django, random
from decimal import Decimal, ROUND_HALF_UP
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()
from db.models import Product
```
-Loads Django’s environment so ORM commands (like Product.objects.get_or_create) can be used without running a Django web server.

-Imports Product from db/models.py – this is the model that maps directly to the SQLite table db_product.

-Initializes Python’s random library for optional random UPC scanning.

**2. Database  Population (seeds from products.txt)**
```pyhton
def seed_from_products_txt(path="products.txt"):
    "lines 30-49"
    Product.objects.get_or_create(upc=upc, defaults={"name": name, "price": price})
```
-Reads product data from products.txt.

-Uses the Django ORM method get_or_create() to insert rows into the database if they don’t already exist.

-Ensures the table is always populated before the GUI runs.

-Prints a summary such as:

-Seed complete. Created 4 new products. Total: 4

-This directly satisfies part (a) of the assignment:

“Populating the DB with product UPC codes, names, and prices.”

**3. Cash Register Logic**
```pyhton
class CashRegister:
    def add_by_upc(self, upc):
        p = self.find_by_upc(upc)
        if p:
            self.scanned.append(p)
        return p
```
-Keeps track of all scanned products (self.scanned list).

-Retrieves product information using Django ORM queries:

-Product.objects.get(upc=upc)

-Calculates the subtotal using Python’s Decimal for precision.

-Returns None when a UPC isn’t found (triggers “(unknown)” in the display).

**4. Tkinter GUI**

ScannerUI class
```pyhton
def current_upc(self, get_random_upc):
    code = self.upc_var.get().strip()
    return code or get_random_upc()
```
-Provides an input box to type or “scan” a UPC.

-If left blank, automatically picks a random product.

-On button click, calls a handler in main() that queries the ORM for the product.

DisplayUI class
```pyhton
self.listbox.insert(tk.END, text)
self.subtotal_var.set(f"Subtotal: ${value:.2f}")
```
-Shows scanned items line-by-line.

-Displays the running subtotal at the bottom.

**5. Main Function**
  ```python
def main():
    seed_from_products_txt()
    register = CashRegister()
    ...
    ScannerUI(root, on_scan=handle_scan, get_random_upc=register.get_random_upc)
  ``` 
-Seeds the database first.

-Creates the CashRegister, DisplayUI, and ScannerUI objects.

-Defines handle_scan() which:

    Looks up a product in the database.
    
    Updates the display with UPC name $price or UPC (unknown).
    
    Updates the subtotal.



📖: Design Notes
----------------------

Same behavior as Assignment 2 (Swing/MVC), now using Django ORM:

-Input box acts as a scanner (blank input triggers a random UPC).

-Display line format: UPC name $price.

-Unknown barcode: UPC (unknown).

-Running subtotal at the bottom.
