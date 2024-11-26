# compatible with iOS 18

from subprocess import check_output, CalledProcessError
from requests import get, post
from requests.exceptions import ConnectionError
from time import sleep

HOST: str = "192.168.1.1"
PORT: int = 1413
URL: str = f"http://{HOST}:{PORT}"
PREVIOUS_CLIPBOARD: str = ""

def get_clipboard() -> str:
    try:
        clipboard = str(check_output('pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8'))
        return clipboard
    except CalledProcessError as e:
        print(e)
        return ''

def send_clipboard() -> None:
    copied_text: str = get_clipboard()
    if copied_text == "(null)":
        return
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
    global PREVIOUS_CLIPBOARD
    copied_text = get_clipboard()
    if PREVIOUS_CLIPBOARD != copied_text:
        PREVIOUS_CLIPBOARD = copied_text
        return True
    return False

def loop(iter_time: int = 2) -> None:
    print('Service started')
    while server_ok():
        if clipboard_changed():
            send_clipboard()
        sleep(iter_time)
    print('Stopped')

if __name__ == "__main__":
    loop(3)