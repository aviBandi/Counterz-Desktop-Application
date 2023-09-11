import cv2
import numpy
from kivy.app import App
from kivy.core.image import Image
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.image import Image
from PIL import Image as PILImage

class DrawingApp(App):
    def build(self):
        return MyCanvas("noIMG.png")

class MyCanvas(BoxLayout):
    def __init__(self,pathToImg,**kwargs):
        super(MyCanvas, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.layout = RelativeLayout()

        self.layout.drawMode = True

        self.slider = Slider(min=1, max=10, value=2, size_hint_y=None, height=50)
        self.drawButton = Button(text="Draw", size_hint_y=None, height=50)
        self.clearButton = Button(text="Clear Canvas", size_hint_y=None, height=50)
        self.saveButton = Button(text="Save", size_hint_y=None, height=50)
        self.image_widget = Image(source=pathToImg, allow_stretch=True, keep_ratio=True, size=(self.width, self.height))

        self.canvas_widget = CanvasWidget()

        self.drawButton.bind(on_press=self.drawing)
        self.clearButton.bind(on_press=self.clear_canvas)  # Bind to the clear_canvas function
        self.saveButton.bind(on_press=self.save_canvas)

        self.canvas_widget.bind(size=self.adjust_canvas_size)
        self.layout.add_widget(self.image_widget)

        self.layout.add_widget(self.canvas_widget)
        self.add_widget(self.layout)
        self.add_widget(self.slider)
        self.add_widget(self.drawButton)
        self.add_widget(self.clearButton)  # Add the clearButton to the layout
        self.add_widget(self.saveButton)
    def drawing(self, instance):
        self.layout.drawMode = True

    def clear_canvas(self, instance):  # Implement the clear_canvas function
        self.canvas_widget.clear_lines()

    def adjust_canvas_size(self, instance, value):
        self.canvas_widget.height = self.height - self.slider.height - self.drawButton.height - self.clearButton.height - self.saveButton.height

    def save_canvas(self, instance):
        canvas_image = self.canvas_widget.export_as_image()

        print(f"Width: {self.image_widget.texture.size[0]}, Height: {self.image_widget.texture.size[1]}")
        print(f"Canvas Width: {self.canvas_widget.width}, Canvas Height: {self.canvas_widget.height}")

        heightRatio = canvas_image.height / self.image_widget.texture.size[1]
        widthRatio = canvas_image.width / self.image_widget.texture.size[0]

        if heightRatio < widthRatio:
            scaler = heightRatio
        else:
            scaler = widthRatio
        image_width_pixels = scaler*self.image_widget.texture.size[0]
        image_height_pixels = scaler*self.image_widget.texture.size[1]

        print(f"Width Scaler: {image_width_pixels}, Height: {image_height_pixels}")
        
        canvas_image.save('mask.png')

        ##########
        middle_image = self.extract_middle_by_pixels('../images/mask.png', int(image_width_pixels), int(image_height_pixels))
        cv2.imwrite('../images/mask.png', middle_image)
        #########
        img = cv2.imread('../images/mask.png')
        ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite('../images/mask.png', thresh1)

    def extract_middle_by_pixels(self, image_path, target_width, target_height):
        image = cv2.imread(image_path)
        img_height, img_width, _ = image.shape

        left = (img_width - target_width) // 2
        upper = (img_height - target_height) // 2
        right = left + target_width
        lower = upper + target_height

        middle_cropped = image[upper:lower, left:right]

        return middle_cropped




class CanvasWidget(Widget):
    def __init__(self, **kwargs):
        super(CanvasWidget, self).__init__(**kwargs)
        self.line = None
        self.lines = []  # Keep track of drawn lines

        with self.canvas:
            Color(1, 1, 1, .6)
            self.canvas_rect = Rectangle(pos=self.pos, size=self.size)

    def on_size(self, *args):
        self.canvas_rect.pos = self.pos
        self.canvas_rect.size = self.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                if self.parent.drawMode:
                    Color(0, 0, 0)
                else:
                    num = 290 / 365
                    Color(num, num, num, 1)
                self.line = Line(points=(touch.x, touch.y), width=self.parent.parent.slider.value)
                self.lines.append(self.line)  # Add the line to the list of lines

    def on_touch_move(self, touch):
        if self.line and self.collide_point(*touch.pos):
            self.line.points += (touch.x, touch.y)

    def on_touch_up(self, touch):
        self.line = None

    def clear_lines(self):
        for line in self.lines:
            self.canvas.remove(line)
        self.lines = []

if __name__ == '__main__':

    app = DrawingApp()
    app.run()
