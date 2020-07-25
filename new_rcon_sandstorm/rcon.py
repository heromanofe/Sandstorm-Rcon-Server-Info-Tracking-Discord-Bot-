
import asyncio,discord,Classes,sqlite3, Def_Fun, Config
import valve.source
import valve.source.a2s
import valve.source.master_server
import valve.rcon
from datetime import datetime
import time

#################################################################################################
message_counting = Classes.message_counting
sec_e = Classes.sec_e
ins_e = Classes.ins_e
client = discord.Client()
main_guy = Config.main_guy
stop = 0
admin_role_id = 0
curently_tracking = []
STOP_BOT = 0
server_main = 0
match_state = 0
sleep_for = 0.3
all_servers = asyncio.run(Def_Fun.Initial_setup())
class Admin_Menu:
    def __init__(self, admin_mes, emoji, other_mes, mcr, command,pick_mcr,currently,player):
        self.admin_mes = admin_mes
        self.emoji = emoji
        self.other_mes = other_mes
        self.mcr = mcr
        self.commad = command
        self.currently = currently
        self.pick_mcr = pick_mcr
        self.player = player
Admin_Menus = []
#################################################################################################
@client.event
async def on_ready():
    print('We have logged in as {0.user} | '.format(client)+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"  |")
@client.event
async def on_message(message):
    global a
    global main_guy
    global admin_role_id
    global sec_e
    global ins_e
    global stop
    global server_main
    global Admin_Menus
    global all_servers
    global STOP_BOT
    global match_state
    global sleep_for
    if message.content.startswith('!ssso') and (message.author.id == main_guy or message.guild.owner == message.author):
        s = 0
        while True:
            all_servers[0].mcr.command("gamemodeproperty MultiplayerScenario")
            print("--- Request Nr.: {} ---".format(str(s)))
            s+=1
    if message.content.startswith('!test') and (message.author.id == main_guy or message.guild.owner == message.author):
        SERVER_ADDRESS = ("62.171.147.243", 27131)
        with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as server:
                info = server.info()
                players = server.players()
              #  print("{player_count}/{max_players} {server_name}".format(**info))
                k = []
                for i in info:
                    print(i)
                class player_info:
                    def __init__(self, score, name, duration):
                        self.score = score 
                        self.name = name 
                        self.duration =  duration
                for player in sorted(players["players"],
                                 key=lambda p: p["score"], reverse=True):
                    k.append(player_info("{score}".format(**player),"{name}".format(**player),"{duration}".format(**player)))
                    lol = ""
                    lol = k[len(k)-1].duration.split(".")
                    lol = int(lol[0])%60
                    if lol > 60:
                        min = lol
                        lol = lol%60
                        lol = 'hr'+str(lol)+'min'+str(min-lol*60)
                    else:lol = 'Min'+str(lol)

                    k[len(k)-1].duration = lol

    #if message.content.startswith('!Watch') and (message.author.id == main_guy or message.guild.owner == message.author):
        #watch = OnMyWatch() 
        #watch.run() 
    if message.content.startswith('!stop_bot') and (message.author.id == main_guy or message.guild.owner == message.author):
        if match_state == 0: 
            await message.channel.send("Logging out...")
            await client.logout()
        else: STOP_BOT = 1
    if message.content.startswith('!set_admins') and (message.author.id == main_guy or message.guild.owner == message.author):
        conn = sqlite3.connect("db_server_info.db")
        c = conn.cursor()
        c.execute('update misc set admin_role == ?', [message.role_mentions[0].id])
        conn.commit()
        c.close()
        conn.close()
        admin_role_id = message.role_mentions[0].id
        await message.channel.send("admin role set to <@&{0}>".format(str(admin_role_id)))
    if message.content.startswith('!set_server_main') and (message.author.id == main_guy or message.guild.owner == message.author):
        conn = sqlite3.connect("db_server_info.db")
        c = conn.cursor()
        c.execute('update misc set server_main == ?', [message.role_mentions[0].id])
        conn.commit()
        c.close()
        conn.close()
        server_main = message.role_mentions[0].id
        await message.channel.send("server main role set to <@&{0}>".format(str(server_main)))
    admin_privelege = await admin_or_not(message, "m")
