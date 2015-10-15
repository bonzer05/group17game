#!/usr/bin/python3

import os.path
from map import rooms
from player import *
from items import *
from parser_input import *


def load_room(file):
    # global tells the function that it should use the "global"
    # current_room variable instead of create a new one that is
    # only vissible within this function
    global current_room
    #make this true if the CURRENT ROOM line is found
    found_room = False
    for line in file:
        #if the room if found the load it in current_room
        if found_room:
            current_room = rooms[line]
            break
        elif line == "CURRENT ROOM\n":
            found_room = True
            continue

def load_inventory(file):
    global inventory
    #start with an empty inventory
    inventory = []
    
    found_inventory = False     
    for line in file:
        if found_inventory:
            if line == "\n":
                break
            line = line.strip("\n")
            inventory.append(items[line])
        elif (line == "INVENTORY\n"):
            found_inventory = True
            continue



def load_rooms(file):
    global rooms
    found_rooms = False
    found_room = ""
    
    for line in file:
        if found_rooms:
            #end the loop when all rooms are loaded
            if line == "END ROOMS\n":
                found_rooms = False
                break
            #start loading each room's items
            line = line.strip("\n")
            if line == line.upper():
                #the method .title() capitalises the 1st letter
                #of each word in the string
                line = line.lower()
                found_room = line.title()
                continue
            elif (found_room != "") and (line != ""):
                rooms[found_room]["items"].append(items[line])
            else:
                found_room = ""
                continue
        elif (line == "ROOMS\n"):
            found_rooms = True
            continue

def empty_rooms():
    global rooms
    for roomId,room in rooms.items():
        rooms[roomId]["items"] = []
        

def load_game():
    # check if a save file exists
    if not os.path.exists("save.txt"):
        print("You do not have a save file.")
    else:
        # open save.txt in read mode
        file = open("save.txt", 'r')
        #load inventory
        load_inventory(file)
        # emptry tooms of all items to add the items
        # that were storedin save.txt        
        empty_rooms()
        load_rooms(file)
        # load the room the player was in        
        load_room(file)
        #close the file
        file.close()
        
        print("Adventure Loaded")        

def save_game():
    # Re-write the previous saved file
    file = open("save.txt", 'w')
    file = open("save.txt", 'r+')

    
    # Save inventory
    file.write("INVENTORY\n")
    for item in inventory:
        file.write("%s\n" % item["id"])
    file.write("\n")
    
    # Save room items
    file.write("ROOMS\n")
    for roomId,room in rooms.items():        
        file.write(roomId.upper())
        file.write("\n")
        for item in room["items"]:
            file.write(item["id"])
            file.write("\n")
    file.write("END ROOMS\n\n")
    
    # Save current room
    file.write("CURRENT ROOM\n")
    file.write(current_room["id"])
    
    #close and save
    file.close()
    
    print("Adventure Saved")

def list_of_items(items):
    """This function takes a list of items (see items.py for the definition) and
    returns a comma-separated list of item names (as a string). For example:
    """
    
    if items == []:
        return ''
    
    str_items = items[0]["name"]
    skip = False
    for item in items:
        if skip:
            str_items += ", " + item["name"]
        else:
            skip=True
        
    return str_items

def print_room_items(room):
    """This function takes a room as an input and nicely displays a list of items
    found in this room (followed by a blank line). If there are no items in
    the room, nothing is printed. See map.py for the definition of a room, and
    items.py for the definition of an item. This function uses list_of_items()
    to produce a comma-separated list of item names. For example:
    """
    
    if room["items"] != []:
        item_list = list_of_items(room["items"])
        string = "There is " + item_list + " here."
        print(string)
        print()

def print_inventory_items(items):
    """This function takes a list of inventory items and displays it nicely, in a
    manner similar to print_room_items(). The only difference is in formatting:
    print "You have ..." instead of "There is ... here.". For example:
    """
    
    item_list = list_of_items(items)
    item_list = "You have " + item_list + "."
    print(item_list)
    print()

def print_room(room):
    """This function takes a room as an input and nicely displays its name
    and description. The room argument is a dictionary with entries "name",
    "description" etc. (see map.py for the definition). The name of the room
    is printed in all capitals and framed by blank lines. Then follows the
    description of the room and a blank line again. If there are any items
    in the room, the list of items is printed next followed by a blank line
    (use print_room_items() for this). For example:
    """
    
    # Display room name
    print()
    print(room["name"].upper())
    print()
    # Display room description
    print(room["description"])
    print()
    if room["items"] != []:
        print_room_items(room)
        #print()


def exit_leads_to(exits, direction):
    """This function takes a dictionary of exits and a direction (a particular
    exit taken from this dictionary). It returns the name of the room into which
    this exit leads. For example:
    """
    
    return rooms[exits[direction]]["name"]


def print_exit(direction, leads_to):
    """This function prints a line of a menu of exits. It takes a direction (the
    name of an exit) and the name of the room into which it leads (leads_to),
    and should print a menu line in the following format:
    """
    
    print("GO " + direction.upper() + " to " + leads_to + ".")


