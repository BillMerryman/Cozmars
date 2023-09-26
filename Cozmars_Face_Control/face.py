import os
import threading
import random
import time
import asyncio
import digitalio
import board
from PIL import Image, ImageDraw
from adafruit_rgb_display import ili9341
from adafruit_rgb_display import st7789  # pylint: disable=unused-import
from adafruit_rgb_display import hx8357  # pylint: disable=unused-import
from adafruit_rgb_display import st7735  # pylint: disable=unused-import
from adafruit_rgb_display import ssd1351  # pylint: disable=unused-import
from adafruit_rgb_display import ssd1331  # pylint: disable=unused-import

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

disp = st7789.ST7789(spi, 
        rotation=270, 
        width=135, 
        height=240, 
        x_offset=53, 
	y_offset=40, # 1.14" ST7789
	cs=cs_pin,
	dc=dc_pin,
	rst=reset_pin,
	baudrate=BAUDRATE,
	)

if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

class FaceAnimate(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.face_offset_x = 0
		self.face_offset_y = 0
		self.images = {}
		self.load_images(os.getcwd() + "/Cozmars_Face_Control/images.txt")
		self.face_key = list(self.images.keys())[0]
		self.face = self.images[self.face_key]		
		self.running = True
		random.seed()

	def load_images(self, file_list_path):
		try:
			with open(file_list_path, 'r') as file:
				for line in file:
					image_filename = line.strip()
					key = image_filename.split('.')[0]
					image = Image.open(os.getcwd() + "/Cozmars_Graphics/" + image_filename)
					self.images[key] = image
		except Exception as e:
			print(f"{e}")

	def run(self):
		while self.running:
			time.sleep(random.uniform(.5, 1))
			self.face_offset_x = random.randint(-5, 5)
			self.face_offset_y = random.randint(-5, 5)
			self.show_face()

	def set_face(self, face_name):
		self.face = self.images[face_name]
		self.show_face()

	def get_background(self, R, G, B):
		image = Image.new("RGB", (width, height))
		draw = ImageDraw.Draw(image)
		draw.rectangle((0, 0, width, height), outline=0, fill=(R, G, B))
		return image

	def show_face(self):
		background = self.get_background(int("6B", 16), int("8E", 16), int("23",16))
		background.paste(self.face, (self.face_offset_x, self.face_offset_y), self.face)
		disp.image(background)

	def stop(self):
		self.running = False
