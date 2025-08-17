from flask import Flask, render_template, redirect, request, url_for
from dotenv import dotenv_values
import subprocess
import os

config = dotenv_values(".env")

app = Flask(__name__)

@app.route('/')
def home():
	# Get the info parameter if it exists
	info = request.args.get('info')  # Returns None if not provided

	return render_template("home.html", info=info)

@app.post('/mtg-proxies')
def mtg_proxies():
	action = request.form.get("action")
	text = request.form.get("text")
	uploaded_file = None
	filename = None
	content_text = None
	process = None

	if action == "reset":
		return redirect(url_for("home"))

	if "file" in request.files:
		uploaded_file = request.files["file"]
		filename = uploaded_file.filename

	if text != "":
		decklist = text.split("\n")
		f = open("deck.txt", "w")
		for card in decklist:
			try:
				f.write(card)
			except UnicodeEncodeError:
				f.close()
				os.remove("deck.txt")
				return redirect(url_for("home", info="Failed to find card: '{}'. Please replace with different card print.".format(card)))
		f.close()

	if filename != "":
		 # Read content as bytes
		content_bytes = uploaded_file.read()
		
		# If the file is text, decode to string
		content_text = content_bytes.decode('utf-8')

		if not os.path.exists(filename):
			decklist = content_text.split("\n")
			f = open(filename, "w")
			for card in decklist:
				try:
					f.write(card)
				except UnicodeEncodeError:
					f.close()
					os.remove(filename)
					return redirect(url_for("home", info="Failed to find card: '{}'. Please replace with different card print.".format(card)))
			f.close()

		filename = filename.removesuffix(".txt")

	if action == "convert":
		if text != "":
			process = subprocess.Popen(["python", "convert.py", "deck.txt", "deck-mtg-arena.txt"], stdout=subprocess.PIPE, text=True)
		if filename != "":
			process = subprocess.Popen(["python", "convert.py", "{}.txt".format(filename), "{}-mtg-arena.txt".format(filename)], stdout=subprocess.PIPE, text=True)	
	elif action == "token":
		if text != "":
			process = subprocess.Popen(["python", "tokens.py", "deck.txt"], stdout=subprocess.PIPE, text=True)
		if filename != "":
			process = subprocess.Popen(["python", "tokens.py", "{}.txt".format(filename)], stdout=subprocess.PIPE, text=True)
	elif action == "print":
		if text != "":
			process = subprocess.Popen(["python", "print.py", "deck.txt", "deck.pdf"], stdout=subprocess.PIPE, text=True)
		if filename != "":
			process = subprocess.Popen(["python", "print.py", "{}.txt".format(filename), "{}.pdf".format(filename)], stdout=subprocess.PIPE, text=True)	
	
	output, _ = process.communicate()
	print(output)
	if "ERROR" in output or "WARNING" in output:
		return redirect(url_for("home", info=output))
	else:
		return redirect(url_for("home", info="Task Completed"))

def main():
	app.run(host=config["IP_ADDR"], port=config["PORT"], debug=config["DEBUG"])
	
if __name__ == "__main__":
	main()