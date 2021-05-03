import time
import datetime
import board
import busio
from collections import deque
from menuItem import MenuItem
from itertools import chain
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd


def initializeLCD():
    # Modify this if you have a different sized Character LCD
    lcd_columns = 16
    lcd_rows = 2
    
    # Initialise I2C bus.
    i2c = busio.I2C(board.SCL, board.SDA)
    
    # Initialise the LCD class
    lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

    # Turn on LCD backlight
    lcd.color = [100, 0, 0]

    return i2c, lcd


def initializeMenu():
    # Populate menu items
    MenuItem(['Set timelapse', 'Raspberry info']) # Root menu, no parent set
    MenuItem(['Frame interval', '# frames', 'Start timelapse'], 'Set timelapse') 
    MenuItem(['IP address'], 'Raspberry info')

    # Set allowed values of relevant menu items.
    menu = MenuItem.items
    menu['Frame interval'].allowedValues = list( 
        chain( range(0,60,5), # every 5 s up till 1 min
               range(60,60*60,60), # every min up till 1 h
               range(60*60, 60*60*24+60*60, 60*60) ) ) # every h up till and including 1 day
    menu['# frames'].allowedValues = list( 
        chain( range(1,100),
               range(100,1000,100),
               range(1000,10000,1000),
               range(10000,100000,10000) ) )
    menu['Start timelapse'].allowedValues = [True, False]

    # Set default values of relevant menu items
    menu['Frame interval'].value = 5
    menu['# frames'].value = 20
    menu['Start timelapse'].value = False


def menuLoop(lcd):
    menu = MenuItem.items
    for i in menu.values():
        print(i.parent)
    root = [item for item in menu.values() if item.parent == None]
    print(root)
    items = deque(root)
    print(items)

    lcd.clear()
    lcd.message = ">{}\n {}".format(items[0].name, items[1].name)

    while not menu['Start timelapse'].value:

        if lcd.down_button:
            lcd.clear()
            items.rotate(-1)
            lcd.message = ">{}\n {}".format(items[0].name, items[1].name)

        if lcd.up_button:
            lcd.clear()
            items.rotate(1)
            lcd.message = ">{}\n {}".format(items[0].name, items[1].name)

        if lcd.right_button:
            # Start editing value if menu item has no children.
            if items[0].children == None:
                pass
            # If menu item has child items, go down in menu hierarchy.
            else:
                items = deque(items[0].children)
                message = ""
                for item in items:
                    message += " {}\n".format(item.name)
                    if item == items[1]: break # Only print the first two items
                lcd.clear()
                lcd.message = message
                lcd.cursor_position(0,0)
                lcd.message = ">"

        if lcd.left_button:
            if items[0].parent == None:
                pass
            else:
                items = deque(items[0].parent.siblings)
                message = ""
                for item in items:
                    message += " {}\n".format(item.name)
                    if item == items[1]: break # Only print the first two items
                lcd.clear()
                lcd.message = message
                lcd.cursor_position(0,0)
                lcd.message = ">"

        if lcd.select_button:
            pass

        else: 
            time.sleep(0.1)



def setupMenu(i2c, lcd):
    # Initiate menu items
    menuItems = {"frame interval" : 3, 
                 "# frames" : 4, 
                 "duration": 12, 
                 "start sequence" : False}

    keys = [key for key in menuItems]
    items = deque(keys)
    print(items)

    # Basic menu scrolling
    lcd.clear()
    lcd.message = ">{}\n {}".format(items[0], items[1])
    while not menuItems["start sequence"]:
        if lcd.down_button:
            lcd.clear()
            items.rotate(-1)
            lcd.message = ">{}\n {}".format(items[0], items[1])

        if lcd.up_button:
            lcd.clear()
            items.rotate(1)
            lcd.message = ">{}\n {}".format(items[0], items[1])

        if lcd.select_button:
            pass


        # if Cleo_wil_op_lipje_bijten:
        #     don't



        else: time.sleep(0.1)


def main():

    try:
        # Initialize the LCD board
        i2c, lcd = initializeLCD()

        # Welcome message
        lcd.message = "TIMELAPSER\nv1.0"
        time.sleep(0.5)
        lcd.cursor_position(0,2)
        lcd.message = ">"
        time.sleep(0.5)
        lcd.clear()

        # Start menu
        # out = setupMenu(i2c, lcd)
        initializeMenu()
        out = menuLoop(lcd)
    
    except KeyboardInterrupt:
        lcd.clear()
        lcd.color = [0, 0, 0]
    finally:
        lcd.backlight = False


if __name__ == "__main__":
   main()