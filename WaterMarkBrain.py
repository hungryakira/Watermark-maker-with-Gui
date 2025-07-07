# Import statements:
from PIL import Image, ImageDraw
from math import ceil

class WaterMarkBrain:
    """Class for creating watermark."""

    def __init__(self):

        self.original_image = None
        self.new_image = None
        self.text= "Your watermark"
        self.txt_layer = None

    def load_image(self, image_path):
        self.original_image = Image.open(image_path).convert("RGBA") # create a PIL.Image.Image object img and convert to RGBA.

    # Creating watermark from text
    def create_watermark(self, font_picked, spacing, opacity):
        """Function to create horizontal watermark

        Returns
            txt_layer: Image object with watermark applied
        """

        self.txt_layer = Image.new("RGBA", (self.original_image.size[0] * 2, self.original_image.size[0] * 2), (255, 255, 255, 0))
        draw = ImageDraw.Draw(self.txt_layer)
        draw_loc = {"x":5,
                    "y":10
                    } #starting draw position at top left

        # finding input text dimensions using textbbox
        bbox = draw.textbbox((0, 0), self.text, font=font_picked)  # (left, top, right, bottom)
        text_width = int(bbox[2] - bbox[0])
        text_height = int(bbox[3] - bbox[1])

        draw.text((draw_loc["x"],draw_loc["y"]),
                  text=self.text, fill=(255, 255, 255, 100), font=font_picked) #draw first watermark

        # Drawing watermark
        for y in range(ceil(self.txt_layer.size[1] / (text_height + (spacing * 1.5)))): #number of loop = (font height + gap) / image height
            draw_loc["x"] = 5 #reset x
            for x in range(ceil(self.txt_layer.size[0]/(text_width + spacing))): #number of loop = (font width + gap) / image width
                draw.text((draw_loc["x"],draw_loc["y"]), text=self.text, fill=(255, 255, 255, opacity), font=font_picked)
                draw_loc["x"] += text_width + spacing
            draw_loc["y"] += text_height + (spacing * 1.5)

        return self.txt_layer

# adding photos together
    def add_watermark(self, rotation):
        self.new_image = self.original_image.copy()
        self.new_image.paste(self.txt_layer.rotate(rotation),
                             (-int(self.new_image.size[0] / 2), -int(self.new_image.size[0] / 2)),  #Paste image to middle of original image
                             mask = self.txt_layer.rotate(rotation))

