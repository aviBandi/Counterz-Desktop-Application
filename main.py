import cv2
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from drawMask import MyCanvas
from drawPassingLine import *
import drawPassingLine
from resizeImage import resize
from detectionCode import counter


class ProgramVars():
    detectionObject=None
    detectionVideoPath=None
    firstFrame=None
    limits = None

class WindowManager(ScreenManager):
    pass

class HomePage(Screen):
    def show_popup(self, content):
        # Create a pop-up window
        # content = Label(text=f"You had {num} {detetction} pass the line")
        popup = Popup(title="Popup Example", content=content, size_hint=(None, None), size=(500, 500))

        # Add a button to close the pop-up
        close_button = Button(text="Close")
        close_button.bind(on_press=popup.dismiss)
        content.add_widget(close_button)

        # Open the pop-up
        popup.open()
    def execute(self, instance):
        if ProgramVars.detectionObject != None and ProgramVars.detectionVideoPath != None and ProgramVars.limits != None:
            print(f"limits: {ProgramVars.limits}")
            print(f"Detectio Object {ProgramVars.detectionObject}")
            print(f"Video Path {ProgramVars.detectionVideoPath}")
            cv2.imshow("mask",cv2.imread("mask.png"))
            for i, each in enumerate(ProgramVars.limits):
                ProgramVars.limits[i] = int(each)
            count = counter.count(ProgramVars.limits, ProgramVars.detectionObject, cv2.VideoCapture(ProgramVars.detectionVideoPath), cv2.imread("mask.png"))
            self.show_popup(Label(text=f"You had {count} {ProgramVars.detectionObject} pass the line"))
        else:
            self.show_popup(Label(text="Please make sure you selected\n select a video, detection object,\n and draw a mask and passing line"))




class ChooseVideo(Screen):
    selected_video_path = ""
    # loads in video for a preview for the user.
    def load_video(self, selected_file):
        video_widget = self.ids.video_widget
        try:
            self.selected_video_path = selected_file[0]
        except:
            pass
        selected_video_path = repr(self.selected_video_path)
        video_widget.source = selected_video_path[1:-1]
        video_widget.state = 'play'
    # this corelates to the  save video in the choose video screen
    def save_video(self):
        ProgramVars.detectionVideoPath=self.selected_video_path

        print(ProgramVars.detectionVideoPath)

class ChooseDetection(Screen):
    def checkbox_click(self,instance,value,detectionObj):
        if value==True:
            ProgramVars.detectionObject=detectionObj
            print(ProgramVars.detectionObject)

            # video_capture = cv2.VideoCapture(ProgramVars.detectionVideoPath)
            #
            # if video_capture.isOpened():
            #     ret, opencv_image = video_capture.read()
            #     video_capture.release()
            #
            # cv2.imwrite("firstFrame.png", opencv_image)


class AddRestrictions(Screen):
    def on_pre_enter(self, *args):


        # Shows the dumbasses no image was selected..0
        if ProgramVars.detectionVideoPath == None:
            # self.ids.firstFrame.source= "Images/noIMG.png"
            self.ids.masker.clear_widgets()
            self.ids.masker.add_widget(Image(source='Images/noIMG.png'))
        # Code to show the first frame of the video
        else:



            drawing_canvas = MyCanvas("firstFrame.png")
            self.ids.masker.clear_widgets()
            self.ids.masker.add_widget(drawing_canvas)

class AddPassingPoint(Screen):
    def on_pre_enter(self, *args):
        if ProgramVars.detectionVideoPath == None:
            self.ids.drawPassing.clear_widgets()
            self.ids.drawPassing.add_widget(Image(source='Images/noIMG.png'))
        else:

            firstFrame = cv2.imread("firstFrame.png")
            mask = cv2.imread("mask.png")

            width = firstFrame.shape[1] / mask.shape[1]
            height = firstFrame.shape[0] / mask.shape[0]

            resize('mask.png', width, height)

            img = cv2.bitwise_and(cv2.imread("firstFrame.png"), cv2.imread("mask.png"))
            cv2.imwrite("both.png", img)
            self.ids.drawPassing.clear_widgets()
            drawPassing = LineDrawingAppWidget("both.png")
            self.ids.drawPassing.add_widget(drawPassing)
    def on_pre_leave(self, *args):
        ProgramVars.limits = drawPassingLine.ProgramVars.linePoints
            # print(f"the think other{drawPassingLine.ProgramVars.linePoints}")
            #
            # ProgramVars.limits = drawPassingLine.ProgramVars.linePoints
            # print(ProgramVars.limits)
class detectionsApp(MDApp):
    pass


detectionsApp().run()
