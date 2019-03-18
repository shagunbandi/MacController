from flask import Flask
from flask import render_template
import os
app = Flask(__name__)

volume_level = 3
play_status = 0


@app.route('/')
def home():
   return render_template("main.html")



@app.route('/music')
def music_toggle():
	return render_template("music.html", value="Ready", status="Done")


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


# osascript -e 'tell application "iTunes" to play'


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

if __name__ == '__main__':
	command = 'osascript -e "set Volume 3"'
	os.system(command)
	app.run('0.0.0.0')
