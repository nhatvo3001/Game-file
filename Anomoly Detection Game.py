"""
Category 1: Allowing user to choose the difficulty through command-line argument
Category 2: Material anomaly
a: A new anomly called "MATERIAL CHANGE" was added
b: This anomaly choose from a list of 4 materials, which are metal, leather, wooden, and oak.
c: No changes in rooms were needed

Vo Minh Nhat
101284192
Van Tien Phi Pham
101320140

Pair Programming:
1) We did pair programming by screensharing our code and a little in person
2) We mostly work together, but the time we worked independently was each of us coming up with a basic 
algorithm of how the implementation may look like, so that when we meet, we somewhat have a basis for discussion
3) None of the tasks came up unplanned. We did find that implementing the second feature (new anomaly) was much harder
compared loading a text file
4) As planned, we would switch for each feature (so driver on featuer 1 would be navigator for feature 2), and this did work for the
first category. However, category 2 requires much more work for us, so when the driver felt stucked, we would switch role. 
5) In the future, we might prefer meeting in person more often because in person, we could share both of our screens at the sametime, 
while screensharing could only take one screen at a time, so the navigator would sometimes find it difficult to navigate. 
"""


import Duty
import random
import sys


def main():
    """
    The main function is mostly just here to setup the game and keep it running in a loop.
    It has a specific order of events that it follows.
    There are a lot of comments in here to help you understand what is going on, but 
    feel free to remove them if they impede your reading of the code.
    """

    # First, we set up all of the game data. 
    # This could have been done using the init() function's optional parameters,
    # but this should make it easier for you to modify it later.

    # These 'helper functions' just clean up the main function and make it more readable.
    # We need to add rooms to the game and we need to register what anomalies are possible.
    add_rooms()
    register_anomalies()

    # It might be cleaner to put all of these into their own helper function. Feel free to do that if you think it would be better!
    game_settings()
    # Initialize the game with all of the data we've just set up.
    game_running = True
    while game_running:
        # The game keeps track of time while the player is idle, so it is possible we will need
        # to create multiple anomalies at a time the next time the player types a command.
        # `number_of_anomalies_to_create` also takes our probability setting into account.
        n_anomalies = Duty.number_of_anomalies_to_create()

        # We create one anomaly at a time, and we'll write a small helper function to clean up the main function.
        for _ in range(n_anomalies):
            # Keep looping until we can create the anomaly, just in case one of them fails
            anomaly_created = False
            while not anomaly_created:
                anomaly_created = create_anomaly()
            

        # This will update the game status to check if we've lost the game or reached the end.
        # Update returns True if the game should keep going or False if it should end after this loop.
        game_running = Duty.update()

        # Display shows all of the game data. If update() determined the game should end, display() will show the end screen.
        Duty.display()

        # This will pause the loop and wait for the user to type something, running the appropriate commands
        # to handle their actions.
        Duty.handle_input()    # This is the main game loop. It will run until the game_running variable is set to False.

def game_settings():
    #Default setting if user doesn't enter anything in the command-lin argument. This is equivalent to the normal level
    settings_list = [5, 45,0.05,900]
    #Check if command-line argument exists
    if len(sys.argv) >= 2:
        #Load up the text file
        filehandle = open("settings.txt","r")
        #Keep reading the text file until finds a level in the text that matches with the user's choice
        while True:
            data = filehandle.readline()
            #The strip method is to strip out the white spaces from the text file
            if sys.argv[1].upper() == data.strip():
                #Once the level has been found, change the element of the list
                for i in range(4):
                    data = filehandle.readline()
                    settings_list[i] = data
                break
            #If command-line argument is found but doesn't match, keep reading the file until it ends
            elif data == "":
                break
        filehandle.close()
    Duty.set_setting("debug", False)# Setting this to True will show additional information to help you debug new anomalies
    #Making the user wait longer when report the anomaly, so the shift could go over quicker, and new anomalies could happen meanwhile
    Duty.set_setting("anomaly_report_time", settings_list[0]) 
    #Setting the game's settings according to the list
    Duty.set_setting("timescale", settings_list[1])
    Duty.set_setting("probability", settings_list[2])
    Duty.set_setting("min_seconds_between_anomalies", settings_list[3])
    Duty.init()

