
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import qrcode
from PIL import Image, ImageTk
import os
from datetime import datetime

class QRCodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator Pro")
        self.root.geometry("650x800")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TFrame', background="#f0f0f0")
        self.style.configure('TLabel', background="#f0f0f0", font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TLabelFrame', font=('Arial', 10, 'bold'), background="#f0f0f0")
        self.style.configure('TEntry', font=('Arial', 10), padding=5)
        
        # Create custom button styles
        self.style.configure('Accent.TButton', 
                          foreground='white', 
                          background='#4CAF50',
                          font=('Arial', 10, 'bold'),
                          padding=8)
        self.style.map('Accent.TButton',
                     foreground=[('active', 'black'), ('disabled', 'gray')],
                     background=[('active', '#45a049'), ('disabled', '#cccccc')])
        
        # Variables
        self.data_var = tk.StringVar()
        self.filename_var = tk.StringVar(value="my_qr_code")
        self.fill_color_var = tk.StringVar(value="#000000")  # Black
        self.back_color_var = tk.StringVar(value="#FFFFFF")  # White
        self.logo_path = ""
        self.qr_image = None
        self.qr_photo = None
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(header_frame, text="QR Code Generator Pro", font=('Arial', 16, 'bold'), 
                 background="#f0f0f0").pack()
        
        # Input Section
        input_frame = ttk.LabelFrame(main_frame, text="QR Code Content", padding="15")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(input_frame, text="Enter URL or Text:").pack(anchor=tk.W)
        self.data_entry = ttk.Entry(input_frame, textvariable=self.data_var, width=50)
        self.data_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Settings Section
        settings_frame = ttk.LabelFrame(main_frame, text="QR Code Settings", padding="15")
        settings_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Filename
        ttk.Label(settings_frame, text="File Name:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        ttk.Entry(settings_frame, textvariable=self.filename_var).grid(row=0, column=1, sticky=tk.EW, pady=(0, 10))
        
        # Colors
        ttk.Label(settings_frame, text="Fill Color:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        color_frame = ttk.Frame(settings_frame)
        color_frame.grid(row=1, column=1, sticky=tk.EW)
        ttk.Entry(color_frame, textvariable=self.fill_color_var, width=8).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(color_frame, text="Choose", command=lambda: self.choose_color(self.fill_color_var)).pack(side=tk.LEFT)
        
        ttk.Label(settings_frame, text="Background Color:").grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        bg_color_frame = ttk.Frame(settings_frame)
        bg_color_frame.grid(row=2, column=1, sticky=tk.EW)
        ttk.Entry(bg_color_frame, textvariable=self.back_color_var, width=8).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(bg_color_frame, text="Choose", command=lambda: self.choose_color(self.back_color_var)).pack(side=tk.LEFT)
        
        # Logo
        ttk.Label(settings_frame, text="Add Logo:").grid(row=3, column=0, sticky=tk.W, pady=(0, 10))
        logo_frame = ttk.Frame(settings_frame)
        logo_frame.grid(row=3, column=1, sticky=tk.EW)
        self.logo_btn = ttk.Button(logo_frame, text="Select Logo", command=self.select_logo)
        self.logo_btn.pack(side=tk.LEFT, padx=(0, 5))
        self.clear_logo_btn = ttk.Button(logo_frame, text="Clear", command=self.clear_logo)
        self.clear_logo_btn.pack(side=tk.LEFT)
        
        # Button Frame
        btn_frame = ttk.Frame(main_frame, padding=(0, 15, 0, 0))
        btn_frame.pack(fill=tk.X)
        
        # Generate Button
        self.generate_btn = ttk.Button(
            btn_frame, 
            text="Generate QR Code", 
            command=self.generate_qr, 
            style='Accent.TButton',
            width=20
        )
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Save Button
        self.save_btn = ttk.Button(
            btn_frame, 
            text="Save QR Code", 
            command=self.save_qr,
            width=20
        )
        self.save_btn.pack(side=tk.LEFT)
        
        # QR Code Display
        self.qr_frame = ttk.LabelFrame(main_frame, text="QR Code Preview", padding="15")
        self.qr_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        # Canvas for QR code display
        self.qr_canvas = tk.Canvas(self.qr_frame, bg="white", bd=0, highlightthickness=0)
        self.qr_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure grid weights
        settings_frame.columnconfigure(1, weight=1)
    
    def choose_color(self, color_var):
        color = colorchooser.askcolor(title="Choose color", initialcolor=color_var.get())
        if color[1]:  # User didn't cancel
            color_var.set(color[1])
    
    def select_logo(self):
        self.logo_path = filedialog.askopenfilename(
            title="Select Logo Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if self.logo_path:
            self.logo_btn.config(text=f"Logo: {os.path.basename(self.logo_path)}")
    
    def clear_logo(self):
        self.logo_path = ""
        self.logo_btn.config(text="Select Logo")
    
    def generate_qr(self):
        data = self.data_var.get()
        if not data:
            messagebox.showerror("Error", "Please enter some text or URL to encode")
            return
        
        try:
            # Create basic QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Create image with colors
            img = qr.make_image(
                fill_color=self.fill_color_var.get(),
                back_color=self.back_color_var.get()
            ).convert('RGB')
            
            # Add logo if specified
            if self.logo_path and os.path.exists(self.logo_path):
                logo = Image.open(self.logo_path)
                
                # Calculate logo size (20% of QR code size)
                img_width, img_height = img.size
                logo_size = min(img_width, img_height) // 5
                
                # Resize logo
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                
                # Calculate position to center logo
                pos = ((img_width - logo_size) // 2, (img_height - logo_size) // 2)
                
                # Paste logo on QR code
                img.paste(logo, pos)
            
            # Store the image reference
            self.qr_image = img
            
            # Resize for display while maintaining aspect ratio
            canvas_width = self.qr_canvas.winfo_width() - 20
            canvas_height = self.qr_canvas.winfo_height() - 20
            
            # Calculate the scaling factor
            img_ratio = img.width / img.height
            canvas_ratio = canvas_width / canvas_height
            
            if canvas_ratio > img_ratio:
                # Canvas is wider than image
                new_height = canvas_height
                new_width = int(new_height * img_ratio)
            else:
                # Canvas is taller than image
                new_width = canvas_width
                new_height = int(new_width / img_ratio)
            
            # Resize the image
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert for display in Tkinter
            self.qr_photo = ImageTk.PhotoImage(resized_img)
            
            # Clear canvas and display new image
            self.qr_canvas.delete("all")
            x = (canvas_width - new_width) // 2
            y = (canvas_height - new_height) // 2
            self.qr_canvas.create_image(x, y, anchor=tk.NW, image=self.qr_photo)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")
    
    def save_qr(self):
        if not self.qr_image:
            messagebox.showerror("Error", "Please generate a QR code first")
            return
        
        filename = self.filename_var.get()
        if not filename:
            filename = f"qr_code_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = filedialog.asksaveasfilename(
            title="Save QR Code",
            initialfile=filename,
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                self.qr_image.save(filepath)
                messagebox.showinfo("Success", f"QR code saved successfully at:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR code: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()