import tkinter as tk
from tkinter import filedialog, ttk
from PIL import ImageTk, ImageFont
from WaterMarkBrain import WaterMarkBrain

class WaterMarkGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark Tool")

        # Initialize WaterMarkBrain
        self.watermark = WaterMarkBrain()

        # Default Watermark settings
        self.text = "Your watermark"
        self.font_size = 24
        self.opacity = 100
        self.rotation = 45
        self.spacing = 30
        self.font = self.load_font()

        # Create UI
        self.setup_ui()

    def load_font(self):
        """Load font with current size"""
        try:
            return ImageFont.truetype("arial.ttf", self.font_size)
        except:
            print("Error loading font. Font loaded using default")
            return ImageFont.load_default()

    def setup_ui(self):
        """Configure the user interface"""
        # Main frames
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True) #expand widget to fill window

        # 7 frames inside Main_frame: Preview, Function, Image, Watermark txt, Sliders, Buttons

        # Preview frame
        preview_frame = ttk.Frame(main_frame, width=400, height=400) #keep smaller frames inside main frame
        preview_frame.pack(side="left", fill="both", padx=5, pady=5)
        preview_frame.pack_propagate(False) #keep frame from shrinking

        self.canvas = tk.Canvas(preview_frame, width=400, height=400, bg='white')
        self.canvas.pack()
        self.canvas.create_text(200, 200, text="Image Preview", fill="gray")


        # Function frame
        function_frame = ttk.Frame(main_frame)
        function_frame.pack(side="right", fill="both", expand=True)

        # Image frame
        img_frame = ttk.LabelFrame(function_frame, text="Image Selection", padding="10")
        img_frame.pack(fill="x", pady=5)

        ttk.Button(img_frame, text="Browse", command=self.load_image).pack(side="left")
        self.img_path_label = ttk.Label(img_frame, text="Please select image")
        self.img_path_label.pack(side="left", padx=10)

        # Watermark text frame
        text_frame = ttk.LabelFrame(function_frame, text="Watermark Text", padding="10")
        text_frame.pack(fill="x", pady=5)

        self.text_var = tk.StringVar(value=self.text) #Can't pass Python variable to widget. Need to use subclasses StringVar
        ttk.Entry(text_frame, textvariable=self.text_var).pack(fill="x")

        # sliders frame
        sliders_frame = ttk.LabelFrame(function_frame, text="Watermark Settings", padding="10")
        sliders_frame.pack(fill="x", pady=5)
        self.value_labels = {}  # dictionary for value labels

        # Font size slider
        ttk.Label(sliders_frame, text="Font Size:").grid(row=0, column=0, sticky="w")

        self.font_size_var = tk.IntVar(value=self.font_size)
        ttk.Scale(
            sliders_frame,
            from_=10,
            to=72,
            variable=self.font_size_var,
            command=lambda v: self.update_slider("font_size")
        ).grid(row=0, column=1, sticky="ew")

        self.value_labels["font_size"] = ttk.Label(sliders_frame, text=f"{self.font_size}")
        self.value_labels["font_size"].grid(row=0, column=2, padx=5)

        # Opacity slider
        ttk.Label(sliders_frame, text="Opacity:").grid(row=1, column=0, sticky="w")

        self.opacity_var = tk.IntVar(value=self.opacity)
        ttk.Scale(
            sliders_frame,
            from_=0,
            to=255,
            variable=self.opacity_var,
            command=lambda v: self.update_slider("opacity")
        ).grid(row=1, column=1, sticky="ew")

        self.value_labels["opacity"] = ttk.Label(sliders_frame, text=f"{self.opacity}")
        self.value_labels["opacity"].grid(row=1, column=2, padx=5)

        # Rotation slider
        ttk.Label(sliders_frame, text="Rotation:").grid(row=2, column=0, sticky="w")

        self.rotation_var = tk.IntVar(value=self.rotation)
        ttk.Scale(
            sliders_frame,
            from_=0,
            to=360,
            variable=self.rotation_var,
            command=lambda v: self.update_slider("rotation")
        ).grid(row=2, column=1, sticky="ew")

        self.value_labels["rotation"] = ttk.Label(sliders_frame, text=f"{self.rotation}")
        self.value_labels["rotation"].grid(row=2, column=2, padx=5)

        # Spacing slider
        ttk.Label(sliders_frame, text="Spacing:").grid(row=3, column=0, sticky="w")

        self.spacing_var = tk.IntVar(value=self.spacing)
        ttk.Scale(
            sliders_frame,
            from_=10,
            to=100,
            variable=self.spacing_var,
            command=lambda v: self.update_slider("spacing")
        ).grid(row=3, column=1, sticky="ew")

        self.value_labels["spacing"] = ttk.Label(sliders_frame, text=f"{self.spacing}")
        self.value_labels["spacing"].grid(row=3, column=2, padx=5)

        # Action buttons frame
        btn_frame = ttk.Frame(function_frame)
        btn_frame.pack(fill="x", pady=10)

        ttk.Button(btn_frame, text="Apply Watermark", command=self.apply_watermark).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Save Image", command=self.save_image).pack(side="left", padx=5)

    def update_slider(self, setting_name):
        # Update value variable
        value = int(round(getattr(self, f"{setting_name}_var").get()))
        setattr(self, setting_name, value)

        # Update value label
        display_text = str(value)
        self.value_labels[setting_name].config(text=display_text)

        if setting_name == "font_size":
            self.font = self.load_font()

    def load_image(self):
        """Load image from file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            self.img_path_label.config(text=file_path.split("/")[-1])
            self.watermark.load_image(file_path)
            self.update_preview()

    def update_preview(self):
        """Update preview image"""
        if not self.watermark.original_image:
            return

        img = self.watermark.original_image.copy()
        img.thumbnail((400, 400))

        img_tk = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(200, 200, image=img_tk)
        self.canvas.image = img_tk

    def apply_watermark(self):
        """Apply watermark with selected settings"""
        if not self.watermark.original_image:
            return

        self.watermark.text = self.text_var.get()

        # Create and apply watermark
        self.watermark.create_watermark(
            font_picked=self.font,
            spacing=self.spacing,
            opacity=self.opacity
        )
        self.watermark.add_watermark(rotation=self.rotation) # rotation is one of the inputs in tkinter paste function

        # Update preview
        if self.watermark.new_image:
            img = self.watermark.new_image.copy()
            img.thumbnail((400, 400))
            sample_img = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(200, 200, image=sample_img)
            self.canvas.image = sample_img

    def save_image(self):
        """Save new image"""
        if not self.watermark.new_image:
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")]
        )
        if save_path:
            self.watermark.new_image.save(save_path)
            print(f"File saved in {save_path}")