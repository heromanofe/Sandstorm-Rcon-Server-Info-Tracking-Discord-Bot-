###############################################################################
ment2 = 1
sec_e = ""
ins_e = ""
last_state = ""
message_counting = 0
##############################################################################
class Server_match:
    def __init__(self, ip, server_port,password, game, mcr, short_name, full_name,max_score, query):
        self.ip = ip #IP
        self.server_port = server_port  #RCON port
        self.password = password
        self.game_port = game
        self.query = query
        self.mcr = mcr
        self.short_name = short_name
        self.full_name = full_name
        self.max_score = max_score
    timer = 0
    lost = 0
    tries = 0
    max_players=0
    bot_count= 0
    error = 0
    mss =""
    check_for_first_level= 1
    check_for_second_level = 1
    Match_state = "NONE, NO" ##for example, ROUND ACTIVE
    ins_wins= 0 #Curently how many rounds won INSURGENTS
    server_number = 0 #number, like #2
    security_wins = 0 #sec wins
    map = "NONE" #MAP on server
    second_map = ""
    lastWin_team = 3
    dogs = ""
    pug_state = ""
    players_count = "0"
    obj_name = ""
    obj_type = ""
    mutators = ""
    edit_error = 0
##############################################################################
def numbers(num):
    mmm = ""
    if num == 0:
        mmm = "0️⃣"
    elif num == 1:
        mmm = "1️⃣"
    elif num == 2:
        mmm = "2️⃣"
    elif num == 3:
        mmm = "3️⃣"
    elif num == 4:
        mmm = "4️⃣"
    elif num == 5:
        mmm = "5️⃣"
    elif num == 6:
        mmm = "6️⃣"
    elif num == 7:
        mmm = "7️⃣"
    elif num == 8:
        mmm = "8️⃣"
    elif num == 9:
        mmm = "9️⃣"
    return mmm

def Obj_naming(num):
    mmm = ""
    if num == "A":
        mmm = "Alpha"
    elif num == "B":
        mmm = "Bravo"
    elif num == "C":
        mmm = "Charlie"
    elif num == "D":
        mmm = "Delta"
    elif num == "E":
        mmm = "Echo"
    elif num == 'F':
        mmm = "Foxtrot"
    elif num == 'G':
        mmm = "G"
    elif num == "H":
        mmm = "Hotel"
    elif num == "I":
        mmm = "I"
    elif num == "J":
        mmm = "J"
    else:mmm=num
    return mmm


def Map_naming(num):
    mmm = ""
    if num == "Canyon":
        mmm = "Crossing"
    elif num == "Farmhouse":
        mmm = "Farmhouse"
    elif num == "Town":
        mmm = "Hideout"
    elif num == "Sinjar":
        mmm = "Hillside"
    elif num == "Ministry":
        mmm = "Ministry"
    elif num == 'Compound':
        mmm = "Outskirts"
    elif num == 'PowerPlant':
        mmm = "PowerPlant"
    elif num == "Precinct":
        mmm = "Precinct"
    elif num == "Mountain":
        mmm = "Summit"
    elif num == "Buhriz":
        mmm = "Tideway"
    elif num == "Oilfield":
        mmm = "Refinery"
    else:mmm=num
    return mmm