def add_rooms():
    """
    Adds all of the rooms to the game. 
    Duty.add_room() takes a string for the name of a room and a list of strings for the items in the room.
    """
    Duty.add_room("Living Room", ["42\" TV Playing Golf", "Black Leather Sofa", "Circular Metal Coffee Table", "Wooden Bookshelf with 3 Shelves"])
    Duty.add_room("Kitchen", ["Gas Stove", "Retro Red Metal Refrigerator", "Oak Wooden Table", "4 Wooden Chairs"])
    Duty.add_room("Bedroom", ["Queen Size Bed", "Oak Wooden Nightstand", "Oak Wooden Dresser", "Oak Wooden Desk", "Oak Wooden Chair"])
    Duty.add_room("Bathroom", ["Toilet with Oak Seat", "Chrome Sink", "Shower with Blue Tiles", "Medicine Cabinet"])


def register_anomalies():
    """
    Each anomaly we want to add to the game must be "Registered". 
    This is so the game knows what anomalies are possible.
    They will all be stored in UPPERCASE to make it easier to compare them later.
    """
    Duty.register_anomaly("CAMERA MALFUNCTION")
    Duty.register_anomaly("MISSING ITEM")
    Duty.register_anomaly("ITEM MOVEMENT")
    Duty.register_anomaly("MATERIAL CHANGE")
    

    
def create_anomaly() -> bool:
    """
    This little helper function handles the control flow for three steps:
    1. Choose a random room that does not have an anomaly, because rooms can only have one anomaly.
    2. Choose a random anomaly from the list of registered anomalies.
    3. Create the anomaly in the room.

    Return True if an anomaly was created, False if no anomaly was created.
    """

    # Choose a random room that does not have an anomaly
    room = Duty.get_random_unchanged_room()

    # Pick a random anomaly from the list of registered anomalies
    # Note: It is possible that some anomalies you create can't work in every room.
    # Maybe you will need additional logic to make sure the anomaly makes sense in the room.
    
    #anomaly = Duty.get_random_anomaly()
    anomaly = "MATERIAL CHANGE"
    # Camera Malfunction is actually a special one.
    # It will not show this camera when clicking through if 
    # It sees CAMERA MALFUNCTION as the anomaly name
    if anomaly == "CAMERA MALFUNCTION":
        # All anomalies are stores as all uppercase
        # Since a camera malfunction means no items are shown, we pass an empty list
        return Duty.add_anomaly("CAMERA MALFUNCTION", room, [])
    elif anomaly == "MISSING ITEM":
        # We pass the name of the room to these functions to separate out the logic
        return missing_item(room)
    elif anomaly == "ITEM MOVEMENT":
        return item_movement(room)
    elif anomaly == "MATERIAL CHANGE":
        return material_change(room)
    else:
        print(f"ERROR: Anomaly {anomaly} not found")
        return False

def missing_item(room: str) -> bool:
    """
    Removes a random item from the room. This is a pretty straightforward one.
    1. Get the list of items in the room. (Duty.get_room_items())
    2. Choose a random item to remove. (random.randint())
    3. Make a copy of the list of items and remove the item from the copy. (list slicing)
    4. Create the anomaly with the new list of items. (Duty.add_anomaly())
    """
    items = Duty.get_room_items(room)
    item_index_to_remove = random.randint(0, len(items)-1)
    new_items = items[:]
    new_items.pop(item_index_to_remove)
    
    # add_anomaly returns True if the anomaly was created, False if it was not.
    return Duty.add_anomaly("MISSING ITEM", room, new_items)

