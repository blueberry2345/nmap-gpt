import optparse
import tkinter
from userinterface import UserInterface


def get_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-t", "--target", dest="ip_target", help="Input IP address of target")
    (user_input, _ ) = parse_object.parse_args()

    # if user doesn't input ip address of target
    if not user_input.ip_target:
        print("Input IP address of target")

    return user_input.ip_target

# Create window for UI
window = tkinter.Tk()
UserInterface(window)

# Mainloop for window
window.mainloop()