def print_menu(exits, room_items, inv_items):
    """This function displays the menu of available actions to the player. The
    argument exits is a dictionary of exits as exemplified in map.py. The
    arguments room_items and inv_items are the items lying around in the room
    and carried by the player respectively. The menu should, for each exit,
    call the function print_exit() to print the information about each exit in
    the appropriate format. The room into which an exit leads is obtained
    using the function exit_leads_to(). Then, it should print a list of commands
    related to items: for each item in the room print
    """
    
    print("You can:")
    # Iterate over available exits
    for direction in exits:
        # Print the exit name and where it leads to
        print_exit(direction, exit_leads_to(exits, direction))
    for item in room_items:
        print("TAKE " + item["id"].upper() + " to take " + item["name"])
    for item in inv_items:
        print("DROP " + item["id"].upper() + " to drop your " + item["name"])
    print("Go to main MENU.")
    
    print("What do you want to do?")


def is_valid_exit(exits, chosen_exit):
    """This function checks, given a dictionary "exits" (see map.py) and
    a players's choice "chosen_exit" whether the player has chosen a valid exit.
    It returns True if the exit is valid, and False otherwise. Assume that
    the name of the exit has been normalised by the function normalise_input().
    """
    return chosen_exit in exits


def execute_go(direction, room):
    """This function, given the direction (e.g. "south") updates the current room
    to reflect the movement of the player if the direction is a valid exit
    (and prints the name of the room into which the player is
    moving). Otherwise, it prints "You cannot go there."
    """
    
    global current_room
    if direction in room["exits"]:
        current_room = rooms[room["exits"][direction]]
    else:
        print("You can't go that way.")
        print()


def execute_take(item_id, room):
    """This function takes an item_id as an argument and moves this item from the
    list of items in the current room to the player's inventory. However, if
    there is no such item in the room, this function prints
    "You cannot take that."
    """
    for item in room["items"]:
        if item_id == item["id"]:
            inventory.append(items[item_id])
            room["items"].remove(items[item_id])
            print("You took",items[item_id]["name"])
            return
            
    print("There is no such item here.")

def execute_drop(item_id, room):
    """This function takes an item_id as an argument and moves this item from the
    player's inventory to list of items in the current room. However, if there is
    no such item in the inventory, this function prints "You cannot drop that."
    """
    for item in inventory:
        if item_id == item["id"]:
            inventory.remove(items[item_id])
            room["items"].append(items[item_id])
            print("You dropped ",items[item_id]["name"])
            return
    print("You don't have", items[item_id]["name"],".")

def execute_command(command, room):
    """This function takes a command (a list of words as returned by
    normalise_input) and, depending on the type of action (the first word of
    the command: "go", "take", or "drop"), executes either execute_go,
    execute_take, or execute_drop, supplying the second word as the argument.
    """

    if 0 == len(command):
        return

    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1], room)
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1], room)
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1], room)
        else:
            print("Drop what?")
            
    elif command[0] == "menu":
        return "menu"            
    
    elif (command[0] == "quit") or (command[0] == "exit"):
        return "Quit"
    else:
        print("This makes no sense.")


def menu(exits, room_items, inv_items):
    """This function, given a dictionary of possible exits from a room, and a list
    of items found in the room and carried by the player, prints the menu of
    actions using print_menu() function. It then prompts the player to type an
    action. The players's input is normalised using the normalise_input()
    function before being returned.
    """

    # Display menu
    print_menu(exits, room_items, inv_items)

    # Read player's input
    user_input = input("> ")
    print()
    
    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


def move(exits, direction):
    """This function returns the room into which the player will move if, from a
    dictionary "exits" of avaiable exits, they choose to move towards the exit
    with the name given by "direction". For example:
    """

    # Next room to go to
    return rooms[exits[direction]]

def main_menu(game_started):
    # Print main menu
    print("MAIN MENU:\n")
    # If game has started print continue. Else print new game.
    if not game_started:
        print("New Game")
    else:
        print("Continue Game")
    print("Load Game\nSave Game\nQuit Game")
    #Get input from user
    choice = str(input("> Chose Option: "))
    print()
    #make all letters lower case
    choice = choice.lower()
    
    if (choice == "new game") or (choice == "new"):
        return ""
    if (choice == "continue game") or (choice == "continue"):
        return ""
    elif (choice == "load game") or (choice == "load"):
        load_game()
        return ""
    elif (choice == "save game") or (choice == "save"):
        save_game()
    elif (choice == "quit game") or (choice == "quit"):
        return "Quit"

# This is the entry point of our program
def main():
    game_started = False
    # Print main menu and heck if player wants to quit
    menu_option = main_menu(game_started)
    
    # Main game loop
    # If player wants to quit don't enter loop
    while menu_option != "Quit":
        game_started = True
        # Display game status (room description, inventory etc.)
        print_room(current_room)
        print_inventory_items(inventory)

        # Show the menu with possible actions and ask the player
        command = menu(current_room["exits"], current_room["items"], inventory)

        # Execute the player's command
        menu_option = execute_command(command, current_room)
        # If player asks for main menu, display main menu
        if menu_option == "menu":
            menu_option = main_menu(game_started)


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()
    #save_game()
    #load_game()