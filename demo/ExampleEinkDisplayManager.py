# !/usr/bin/python
# -*- coding:utf-8 -*-

"""DEMO - E-ink Display Manager"""
import sys
import os

import logging
from ext.waveshare_epd import epd2in13b_V3
import time
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.DEBUG)

try:
	logging.info("epd2in13b_V3 Watch Demo Pe3eS")

	epd = epd2in13b_V3.EPD()
	logging.info("Init and Clear")
	epd.init()
	epd.Clear()
	time.sleep(1)

	# Drawing on the image
	logging.info("Prepare Fonts")
	font28 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 28)
	font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
	font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
	font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

	# Drawing on the Horizontal image
	logging.info("Show Time ...")
	HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
	drawblack = ImageDraw.Draw(HBlackimage)
	drawblack.text((10, 0), 'Time:', font=font20, fill=0)

	run = 0
	while True:
		HRedimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
		drawred = ImageDraw.Draw(HRedimage)
		drawred.text((10, 30), time.strftime('%H:%M'), font=font28, fill=0)
		epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))
		time.sleep(60)
		run += 1
		if run == 3:
			break

	logging.info("Clear...")
	epd.init()
	epd.Clear()

	logging.info("Goto Sleep...")
	epd.sleep()

except IOError as e:
	logging.info(e)

except KeyboardInterrupt:
	logging.info("ctrl + c:")
	epd2in13b_V3.epdconfig.module_exit()
	exit()
