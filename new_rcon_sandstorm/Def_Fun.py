import mcrcon_new,sqlite3,re,asyncio,discord,Classes, Config
mcrcon= mcrcon_new
import valve.source
import valve.source.a2s
import valve.source.master_server
from datetime import datetime
import time
import valve.rcon
#################################################################################################
My_id= 0 #Here you could put sumeones discord ID so he could do admin stuff with this bot without being Server owner
all_servers = Config.all_ser()
last_state = Classes.last_state
message_counting = Classes.message_counting
#################################################################################################
#sec_e = Classes.sec_e
#ins_e = Classes.ins_e
async def Initial_setup():
    global all_servers
    conn = sqlite3.connect("db_server_info.db")
    c = conn.cursor()
    result = c.execute('SELECT ip,r_port,password,g_port, short_name, full_name, max_score, query from Server_list').fetchall()
    for row in result:
        do = 1
        for i in all_servers:
            if i.ip != row[0] and i.server_port != row[1] and i.password != row[2]:
                if do != 0: do = 1
                
            else: 
                do = 0
        if do == 1:
            mcr = mcrcon.MCRcon(row[0],row[2],row[1])
            try:
                mcr.connect()
                all_servers.append(Classes.Server_match(row[0], row[1], row[2],row[3], mcr, row[4], row[5], row[6], row[7]))
            except: 
                if len(all_servers) > 0:
                  all_servers.remove(all_servers[len(all_servers)-1])
                print("ERROR, DIDN'T CONNECTED TO RCON")
    return all_servers
        

