from flask import Flask
from flask import render_template, request, jsonify
import os

import RPi.GPIO as GPIO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

volume_level = 3
play_status = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

gpio_status_dict = {
    3: False,
    2: False
}


@app.route('/pihome')
def pihome_no_par():
    return render_template("picontrol.html", fan_status="Unknown", light_status="Unknown")

@app.route('/pihome/<gpio_pin>/<gpio_status>')
def pihome(gpio_pin=None, gpio_status=None):

    gpio_pin = int(gpio_pin)
    gpio_status = bool(gpio_status)

    print(gpio_pin)
    print(gpio_status)

    GPIO.output(gpio_pin, GPIO.HIGH if gpio_status else GPIO.LOW)
    gpio_status_dict[gpio_pin] = not gpio_status

    return render_template("picontrol.html", fan_status=gpio_status_dict[2], light_status=gpio_status_dict[3])


@app.route('/')
def home():
   return render_template("main.html")


@app.route('/music')
def music_toggle():
    return render_template("music.html", value="Ready", status="Done")


@app.route('/next_song')
def next_song():
    command = 'tell application "iTunes" to next track'
    command = "osascript -e '" + command + "'"

    print(command)
    os.system(command)

    return render_template("music.html", status="Next Song Bringing right up")


@app.route('/prev_song')
def prev_song():
	command = 'tell application "iTunes" to previous track'
	command = "osascript -e '" + command + "'"

	print(command)
	os.system(command)	

	return render_template("music.html", status="Bringn' back the previous song")



@app.route('/music/<status>')
def music_set(status):
	
	global play_status

	
	if status == '1' or status == 1:
		command = "osascript -e 'tell application " + '"iTunes"' + ' to play' + "'"
		play_status = 1
	elif status == '0' or status == 0:
		command = "osascript -e 'tell application " + '"iTunes"' + ' to pause' + "'"
		play_status = 0
	else:
		if play_status == '1' or play_status == 1:
			command = "osascript -e 'tell application " + '"iTunes"' + ' to pause' + "'"
			play_status = 0
		else:
			command = "osascript -e 'tell application " + '"iTunes"' + ' to play' + "'"
			play_status = 1

	print(command)
	os.system(command)
	
	value = "Playing" if play_status==1 else "Paused"
	return render_template("music.html", value=value, status="Done")



@app.route('/volume')
def volume_no_par():
	return render_template("volume.html", value="", status="Ready")


@app.route('/volume/<up_down>')
def volume(up_down):
	global volume_level
	status = "Hogya Bhiya !!"
	if up_down == '1' or up_down == 1:
		if volume_level < 7:
			volume_level += 1
		else:
			status = "Max Volume Reached"
	else:
		if volume_level > 0:
			volume_level -= 1
		else:
			status = "Min Volume Reached"

	command = 'osascript -e "set Volume ' + str(volume_level) + '"'
	os.system(command)

	return render_template("volume.html", value=volume_level, status=status)


@app.route('/youtube')
def youtube():
	return render_template("youtube.html", status="Ready")


# https://eastmanreference.com/complete-list-of-applescript-key-codes


@app.route('/move_left')
def move_left():
	
	command = 'tell application "System Events" to key code 123 using {option down, command down}'
	command = "osascript -e '" + command + "'"
	print(command)
	os.system(command)	

	return render_template("youtube.html", status="Moving Left")


@app.route('/move_right')
def move_right():
	
	command = 'tell application "System Events" to key code 124 using {option down, command down}'
	command = "osascript -e '" + command + "'"
	print(command)
	os.system(command)	

	return render_template("youtube.html", status="Moving Right")


@app.route('/youtube_toggle')
def youtube_toggle():
	
	command = 'tell application "System Events" to key code 40'
	command = "osascript -e '" + command + "'"
	
	print(command)
	os.system(command)	

	return render_template("youtube.html", status="Toggle Music")


@app.route('/brightness')
def brightness():
	return render_template("brightness.html", status="Ready")


@app.route('/inc_brightnes')
def inc_brightnes():

	command = 'tell application "System Events" to key code 113'
	command = "osascript -e '" + command + "'"
	print(command)
	os.system(command)	

	return render_template("brightness.html", status="Dimming")


@app.route('/dec_brightnes')
def dec_brightnes():

	command = 'tell application "System Events" to key code 107'
	command = "osascript -e '" + command + "'"
	print(command)
	os.system(command)	

	return render_template("brightness.html", status="Brighter")



if __name__ == '__main__':
	command = 'osascript -e "set Volume 3"'
	os.system(command)
	app.run(host='0.0.0.0', port=5001)
