##########################################################################################################################################################################################
    if message.content.startswith('!stop_match_state') and (message.author.id == main_guy or admin_privelege == True or message.guild.owner == message.author):
        stop = 1
    if message.content.startswith('!check_level') and (message.author.id == main_guy or admin_privelege == True or message.guild.owner == message.author):
        for i in all_servers:
            i.check_for_second_level = 1
            i.check_for_first_level = 1
    if message.content.startswith('!start_match_state') and (message.author.id == main_guy or admin_privelege == True or message.guild.owner == message.author):
        global curently_tracking
        match_state = 1
        all_servers = await Def_Fun.Initial_setup()
        stop = 1
        msgs = []
        mmm = await message.guild.fetch_emojis()
        for i in mmm:
            if i.name == "insurgents":
                ins_e = i
                Classes.ins_e = ins_e
            if i.name == "Security":
                sec_e = i
                Classes.sec_e = sec_e
        await asyncio.sleep(12)
        stop = 0
        curently_tracking = all_servers
        sleep_for = 8/len(curently_tracking)
        while True:
            #time.sleep(0.5)
            #await asyncio.sleep(4)
            if STOP_BOT == 1 or stop == 1:
                for b in curently_tracking:
                    if b.pug_state != "": await b.pug_state.delete()
                    b.pug_state = ""
                    match_state = 0
                if STOP_BOT == 1: 
                    await message.channel.send("Logging out...")
                    await client.logout()
                return
            for b in curently_tracking:

                if STOP_BOT == 1 or stop == 1:
                    for b in curently_tracking:
                        if b.pug_state != "": await b.pug_state.delete()
                        b.pug_state = ""
                        match_state = 0
                if STOP_BOT == 1: 
                    await message.channel.send("Logging out...")
                    await client.logout()
                    return
                try:
                    b.error = 0
                    if b.check_for_second_level == 1:
                        #await Def_Fun.players_query(b)
                        await Def_Fun.Match_state(message, b)
                        await asyncio.sleep(0.5)
                    await Def_Fun.rcon_things(message, b, curently_tracking)
                    b.lost = 0
                    b.tries = 0
                    
                except:
                    print("Error in :"+str(b.error)+"    "+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"     On "+b.ip+":"+str(b.server_port))
                    b.tries += 1
                    b.lost = 1
                    await asyncio.sleep(10)
                    b.mcr.disconnect()
                    try:
                        print("Connecting....")
                        b.mcr.connect()
                        print("Connected!!")+"  |  "+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"  |"
                    except:
                        print("Couldn't connect :(" +"  |  "+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"  |")

                if  b.mss =="" and b.tries > 8 and b.lost ==1:
                        b.mss = await message.channel.send("server ( {0} ) is down, can't connect to rcon...<@&{1}> please fix it up dog".format(b.ip+":"+str(b.game_port), str(server_main)))
                        b.Match_state = "FAILED TO CONNECT TO AN RCON, ATTEMPT NR. {0}".format(b.tries)
                if b.lost == 0 and b.mss !="":
                        await b.mss.delete()
                        b.mss = ""
                        b.Match_state = "Server connection fixed, server is UP!"
                        k = await message.channel.send("Fixed server ( {0} )".format(b.ip+":"+str(b.game_port)))
                        await asyncio.sleep(5)
                        await k.delete()
                kkll = 0
                yes = False
               
                for i in await Def_Fun.players_query(b):
                    if str(i.score) == "0": kkll+=1
                if int(kkll) == int(b.players_count): yes = True
                else: yes = False
                if b.timer > ((60*20/5) - 80) and int(b.players_count) > 0 and yes == True:
                    b.check_for_second_level = 1
                
                
                time.sleep(sleep_for)
