
import winsound
from time import sleep, localtime


def beep():
    if m == 59:
        winsound.Beep(2000, 250)  # one long beep
        winsound.Beep(1000, 500)  # one long beep
    elif m == 29:
        winsound.Beep(3000, 200)
        winsound.Beep(2000, 400)


if __name__ == "__main__":
    while True:
        now = localtime()
        m = now.tm_min
        s = now.tm_sec
        sleep(60 - s)  # refresh every minute.
        beep()