import mcrcon_new,sqlite3,re,asyncio,discord,Classes
mcrcon= mcrcon_new

#################################################################################################
all_servers = []
last_state = Classes.last_state
message_counting = Classes.message_counting
#################################################################################################
#sec_e = Classes.sec_e
#ins_e = Classes.ins_e
async def Initial_setup():
    global all_servers
    conn = sqlite3.connect("db_server_info.db")
    c = conn.cursor()
    result = c.execute('SELECT ip,r_port,password,g_port, short_name, full_name, max_score from Server_list').fetchall()
    for row in result:
        do = 1
        for i in all_servers:
            if i.ip != row[0] and i.server_port != row[1] and i.password != row[2]:do = 1
            else: do = 0
        if do == 1:
            mcr = mcrcon.MCRcon(row[0],row[2],row[1])
            try:
                mcr.connect()
                all_servers.append(Classes.Server_match(row[0], row[1], row[2],row[3], mcr, row[4], row[5], row[6]))
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
        resp = mcr.command("gamemodeproperty MatchState")
   #     resp = mcr.command("travel Ministry?Scenario=Scenario_Ministry_Checkpoint_Security")
        #resp = mcr.command("gamemodeproperty ActiveObjectiveId")
        
       
        y = 0
        if(resp != b.Match_state):
            b.Match_state = resp
            b.map = mcr.command("gamemodeproperty MultiplayerScenario")
            reg = re.compile(r"\.Scenario_+\w+")
            b.map = re.search(reg, b.map).group(0).replace("_", " ").replace("Scenario","").replace(".","")
            dogs = ""
            k = b.map.split(" ")
            if b.map.split(" ")[len(k)-1] == "Insurgents":
                    b.dogs = "Ins"
            else:b.dogs = "Sec"
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
            if b.Match_state == 'MatchState = "RoundWon"':
                    y = 1
            else: y = 0
            if b.Match_state == 'MatchState = "NONEee"' or b.security_wins >= b.max_score or b.ins_wins >= b.max_score:
                ins_wins= 0 #Curently how many rounds won INSURGENTS
                security_wins = 0 #sec wins
                map = "NONE" #MAP on server
                lastWin_team = 3
        resp = mcr.command("listplayers") 
        reg = re.compile(r'\d{17}')
        reg = re.findall(reg, resp)
        b.players_count = str(len(reg))
        resp = mcr.command("gamemodeproperty ActiveObjective")
        if resp == 'Could not find property "ActiveObjective"':
            b.obj_name ="Name"
            b.obj_type = "Type"
        else:
            b.obj_type = resp.split("'")[0].split('"')[1]
            b.obj_type = b.obj_type[9:len(b.obj_type)]
            b.obj_name = resp.split("_")
            b.obj_name =  b.obj_name[len(b.obj_name)-1].split("'")[0]
            if 'nCache' in b.obj_type:b.obj_type = "WeaponCache"
        resp = b.mcr.command("gamemodeproperty Mutators") 
        s = resp.split("'")
        mutators = "| "
        for l in s:
            if l[0] != '"'and l[len(l)-1] and l[0]!= '"' and '('!= l[0]:
                mutators += l
        mutators = mutators.replace('Mutators = ','').replace('"', "").replace(")", "").replace("(", "").replace(",", " | ")
        b.mutators = mutators.replace('BP_Mutator_', "").replace("_c", "")
        await Match_state(message, y, curently_tracking)

                    

#############################################################################################################################################
async def Match_state(message, y, curently_tracking):
    global ment2
    global pug_state
    global message_counting
    sec_e = Classes.sec_e
    ins_e = Classes.ins_e
    global Matchess
    numbers = Classes.numbers
    m=[]
    for b in curently_tracking:
        embed = discord.Embed(colour=discord.Colour(0xd0021b))
        if b.lastWin_team == 0:mda = "Bravo" 
        elif b.lastWin_team == 1:mda ="Alpha"
        elif b.lastWin_team == 3:mda = "NONE"
        elif b.lastWin_team == 255:mda = "Draw"
        else: mda = "Error?"
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
        serv_full = b.short_name+" || "+b.full_name
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
        embed.add_field(name="**OLD DOGS**|{1}| --{0}-- |".format(dogs, dogs_team), value="**Players:** `{0}`\n**Match_state:** `{1}`\n**Last Winning Team:** `{2}`\n**Curently on:** `{3} ({4})`\n**Map:** `{5}`".format(b.players_count,match, mda,b.obj_name, b.obj_type, b.map), inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline = True)
        embed.add_field(name="\u200b \u200b \u200b \u200b \u200b \u200b \u200b **BOT TEAM**|{1}| --{0}--  |".format(enemy, enemy_team), value="​​​​​​​ **Mutators**: `{3}`\n**{1}**\n```cs\n{2:^28}```".format(enemy,serv_full, b.ip+":"+str(b.game_port), b.mutators), inline=True)
        resp = b.mcr.command("listplayers") 
        reg = re.compile(r'\d{1,3}\s+\|+.{1,32}\|+\s+\d{17}\s+\|+\s+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+\|+\s+\d+\s+\|')
        reg = re.findall(reg, resp)
        pl = "```| [NR] |                PLAYER NAME              |   SCORE  |\n|------|-----------------------------------------|----------|\n"
        scoreing = 0
        for i in reg:
            wi = ""
            r = i.split("|")
            if len(r) > 6:
                okay = 0
                for pp in r:
                    if okay == 0:
                        rrr = re.compile(r'\d{17}\s')
                        rrr = re.findall(rrr,pp)
                        if len(rrr) < 1 :
                            rrr = re.compile(r'\d{1,3}\s')
                            rrr = re.findall(rrr, pp)
                            if pp != r[0] and len(rrr)<1 and pp !='':
                                wi +="|"+pp 
                        else:okay+=1
            else: 
                wi = r[1]
            scoreing+=1
            rrr = re.compile(r'\d+')
            rrr = re.findall(rrr, r[len(r)-2])[0]
            pl += "| [{0} {1:^40}|{2:^10}|\n".format(str(scoreing)+"]  |", wi.strip(), rrr)
        embed.add_field(name="===========================================================", value="{0}\n|___________________________________________________________|```".format(pl))
        m = embed
        if y == 1 or y == 0:
            if b.pug_state == "":b.pug_state = await message.channel.send(embed=m)
            else: await b.pug_state.edit(embed=m)
    
########################################################################################################