############################################################################################################################################################################################
    if message.content.startswith('!admin_menu') and (message.author.id == main_guy or admin_privelege == True or message.guild.owner == message.author):
        embed = discord.Embed(colour=discord.Colour(0xd0021b))
        embed.add_field(name="```{0:^64}```".format('Commands'), value="```0.|!say  [TEXT] --> send text as an admin to server\n--|------------------------------------------------\n1.|!kick [Reason] --> Kick player from server\n--|------------------------------------------------\n2.|!ban  [Mins] [Reason] --> ban player from server```")
        m = await message.channel.send(embed = embed)
        Admin_Menus.append(Admin_Menu(m, m, "", "", "admin_menu", 0, all_servers,""))

    if message.content.startswith('!say') and (message.author.id == main_guy or admin_privelege == True or message.guild.owner == message.author):
        m = ""
        count = 0
        emoji = []
        mcr = []
        current_serv = await Def_Fun.Initial_setup()
        for i in current_serv:
            m += "["+Classes.numbers(count)+"]"+" {0}".format(i.ip+":"+str(i.game_port)+"  | --> "+i.full_name+"\n")
            emoji.append(Classes.numbers(count))
            count+=1
            mcr.append(i.mcr)

        g = await message.channel.send("On which server should I say that?:\n"+m)
        Admin_Menus.append(Admin_Menu(message, emoji, g, mcr, "say", 1, '',''))
        for i in emoji:
            await g.add_reaction(i)
############################################################  EMOJIS  ############################################################                   
@client.event
async def on_reaction_add(reaction, user):
    global all_servers
    global Admin_Menus
    message = reaction.message
    admin_privelege = await admin_or_not(user,"")
    global main_guy
    if (('On which server should I say that?:' in reaction.message.content or '' in reaction.message.content) and (user.id == main_guy or admin_privelege == True or message.guild.owner.id == user.id)):
        for i in Admin_Menus:
            if i.other_mes.id == reaction.message.id:
                count=0
                if i.commad == "admin_menu":
                    await menu(i,reaction)
                elif i.pick_mcr == 1:
                    for n in i.emoji:
                        if n == reaction.emoji:
                            i.mcr = i.mcr[count]
                        count+=1
                    i.pick_mcr = 0
                   
                    if i.commad == "say":
                        mes = "[{0}] {1}".format(i.admin_mes.author.name, i.admin_mes.content[4:]).strip()
                        i.mcr.command("say "+mes)
                        await i.other_mes.channel.send("Said: {0}".format(mes))
                        await i.other_mes.delete()
                        Admin_Menus.remove(i)
                        await i.admin_mes.delete()
                        return 
                           # i.mcr = i.mcr[count]
                        
                
########################################
async def admin_or_not(message,m):
    global admin_role_id
    global server_main
    priv = False
    if m == "m":
        if message.author.bot == False:
            for i in message.guild.get_member(message.author.id).roles:
                if i.id == admin_role_id:
                    priv = True
    else:
        if message.bot == False:
            for i in message.guild.get_member(message.id).roles:
                if i.id == admin_role_id:
                    priv = True
    return priv
#########################################
async def set_vars():
    global admin_role_id
    conn = sqlite3.connect("db_server_info.db")
    c = conn.cursor()
    result = c.execute('SELECT admin_role, server_main from misc').fetchone()
    c.close()
    conn.close()
    admin_role_id = result[0]
    server_main = result[1]
asyncio.run(set_vars())
async def menu(i, reaction):
    if reaction.emoji == "1️⃣" and i.commad == "admin_menu": 
        i.command = 'player'
        i.pick_mcr = 1
        embed = discord.Embed(colour=discord.Colour(0xd0021b))
        ll = ""
        co = 0
        for n in i.currently:
            ll += Classes.numbers(co)+n.ip+":"+str(n.game_port)+"\n"
            co +=1
        embed.add_field(name="```{0:^64}```".format('MCR List --> ❌ to go back'), value="```{0}```".format(ll))
        m = await reaction.message.edit(embed = embed)

client.run(Config.token) ##YOUR TOKEN HERE##

