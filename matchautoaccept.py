# xhost +local:


import time
import pyautogui

ACCEPT_MATCH = "./img_ref/mfound/lol_accept_match.png"
SELECT_EMOTE = "./img_ref/champselect/select_emote.png"
SELECT_EMOTE_GRAY = "./img_ref/champselect/select_emote_gray.png"
MATCH_LOADNIG = "./img_ref/champselect/match_loading.png"
IN_QUEUE = "./img_ref/mfound/in_queue.png"



def match_accept_watcher():
    matchAccepted = False
    while (not matchAccepted):
        try:
            pyautogui.click(ACCEPT_MATCH)
        except pyautogui.ImageNotFoundException:
            print("test: {0} not on screen".format(ACCEPT_MATCH))
            time.sleep(5)
        except FileNotFoundError:
            print("{0} not found".format(ACCEPT_MATCH))
            return
        else:
            print("test: {0} found".format(ACCEPT_MATCH))
            time.sleep(13) # Accept match timer
            matchAccepted = not(check_if_src_on_screen(IN_QUEUE)) and in_champselect()

def in_champselect():
    print("champselect check")
    return (check_if_src_on_screen(SELECT_EMOTE) or check_if_src_on_screen(SELECT_EMOTE_GRAY))


def champselect_dodge_guard(): # returns True if the match has gone through or something else happened and False if dodged (and back in the Q)
    notDodged = True
    while (notDodged):
        notDodged = in_champselect()
        time.sleep(5)
    time.sleep(5)
    if (check_if_src_on_screen(MATCH_LOADNIG)):
        print("test: match loading")
        return True
    elif (check_if_src_on_screen(IN_QUEUE)):
        print("test: dodged")
        return False
    else:
        print("test: no img detected returning True")
        return True
        

        
    
    



def check_if_src_on_screen(src):
    try:
        pyautogui.locateOnScreen(src)
    except pyautogui.ImageNotFoundException:
        print("test: src not found")
        return False
    except FileNotFoundError:
        print("{0} ref img not found".format(src))
    else:
        print("test: src found")
        return True



if __name__ == '__main__':
    matchStarted = False
    while (not matchStarted):
        match_accept_watcher()
        matchStarted = champselect_dodge_guard()