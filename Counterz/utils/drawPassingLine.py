from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle


class ProgramVars:
    imageSize = None
    windowWidth = None
    windowHeight = None
    scaler = None
    linePoints = None

class LineDrawingWidget(Widget):
    def __init__(self, **kwargs):
        super(LineDrawingWidget, self).__init__(**kwargs)
        self.start_point = None
        self.end_point = None
        with self.canvas:
            self.bg_color = Color(1, 1, 1, .6)  # Set canvas background color to white
            self.rect = Rectangle(pos=self.pos, size=self.size)

            self.line_color = Color(1, 0, 0)  # Set line color to red
            self.line = Line(points=[])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_touch_down(self, touch):
        x, y = touch.x, touch.y
        self.start_point = [x, y]
        self.end_point = [x, y]

    def on_touch_move(self, touch):
        if self.start_point is not None:
            self.end_point = [touch.x, touch.y]
            self.line.width = 5
            self.line.points = [int(self.start_point[0]), int(self.start_point[1]), int(self.end_point[0]), int(self.end_point[1])]

    def on_touch_up(self, touch):
        self.start_point = None
        self.end_point = None

    def confirm_line(self, instance):
        myPoints = self.line.points

        ProgramVars.linePoints = [
            (myPoints[0] - ((ProgramVars.windowWidth - ProgramVars.imageSize[0]) // 2)) * ProgramVars.scaler,
            (ProgramVars.imageSize[1]-(myPoints[1] - ((ProgramVars.windowHeight - ProgramVars.imageSize[1]) // 2))) * ProgramVars.scaler,
            (myPoints[2] - ((ProgramVars.windowWidth - ProgramVars.imageSize[0]) // 2)) * ProgramVars.scaler,
            (ProgramVars.imageSize[1] - (myPoints[3] - ((ProgramVars.windowHeight - ProgramVars.imageSize[1]) // 2))) * ProgramVars.scaler
        ]

        # print(ProgramVars.linePoints)
class LineDrawingAppWidget(BoxLayout):
    def __init__(self, pathToFirstFrame, **kwargs):
        self.pathToFirstFrame = pathToFirstFrame
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.scaleWidth = None
        self.scaleHeight = None
        self.imageLocalImageSize = None
        self.build()

    def build(self):
        def update_image_size(instance, value):
            try:
                texture_width = instance.texture.size[0]
                texture_height = instance.texture.size[1]
                aspect_ratio = texture_width / texture_height
                if aspect_ratio > instance.width / instance.height:
                    widthOfImage = instance.width
                    heightOfImage = instance.width / aspect_ratio
                else:
                    widthOfImage = instance.height * aspect_ratio
                    heightOfImage = instance.height
                self.imageLocalImageSize = (widthOfImage, heightOfImage)

                ProgramVars.imageSize = (widthOfImage, heightOfImage)
                ProgramVars.windowWidth = self.width
                # subtract 70 because of the height of the button
                ProgramVars.windowHeight = self.height - 70
                self.scaleWidth = original_width / widthOfImage
                self.scaleHeight = original_height / heightOfImage
                ProgramVars.scaler = self.scaleWidth
            except:
                pass

        passingLineWidget = LineDrawingWidget()

        rel = RelativeLayout()
        rel.size_hint = 1, .9

        self.firstFrame = Image(source=self.pathToFirstFrame, allow_stretch=True, keep_ratio=True)

        rel.add_widget(self.firstFrame)
        rel.add_widget(passingLineWidget)
        self.add_widget(rel)

        confLineButton = Button(text='Confirm Line', size_hint_x=1, size_hint_y=None, height=70)
        confLineButton.bind(on_press=passingLineWidget.confirm_line)
        self.add_widget(confLineButton)

        original_width = self.firstFrame.texture.size[0]
        original_height = self.firstFrame.texture.size[1]
        self.firstFrame.bind(size=update_image_size)

class LineDrawingApp(App):
    def __init__(self, pathToFirstFrame, **kwargs):
        self.pathToFirstFrame = pathToFirstFrame
        super().__init__(**kwargs)

    def build(self):
        return LineDrawingAppWidget(self.pathToFirstFrame)

if __name__ == '__main__':
    LineDrawingApp('firstFrame.png').run()