def item_movement(room: str) -> bool:
    """
    Re-arranges two items in a room. This one is a little more complicated.
    1. Get the list of items in the room. (Duty.get_room_items())
    2. Choose two random items to swap. (random.randint())
    3. Make a copy of the list of items and swap the two items. (list slicing)
    4. Create the anomaly with the new list of items. (Duty.add_anomaly())
    """

    items = Duty.get_room_items(room)

    # If there is only one item in the room, we can't move anything!
    if len(items) < 2:
        return False

    # Find two random items to swap
    item_to_move = random.randint(0, len(items)-1)
    item_to_move_to = random.randint(0, len(items)-1)

    # Make sure the two items are not the same
    while item_to_move == item_to_move_to:
        item_to_move_to = random.randint(0, len(items)-1)

    # Make a copy to avoid accidentally modifying the original item list
    new_items = items[:]

    # The below swap is also possible with the line: new_items[item_to_move], new_items[item_to_move_to] = new_items[item_to_move_to], new_items[item_to_move]
    item_a = new_items[item_to_move]
    item_b = new_items[item_to_move_to]
    new_items[item_to_move] = item_b
    new_items[item_to_move_to] = item_a

    return Duty.add_anomaly("ITEM MOVEMENT", room, new_items)

def material_change(room: str) -> bool:
    materials = ["Leather","Metal","Wooden", "Oak"]
    items = Duty.get_room_items(room)
    
    #Copy the items and list of materials so it wouldn't be unintentionally changed
    new_items = items[:]
    new_materials = materials[:]
    
    
    #Choosing a random material from the material lists to swap 
    random_material = random.randint(0,len(new_materials)-1)
    pop_material = new_materials.pop(random_material)          

    
    #Make sure that it always pop out an item that has a material description in it
    while True:
        #Choosing a random item from the list of items
        random_item = random.randint(0,len(new_items)-1)
        pop_item = new_items.pop(random_item)
        #Check if the item does contain a material description, in this case leather.
        if "Leather" in pop_item:
            #If the material to change is the same thing as the material of the item, choose another
            #material until that is not equal to the material of the item
            while pop_material == "Leather":
                new_materials.insert(random_material,pop_material)
                random_material = random.randint(0,len(new_materials)-1)
                pop_material = new_materials.pop(random_material)
            
            #Find where in the string is the material description is placed
            i = pop_item.find("Leather")
            #Cut out the original material and replace it with the new material
            pop_item = pop_item[:i] + pop_material + pop_item[i + len("Leather"):]                                 
            
            break
        elif "Metal" in pop_item:
            while pop_material == "Metal":
                new_materials.insert(random_material,pop_material)
                random_material = random.randint(0,len(new_materials)-1)
                pop_material = new_materials.pop(random_material)
                
            i = pop_item.find("Metal")
            pop_item = pop_item[:i] + pop_material + pop_item[i + len("Metal"):]
            
            break
            
        elif "Wooden" in pop_item:
            while pop_material == "Wooden":
                new_materials.insert(random_material,pop_material)
                random_material = random.randint(0,len(new_materials)-1)
                pop_material = new_materials.pop(random_material)
                
            i = pop_item.find("Wooden")
            pop_item = pop_item[:i] + pop_material + pop_item[i + len("Wooden"):]
            
            break
        elif "Oak" in pop_item:
            while pop_material == "Oak":
                new_materials.insert(random_material,pop_material)
                random_material = random.randint(0,len(new_materials)-1)
                pop_material = new_materials.pop(random_material)
                
            i = pop_item.find("Oak")
            pop_item = pop_item[:i] + pop_material + pop_item[i + len("Oak"):]
            
            break         
        #If the popped out item doesn't have a material description, insert it back to find another item
        else:
            new_items.insert(random_item, pop_item)
        
    #Append the modified item back into the list
    new_items.insert(random_item,pop_item)
    
    return Duty.add_anomaly("MATERIAL CHANGE",room,new_items)
    
    
main()
