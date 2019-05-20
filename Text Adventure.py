class Thing:
    '''Fields: id (Nat),
               name (Str),
               description (Str)
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        
    def __repr__(self):
        return '<thing #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        
class Player:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               location (Room),
               inventory ((listof Thing))
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.location = None
        self.inventory = []
        
    def __repr__(self):
        return '<player #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.inventory) != 0:
            print('Carrying: {0}.'.format(
                ', '.join(map(lambda x: x.name,self.inventory))))
 
class Room:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               contents ((listof Thing)),
               exits ((listof Exit))
    '''    
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.contents = []
        self.exits = []
        
    def __repr__(self):
        return '<room {0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.contents) != 0:
            print('Contents: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.contents))))
        if len(self.exits) != 0:
            print('Exits: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.exits)))) 
 
class Exit:
    '''Fields: name (Str), 
               destination (Room)
               key(Thing)
               message(Str)
    '''       
    
    def __init__(self,name,dest):
        self.name = name
        self.destination = dest
        self.key = None
        self.message = ''
        
    def __repr__(self):
        return '<exit {0}>'.format(self.name)

class World:
    '''Fields: rooms ((listof Room)), 
               player (Player)
    '''       
    
    msg_look_fail = "You don't see that here."
    msg_no_inventory = "You aren't carrying anything."
    msg_take_succ = "Taken."
    msg_take_fail = "You can't take that."
    msg_drop_succ = "Dropped."
    msg_drop_fail = "You aren't carrying that."
    msg_go_fail = "You can't go that way."
    
    msg_quit = "Goodbye."
    msg_verb_fail = "I don't understand that."
    
    def __init__(self, rooms, player):
        self.rooms = rooms
        self.player = player

    def look(self, noun):
        '''
        returns None and print the status of noun onto the screen, and if noun 
        can't be find anywhere, the program will print 'you don't see that here'
        effect: prints strings onto the screen
        
        look: World Str -> None
        '''
        inventory_name = list(map(lambda x: x.name, self.player.inventory))
        contents = list(map(lambda x: x.name, self.player.location.contents))
        if noun == 'me':
            self.player.look()
        elif noun == 'here':
            self.player.location.look()
        elif noun in inventory_name :
            for item in self.player.inventory :
                if item.name == noun:
                    item.look()
        elif noun in contents :
            for item in self.player.location.contents:
                if item.name == noun:
                    item.look()
        else:
            print(self.msg_look_fail)
            
    def inventory(self):
        '''
        returns None and prints the player's inventory onto the screen
        effect: prints a string onto the screen
        
        inventory: World -> None
        '''
        if self.player.inventory == []:
            print(self.msg_no_inventory)
        else:
            inventory_name = list(map(lambda x: x.name, self.player.inventory))
            message = ', '.join(inventory_name)
            print('Inventory: ' + message)
            
    def take(self, noun):
        '''
        returns None and prints a message which indicates whether player 
        successfully take noun or not onto the screen and mutates the contents 
        of player's location and players' inventory.
        effect: print a string onto the screen
                mutates World
        
        take: World Str -> None
        '''
        contents = list(map(lambda x: x.name, self.player.location.contents))
        if noun in contents :
            for item in self.player.location.contents:
                if item.name == noun:
                    self.player.inventory.append(item)
                    self.player.location.contents.remove(item)
                    print(self.msg_take_succ)
        else:
            print(self.msg_take_fail)
            
    def drop(self, noun):
        '''
        returns None and prints a message which indicates whether player 
        successfully drop noun or not onto the screen and mutates the contents 
        of player's location and players' inventory.
        effect: print a string onto the screen
                mutates World
        
        drop: World Str -> None
        '''        
        inventory_names = list(map(lambda x: x.name, self.player.inventory))
        if noun in inventory_names:
            for item in self.player.inventory:
                if item.name == noun :
                    self.player.location.contents.append(item)
                    self.player.inventory.remove(item)
                    print(self.msg_drop_succ)
        else:
            print(self.msg_drop_fail)
        
    def go(self, noun):
        '''
        returns None and prints the status of players new location and mutates 
        the player's location to the new one.
        effect: print a string onto the screen
                mutates World
                
        go: World Str -> None
        '''
        exit_names = list(map(lambda x: x.name, self.player.location.exits))
        if noun in exit_names:
            for exit in self.player.location.exits :
                if exit.name == noun:
                    if exit.key == None:
                        self.player.location = exit.destination
                        self.player.location.look()
                    elif exit.key in self.player.inventory:
                        self.player.location = exit.destination
                        self.player.location.look()
                    else:
                        print(exit.message)
        else:
            print(self.msg_go_fail)
        
                
    def play(self):
        player = self.player
        
        player.location.look()
        
        while True:
            line = input( "- " )
            
            wds = line.split()
            verb = wds[0]
            noun = ' '.join( wds[1:] )
            
            if verb == 'quit':
                print( self.msg_quit )
                return
            elif verb == 'look':
                if len(noun) > 0:
                    self.look(noun)  
                else:
                    self.look('here')
            elif verb == 'inventory':
                self.inventory()     
            elif verb == 'take':
                self.take(noun)    
            elif verb == 'drop':
                self.drop(noun)
            elif verb == 'go':
                self.go(noun)   
            else:
                print( self.msg_verb_fail )

    ## Q3
    def save(self, fname):
        '''
        returns None and save the state of the world to a file called fname
        effect: writing to a file called fname
        
        save: World Str -> None
        '''
        f = open(fname, 'w')
        for item in self.player.inventory:
            f.write("thing #")
            f.write(str(item.id))
            f.write(' ')
            f.write(item.name)
            f.write('\n')
            f.write(item.description)
            f.write('\n')
        for room in self.rooms:
            for item in room.contents:
                f.write("thing #")
                f.write(str(item.id))
                f.write(' ')
                f.write(item.name)
                f.write('\n')
                f.write(item.description)
                f.write('\n')
        for room in self.rooms:
            f.write('room #')
            f.write(str(room.id))
            f.write(' ')
            f.write(room.name)
            f.write('\n')
            f.write(room.description)
            f.write('\n')
            f.write('contents')
            for item in room.contents:
                f.write(' #')
                f.write(str(item.id))
            f.write('\n')
        player = self.player
        f.write('player #')
        f.write(str(player.id))
        f.write(' ')
        f.write(player.name)
        f.write('\n')
        f.write(player.description)
        f.write('\n')
        f.write('inventory')
        for item in player.inventory:
            f.write(' #')
            f.write(str(item.id))
        f.write('\n')
        f.write('location #')
        f.write(str(player.location.id))
        f.write('\n')
        for room in self.rooms:
            for exit in room.exits:
                if exit.key == None:
                    f.write('exit #')
                    f.write(str(room.id))
                    f.write(' #')
                    f.write(str(exit.destination.id))
                    f.write(' ')
                    f.write(exit.name)
                    f.write('\n')
                else:
                    f.write('keyexit #')
                    f.write(str(room.id))
                    f.write(' #')
                    f.write(str(exit.destination.id))
                    f.write(' ')
                    f.write(exit.name)
                    f.write('\n')
                    f.write('#')
                    f.write(str(exit.key.id))
                    f.write(' ')
                    f.write(exit.message)
                    f.write('\n')
        f.close()        
        

## Q2
def load( fname ):
    '''
    returns None and load a game form a file called fname
    effect: read from a file called fname
    
    load: Str -> None
    '''
    f = open(fname)
    l = f.readline()
    things = []
    rooms = []
    while l != '':
        words = l.split()
        genre = words[0]
        if genre == 'thing' :
            id = int(words[1][1:])
            thing = Thing(id)
            thing.name = ' '.join(words[2:])
            l1 = f.readline()
            thing.description = l1
            things.append(thing)
        elif genre == 'room' :
            room_id = int(words[1][1:])
            room = Room(room_id)
            room.name = ' '.join(words[2:])
            l1 = f.readline()
            room.description = l1
            l2 = f.readline()
            thing_ids = list(map(lambda x: int(x[1:]), l2.split()[1:]))
            room.contents = []
            for id in thing_ids :
                for item in things:
                    if item.id == id:
                        room.contents.append(item)
            room.exits = []
            rooms.append(room)
        elif genre == 'player' :
            player_id = int(words[1][1:])
            player = Player(player_id)
            player.name = ' '.join(words[2:])
            l1 = f.readline()
            player.description = l1
            l2 = f.readline()
            thing_ids = list(map(lambda x: int(x[1:]), l2.split()[1:]))
            player.inventory = []
            for id in thing_ids :
                for item in things:
                    if item.id == id:
                        player.inventory.append(item)
            l3 = f.readline()
            room_id = int(l3.split()[1][1:])
            for room in rooms:
                if room.id == room_id:
                    player.location = room
        elif genre == 'exit' :
            exit_entrance_number = int(words[1][1:])
            exit_destination_number = int(words[2][1:])
            for room in rooms:
                if room.id == exit_destination_number :
                    exit_destination = room
            exit_name = ' '.join(words[3:])
            exit = Exit(exit_name,exit_destination)
            for room in rooms:
                if room.id == exit_entrance_number :
                    room.exits.append(exit)
        else:
            exit_entrance_number = int(words[1][1:])
            exit_destination_number = int(words[2][1:])
            for room in rooms:
                if room.id == exit_destination_number :
                    exit_destination = room
            exit_name = ' '.join(words[3:])
            exit = Exit(exit_name,exit_destination)
            l1 = f.readline()
            words2 = l1.split()
            exit_key_number = int(words2[0][1:])
            for item in things:
                if item.id == exit_key_number:
                    exit.key = item
            exit.message = ' '.join(words2[1:])
            for room in rooms:
                if room.id == exit_entrance_number :
                    room.exits.append(exit)            
        l = f.readline()
    world = World(rooms,player)
    f.close()
    return world
            
def makeTestWorld(usekey):
    wallet = Thing(1)
    wallet.name = 'wallet'
    wallet.description = 'A black leather wallet containing a WatCard.'
    
    keys = Thing(2)
    keys.name = 'keys'
    keys.description = 'A metal keyring holding a number of office and home keys.'
    
    phone = Thing(3)
    phone.name = 'phone'
    phone.description = 'A late-model smartphone in a Hello Kitty protective case.'
    
    coffee = Thing(4)
    coffee.name = 'cup of coffee'
    coffee.description = 'A steaming cup of black coffee.'
    
    hallway = Room(5)
    hallway.name = 'Hallway'
    hallway.description = 'You are in the hallway of a university building. \
Students are coming and going every which way.'
    
    c_and_d = Room(6)
    c_and_d.name = 'Coffee Shop'
    c_and_d.description = 'You are in the student-run coffee shop. Your mouth \
waters as you scan the room, seeing many fine foodstuffs available for purchase.'
    
    classroom = Room(7)
    classroom.name = 'Classroom'
    classroom.description = 'You are in a nondescript university classroom. \
Students sit in rows at tables, pointedly ignoring the professor, who\'s \
shouting and waving his arms about at the front of the room.'
    
    player = Player(8)
    player.name = 'Stu Dent'
    player.description = 'Stu Dent is an undergraduate Math student at the \
University of Waterloo, who is excelling at this studies despite the fact that \
his name is a terrible pun.'
    
    c_and_d.contents.append(coffee)
    player.inventory.extend([wallet,keys,phone])
    player.location = hallway
    
    hallway.exits.append(Exit('shop', c_and_d))
    ex = Exit('west', classroom)
    if usekey:
        ex.key = coffee
        ex.message = 'On second thought, it might be better to grab a \
cup of coffee before heading to class.'
    hallway.exits.append(ex)
    c_and_d.exits.append(Exit('hall', hallway))
    classroom.exits.append(Exit('hall', hallway))
    
    return World([hallway,c_and_d,classroom], player)

testworld = makeTestWorld(False)
testworld_key = makeTestWorld(True)

