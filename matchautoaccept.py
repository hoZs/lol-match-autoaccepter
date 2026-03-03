# xhost +local:


from sys import thread_info
import time
import pyautogui
from pathlib import Path
import threading 


class AutoAccept:

    def __init__(self):
        self.MATCH_LOADNIG = "./img_ref/game/match_loading.png"

        self.BASE = Path("./img_ref/client")
        self.RESOLUTIONS = ["1024x576", "1280x720", "1600x900", "1920x1080"]
        self.DETECTION_IMG = ["play.png", "party_grey.png"]
        self.BASE_FULL = self.detect_resolution() / "targets"

        self.ACCEPT_MATCH = self.BASE_FULL / "accept_match.png"
        self.IN_QUEUE = self.BASE_FULL / "in_queue.png"

        # the select emote icons are used to indentify the champselect
        self.SELECT_EMOTE = self.BASE_FULL / "select_emote.png"
        self.SELECT_EMOTE_GRAY = self.BASE_FULL / "select_emote_gray.png"

        self.threadControl = threading.Event()
        self.autoacceptThread = None

    # This MUST run at least once
    def detect_resolution(self): 
        print("**detect resolution started**")
        for res in self.RESOLUTIONS:
            for detectImg in self.DETECTION_IMG:
                print("checking {0} - {1}".format(res, detectImg))
                isOnScreen = check_if_on_screen(self.BASE / res / "detect" / detectImg)
                if (isOnScreen):
                    print("img found -> setting resolution")
                    return (self.BASE / res)
        print("resolution cant be detected -> defaulting to 1920x1080")
        return (self.BASE / "1920x1080")

    
    

    def create_autoaccept_no_champselect_thread(self):
        if (self.autoacceptThread == None or not self.autoacceptThread.is_alive()):
            self.threadControl.set()
            self.autoacceptThread = threading.Thread(target=self._autoaccept_no_champselect_process)
            self.autoacceptThread.start()
            
        
    def stop_autoaccept_no_champselect_thread(self):
        if (self.autoacceptThread != None and self.autoacceptThread.is_alive()):
            self.threadControl.clear() 
            self.autoacceptThread.join()

    def join_autoaccept_no_champselect_thread(self):
        if (self.autoacceptThread != None and self.autoacceptThread.is_alive()):
            self.autoacceptThread.join()

    def _autoaccept_no_champselect_process(self):
        matchStarted = False
        while ((not matchStarted) and self.threadControl.is_set()):
            self._match_accept_watcher()
            matchStarted = self._champselect_dodge_guard()
 
 
    def _match_accept_watcher(self):
        print("**Match accept watcher started**")
        matchAccepted = False
        while ((not matchAccepted) and (self.threadControl.is_set())):
            found = click_if_on_screen(self.ACCEPT_MATCH)
            if (found):
                time.sleep(13) # Accept match timer
                matchAccepted = not(check_if_on_screen(self.IN_QUEUE)) and self.in_champselect()
            else:
                time.sleep(5)

    def in_champselect(self):
        print("champselect check")
        return (check_if_on_screen(self.SELECT_EMOTE) or check_if_on_screen(self.SELECT_EMOTE_GRAY))


    def _champselect_dodge_guard(self): # returns True if the match has gone through or something else happened and False if dodged (and back in the Q)
        notDodged = True
        while (notDodged and self.threadControl.is_set()):
            notDodged = self.in_champselect()
            time.sleep(5)
        time.sleep(5)
        if (check_if_on_screen(self.MATCH_LOADNIG)):
            print("test: match loading")
            return True
        elif (check_if_on_screen(self.IN_QUEUE)):
            print("test: dodged")
            return False
        else:
            print("test: no img detected returning True")
            return True
        

        
    
    



def check_if_on_screen(src):
    convertedSrc = str(src)
    try:
        print("Searching image on screen: ", end="")
        pyautogui.locateOnScreen(convertedSrc)
    except pyautogui.ImageNotFoundException:
        print("not on screen")
        return False
    except FileNotFoundError:
        print("source not found")
    else:
        print("image found")
        return True
    

# returns wether it could or could not complete the action
def click_if_on_screen(src):
    convertedSrc = str(src)
    try:
        print ("Tring to click image: ", end="")
        pyautogui.click(convertedSrc)
    except pyautogui.ImageNotFoundException:
        print("not on screen")
        return False
    except FileNotFoundError:
        print("source not found")
        return False
    else:
        print("action completed")
        return True



if __name__ == '__main__':
    app = AutoAccept()
    app.create_autoaccept_no_champselect_thread()