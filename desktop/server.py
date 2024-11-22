import re

from flask import Flask, request
from pyperclip import copy
from sys import argv
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_route():
    if request.method == 'GET':
        return 'Server is OK.'

    if request.method == 'POST':
        new_clipboard = request.form.get("text")
        if new_clipboard is not None:
            copy(new_clipboard)
        return 'OK'

    return "Invalid method."

if __name__ == "__main__":
    default_port = 1413
    default_host = "0.0.0.0"
    argv_string = ' '.join(argv).lower()
    # Search for host and port provided by user, without validating eligibility
    host_finder_regex = r"-host\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    port_finder_regex = r"-port\s*(\d{1,5})"

    if "-host" in argv_string:
        matches = re.search(host_finder_regex, argv_string)
        if matches is not None:
            default_host = matches.groups()[0]

    if "-port" in argv_string:
        matches = re.search(port_finder_regex, argv_string)
        if matches is not None:
            default_port = matches.groups()[0]

    app.run(host=default_host, port=default_port)