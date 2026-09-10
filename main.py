from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
import json
import os

try:
    import qrcode
    HAS_QR = True
except ImportError:
    HAS_QR = False

FILE_NAME = "thomas_products.json"
MERCHANT_PHONE = "01207193239"

class ThomasApp(App):
    def build(self):
        self.products = self.load_data()
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Header
        self.header = Label(
            text=f"Thomas Supermarket\nWallet: {MERCHANT_PHONE}", 
            font_size='18sp', 
            halign='center',
            size_hint=(1, 0.15)
        )
        layout.add_widget(self.header)
        
        # Input Fields
        self.item_input = TextInput(
            hint_text="Product Name", 
            multiline=False, 
            size_hint=(1, None), 
            height=45
        )
        layout.add_widget(self.item_input)
        
        self.price_input = TextInput(
            hint_text="Price (New Item)", 
            multiline=False, 
            input_filter='float',
            size_hint=(1, None), 
            height=45
        )
        layout.add_widget(self.price_input)
        
        self.qty_input = TextInput(
            hint_text="Quantity", 
            multiline=False, 
            input_filter='int', 
            size_hint=(1, None), 
            height=45
        )
        layout.add_widget(self.qty_input)
        
        # Payment Method Dropdown
        self.payment_spinner = Spinner(
            text="Select Payment Method",
            values=("Cash", "Vodafone Cash", "Orange Cash", "WE Pay", "Fawry"),
            size_hint=(1, None),
            height=45,
            background_color=(0.1, 0.5, 0.6, 1)
        )
        layout.add_widget(self.payment_spinner)
        
        # Buttons
        btn_layout = BoxLayout(spacing=10, size_hint=(1, None), height=50)
        
        sell_btn = Button(text="Sell / Pay", background_color=(0.2, 0.7, 0.3, 1))
        sell_btn.bind(on_press=self.sell_action)
        btn_layout.add_widget(sell_btn)
        
        add_btn = Button(text="Add Product", background_color=(0.2, 0.5, 0.8, 1))
        add_btn.bind(on_press=self.add_action)
        btn_layout.add_widget(add_btn)
        
        stock_btn = Button(text="View Stock", background_color=(0.8, 0.5, 0.2, 1))
        stock_btn.bind(on_press=self.view_stock)
        btn_layout.add_widget(stock_btn)
        
        layout.add_widget(btn_layout)
        
        # QR Display Widget
        self.qr_image = Image(
            size_hint=(1, 0.35),
            allow_stretch=True,
            keep_ratio=True
        )
        layout.add_widget(self.qr_image)
        
        # Status Bar
        self.status_label = Label(
            text="Welcome to Thomas System", 
            font_size='14sp',
            size_hint=(1, 0.15)
        )
        layout.add_widget(self.status_label)
        
        return layout

    def load_data(self):
        if os.path.exists(FILE_NAME):
            try:
                with open(FILE_NAME, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"Cheese": [25.0, 10], "Milk": [15.0, 20]}

    def save_data(self):
        try:
            with open(FILE_NAME, "w", encoding="utf-8") as f:
                json.dump(self.products, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("Save Error:", e)

    def generate_qr(self, payment_method, total_amount):
        if not HAS_QR:
            self.status_label.text = "Error: Install Pillow / qrcode library"
            return False
            
        try:
            qr_data = f"Method: {payment_method}\nTo: {MERCHANT_PHONE}\nAmount: {total_amount} EGP"
            qr = qrcode.make(qr_data)
            
            qr_path = "temp_qr.png"
            qr.save(qr_path)
            
            self.qr_image.source = qr_path
            self.qr_image.reload()
            return True
        except Exception as e:
            self.status_label.text = f"QR Error: {str(e)}"
            return False

    def sell_action(self, instance):
        item = self.item_input.text.strip()
        qty_str = self.qty_input.text.strip()
        payment_method = self.payment_spinner.text
        
        if payment_method == "Select Payment Method":
            self.status_label.text = "Please select a payment method!"
            return

        if item in self.products and qty_str.isdigit():
            qty = int(qty_str)
            if qty <= self.products[item][1]:
                total = qty * self.products[item][0]
                
                if payment_method != "Cash":
                    if self.generate_qr(payment_method, total):
                        self.products[item][1] -= qty
                        self.save_data()
                        self.status_label.text = f"Scan QR to pay {total} EGP via {payment_method}"
                        self.clear_inputs()
                else:
                    self.products[item][1] -= qty
                    self.save_data()
                    self.qr_image.source = ""
                    self.status_label.text = f"Sold: {qty} x {item} | Total: {total} EGP (Cash)"
                    self.clear_inputs()
            else:
                self.status_label.text = f"Insufficient stock! Available: {self.products[item][1]}"
        else:
            self.status_label.text = "Invalid item name or quantity!"

    def add_action(self, instance):
        item = self.item_input.text.strip()
        price_str = self.price_input.text.strip()
        qty_str = self.qty_input.text.strip()
        
        if item and price_str and qty_str.isdigit():
            price = float(price_str)
            qty = int(qty_str)
            self.products[item] = [price, qty]
            self.save_data()
            self.status_label.text = f"Added {item} | Price: {price} EGP | Qty: {qty}"
            self.clear_inputs()
        else:
            self.status_label.text = "Please enter valid Name, Price, and Quantity!"

    def view_stock(self, instance):
        self.qr_image.source = ""
        stock_text = "--- Current Stock ---\n"
        for item, info in self.products.items():
            stock_text += f"{item}: {info[0]} EGP | Stock: {info[1]}\n"
        self.status_label.text = stock_text

    def clear_inputs(self):
        self.item_input.text = ""
        self.price_input.text = ""
        self.qty_input.text = ""
        self.payment_spinner.text = "Select Payment Method"

if __name__ == '__main__':
    ThomasApp().run()
