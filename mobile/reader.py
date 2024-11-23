# compatible with iOS 18

from subprocess import check_output
from requests import get, post
from requests.exceptions import ConnectionError
from time import sleep

HOST: str = "192.168.200.40"
PORT: int = 1413
URL: str = f"http://{HOST}:{PORT}"

PREVIOUS_CLIPBOARD: str = ""

def get_clipboard() -> str:
    return str(check_output('pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8'))

def send_clipboard() -> None:
    copied_text: str = get_clipboard()
    data: dict = {"text": copied_text}
    post(URL, data=data, allow_redirects=False)

def server_ok() -> bool:
    try:
        test_request = get(URL)
        if test_request.status_code == 200:
            return True
        return False
    except ConnectionError:
        return False

def clipboard_changed() -> bool:
    copied_text = get_clipboard()
    if PREVIOUS_CLIPBOARD != copied_text:
        global PREVIOUS_CLIPBOARD
        PREVIOUS_CLIPBOARD = copied_text
        return True
    return False

def loop(iter_time: int = 2) -> None:
    while server_ok():
        if clipboard_changed():
            send_clipboard()
        sleep(iter_time)

if __name__ == "__main__":
    loop()