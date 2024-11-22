from flask import Flask, request
from subprocess import run as run_powershell
from sys import platform, argv
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_route():
    if request.method == 'GET':
        return 'Server is OK.'
    if request.method == 'POST':
        new_clipboard = request.form.get("text")
        # For computers running Windows:
        if platform == "win32":
            run_powershell(["powershell", "-Command", "Set-Clipboard \"", new_clipboard, "\""])
        return str(new_clipboard)
    return "Invalid method."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1413)