####################################################################################################################
async def rcon_things(message, b, curently_tracking):
        global a
        global last_state
        global pug_state
        global sec_e
        global ins_e
        mcr = b.mcr
        #await asyncio.sleep(1)
        count = 0
        k = ""
        if b.check_for_first_level == 1:
            print("------------------------------------------------------------------")
            resp = b.mcr.command("gamemodeproperty Mutators") 
            s = resp.split("'")
            mutators = "| "
            for l in s:
                if l[0] != '"'and l[len(l)-1] and l[0]!= '"' and '('!= l[0]:
                    mutators += l
            mutators = mutators.replace('Mutators = ','').replace('"', "").replace(")", "").replace("(", "").replace(",", " | ")
            b.mutators = mutators.replace('BP_Mutator_', "").replace("_c", "")
            k = "SERVER TRACKING INITIALIZED FOR THE FIRST TIME ON: {0}".format(b.ip+":"+str(b.game_port))
            b.check_for_first_level = 0
            b.check_for_second_level = 1
            resp = ""
            print("------- USED RCON FOR SERVER {0} (FIRST TIME MUTATORS GRAB) FOUND THIS: {1} ------- {2}".format(b.ip+":"+str(b.game_port), b.mutators, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        if b.map.split(" ")[0] != b.second_map and int(b.players_count) > 0:
            b.check_for_second_level = 1
            k="MAP IN (RCON): {0} | SCENARIO:{1} IS DIFFERENT FROM QUERY GRABED MAP: {2}".format(b.map.split(" ")[0],b.map, b.second_map)
        if b.check_for_second_level == 1:
            b.map = mcr.command("gamemodeproperty MultiplayerScenario")
            reg = re.compile(r"\.Scenario_+\w+")
            b.map = re.findall(reg, b.map)
            if k !="": reason = k
            else: reason = "Other reason"
            if len(b.map)>0:
                b.map = b.map[0].replace("_", " ").replace("Scenario","").replace(".","").strip()
            else: b.map = 'No map'
            b.check_for_second_level = 0
            print("------- USED RCON FOR SERVER {0} (CHECKING FOR SCENARIO BECAUSE OF:{1}) SCENARIO NOW IS: {2} -------".format(b.ip+":"+str(b.game_port), reason, b.map)+"  |  "+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"  |")
            print("------------------------------------------------------------------")
            b.timer = 0
            ############################
           # resp = mcr.command("gamemodeproperty LastWinningTeam")
            #print(resp)
            #b.lastWin_team = int(resp.split(" ")[2].replace('"',''))
        b.error = 1
        ####################################################### MATCH STATE CHANGED ################################################4
        #resp = mcr.command("gamemodeproperty MatchState")
        #resp = mcr.command("travel Ministry?Scenario=Scenario_Ministry_Checkpoint_Security")
        #resp = mcr.command("gamemodeproperty ActiveObjectiveId")
        #print(resp)
        resp = ""
        b.match_state=""
        if(resp != b.Match_state):
            b.Match_state = resp
            dogs = ""
            k = b.map.split(" ")
            if b.map.split(" ")[len(k)-1] == "Insurgents":
                    b.dogs = "Ins"
            else:b.dogs = "Sec"
            b.error = 2
            if b.Match_state == 'MatchState = "RoundWon"': #RoundWon
                resp = mcr.command("gamemodeproperty LastWinningTeam")
                print(resp)
                b.lastWin_team = int(resp.split(" ")[2].replace('"',''))
                if b.lastWin_team == 1:
                   b.ins_wins = int(b.ins_wins) +1
                elif b.lastWin_team == 255: 
                    b.ins_wins = b.ins_wins +1
                    b.security_wins=int(b.security_wins)+1
                else:
                    b.security_wins=int(b.security_wins)+1
                print("sec: "+str(b.security_wins))
                print("ins: "+str(b.ins_wins))
                print("{0}:{1}".format(b.ip, str(b.game_port)))
            llo = 0
            llp = 0
            if b.dogs == "Ins": 
                llo = b.ins_wins
                llp = b.security_wins
            else: 
                llo = b.security_wins
                llp = b.ins_wins
            b.error = 3
            if b.Match_state == 'MatchState = "NONEee"' or llo >=1 or llp >= b.max_score:
                b.ins_wins= 0 #Curently how many rounds won INSURGENTS
                b.security_wins = 0 #sec wins
                b.map = "NONE" #MAP on server
                b.lastWin_team = 3
                b.check_for_second_level = 1
        b.error = 3
        #resp = mcr.command("gamemodeproperty ActiveObjective")
        resp= 'Could not find property "ActiveObjective"'
        if resp == 'Could not find property "ActiveObjective"':
            b.obj_name ="Name"
            b.obj_type = "Type"
        else:
            b.obj_type = resp.split("'")[0].split('"')[1]
            b.obj_type = b.obj_type[9:len(b.obj_type)]
            b.obj_name = resp.split("_")
            b.obj_name =  b.obj_name[len(b.obj_name)-1].split("'")[0]
            if 'nCache' in b.obj_type:b.obj_type = "WeaponCache"
        
        await Match_state(message, b)

                    

#############################################################################################################################################
async def Match_state(message, b):
        global pug_state
        sec_e = Classes.sec_e
        ins_e = Classes.ins_e
        global Matchess
        numbers = Classes.numbers
        m=[]
        b.error = 4
        players = await players_query(b)
 #   for b in curently_tracking:
        embed = discord.Embed(colour=discord.Colour(0xd0021b))
        if b.lastWin_team == 0:mda = "Sec" 
        elif b.lastWin_team == 1:mda ="Ins"
        elif b.lastWin_team == 3:mda = "NONE"
        elif b.lastWin_team == 255:mda = "Draw"
        else: mda = "Error?"
        if mda == b.dogs: mda ="OLD DOGS"
        elif mda == "Draw":mda = "DRAW" 
        else: mda = "BOT TEAM"
        ll = ""
        llk = ""
        if b.dogs == "Sec":
            ll = "<:Security:{0}>".format(sec_e.id)
            llk = "<:insurgents:{0}>".format(ins_e.id)
        else:
            llk = "<:Security:{0}>".format(sec_e.id)
            ll = "<:insurgents:{0}>".format(ins_e.id)
        scp = []
        scp.append("")
        scp.append("")
        sc = []
        sc.append("")
        sc.append("")
        if b.ins_wins <= 9:
            scp[0]=":zero:"
            scp[1]=numbers(b.ins_wins)
        else:
            scp[0]=numbers(int(str(b.ins_wins)[0]))
            scp[1]=numbers(int(str(b.ins_wins)[1]))
        match = b.Match_state.replace('MatchState =', '').replace(" ",'').replace('"','')
        oke = ""
        other = ""
        #b.full_name = b.short_name+" || "+b.full_name
        if b.security_wins <= 9:
            sc[0]=":zero:"
            sc[1]=numbers(b.security_wins)
        else:
            sc[0]=numbers(int(str(b.security_wins)[0]))
            sc[1]=numbers(int(str(b.security_wins)[1]))
        if b.dogs == "Ins":
            dogs = scp[0]+scp[1]
            dogs_team = ins_e
            enemy = sc[0]+sc[1]
            enemy_team = sec_e
        else: 
            dogs = sc[0]+sc[1]
            dogs_team = sec_e
            enemy = scp[0]+scp[1]
            enemy_team = ins_e
        b.obj_name = Classes.Obj_naming(b.obj_name)
       # serv_full = b.full_name
        
        embed.add_field(name='{1}```{0:^30}```{1}'.format(b.full_name, dogs_team), value="**Players:** `{0}\{1}`\n**Map:** `{2}`".format(str(b.players_count),str(b.max_players), b.map), inline=True)#**Match_state:** `{2}`\n**Last Winning Team:** `{2}`\n**Curently on:** `{3} ({4})`\n**Map:** `{5}`".format(b.players_count,match, mda,b.obj_name, b.obj_type, b.map), inline=True)**OLD DOGS**|{1}| --{0}-- |
        embed.add_field(name='\u200b', value='\u200b', inline = True)
        embed.add_field(name="\u200b", value="​​​​​​​ **Mutators**: `{1}`\n```cs\n{0:^28}```".format(b.ip+":"+str(b.game_port), b.mutators), inline=True) #\u200b \u200b \u200b \u200b \u200b \u200b \u200b **BOT TEAM**|{1}| --{0}--  |     serv_full
        #players = await players_query(b)
        pl = "```| [NR] |        PLAYER NAME       | SCORE |      Time       |\n|------|--------------------------|-------|-HRS-|-MIN-|-SEC-|\n"
        scoreing = 0
        
        for play in players:
            scs= ""
            if scoreing+1 < 9: scs = "0"+str(scoreing+1)
            else: scs = str(scoreing+1)
            pl += "| [{0}{1:^26}|{2:^7}|{3:^5}|{4:^5}|{5:^5}|\n".format(scs+"] |",play.name, play.score, play.hrs, play.mins, play.secs)
            scoreing+=1
        embed.add_field(name="===========================================================", value="{0}\n|___________________________________________________________|```".format(pl))
        m = embed
        b.error = 5
        #if int(b.players_count) > 0:
        if b.pug_state == "":
                b.pug_state = await message.channel.send(embed=m)
                b.error = 6
        else:
                b.error = 7
                try:
                    await b.pug_state.edit(embed=m)
                    b.edit_error = 0
                except:
                    print("Error!! couldn't edit message.!!"+"  |  "+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"  |")
                    b.edit_error += 1
                    if b.edit_error >= 5:
                        b.pug_state = await message.channel.send(embed=m)
     #   else:
      #      if b.pug_state != "":
       #         await b.pug_state.delete()
        #        b.pug_state = ""
async def players_query(b):
        SERVER_ADDRESS = (b.ip, b.query)
        if b.query == 0:
            SERVER_ADDRESS = ("62.171.147.243", 27131)
        with valve.source.a2s.ServerQuerier(SERVER_ADDRESS, 2) as server:
            try:
                info = server.info()
                players = server.players()
                k = []
                class player_info:
                    def __init__(self, score, name, duration):
                        self.score = score 
                        self.name = name 
                        self.duration = duration
                    hrs=0
                    mins=0
                    secs=0

                b.full_name = "{server_name}".format(**info)

                b.second_map = "{map}".format(**info)
                b.second_map = Classes.Map_naming(b.second_map)
                b.players_count = "{player_count}".format(**info)
                b.max_players = "{max_players}".format(**info)
                for player in sorted(players["players"],
                                 key=lambda p: p["score"], reverse=True):
                    k.append(player_info("{score}".format(**player),"{name}".format(**player),"{duration}".format(**player)))
                    lol = ""
                    sec = float(k[len(k)-1].duration.split(".")[0])
                    min = 0
                    if sec>60:
                        min = float(sec/60.0)
                        min = int(str(min).split(".")[0])
                        sec = sec - (60*min)
                        sec = int(str(sec).split(".")[0])
                        if sec == 60: 
                            min+=1
                            sec = 0
                    hr = 0.0
                    if min > 60:
                        hr = min/60.0
                        hr = int(str(hr).split(".")[0])
                        min = min - (60*hr)

                        if min == 60:
                            hr+=1
                            min = 0
                    sec = int(str(sec).split('.')[0])
                    min = int(str(min).split('.')[0])
                    hr = int(str(hr).split('.')[0])
                    if hr != 0 or hr != 0.0: 
                        lol += "Hr:"+str(hr)+"-"
                        k[len(k)-1].hrs=str(hr)
                    else: k[len(k)-1].hrs="0"
                    if min != 0 or min != 0.0: 
                        lol+="M:"+str(min)+"-"
                        k[len(k)-1].mins=str(min)
                    else: k[len(k)-1].mins="0"
                    if sec != 0 or sec != 0.0: 
                        lol+="S:"+str(sec)
                        k[len(k)-1].secs=str(sec)
                    else: k[len(k)-1].secs="0"
                    k[len(k)-1].duration = lol
            except: 
                k = ""
            return k
########################################################################################################
