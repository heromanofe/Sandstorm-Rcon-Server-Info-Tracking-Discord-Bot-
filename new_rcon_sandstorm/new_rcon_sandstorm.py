
import asyncio,discord,Classes,sqlite3, Def_Fun
#################################################################################################
message_counting = Classes.message_counting
sec_e = Classes.sec_e
ins_e = Classes.ins_e
client = discord.Client()
main_guy = 0000000000000000000
stop = 0
admin_role_id = 0
curently_tracking = []
server_main = 0
#################################################################################################
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
@client.event
async def on_message(message):
    global a
    global main_guy
    global admin_role_id
    global sec_e
    global ins_e
    global stop
    global server_main
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
    admin_privelege = await admin_or_not(message)
    if message.content.startswith('!stop_match_state') and (message.author.id == main_guy or admin_privelege == True or message.guild.owner == message.author):
        stop = 1
    if message.content.startswith('!esetup') and (message.author.id == main_guy or admin_privelege == True or message.guild.owner == message.author):
        mmm = await message.guild.fetch_emojis()
        for i in mmm:
            if i.name == "insurgents":
                ins_e = i
                Classes.ins_e = ins_e
            if i.name == "Security":
                sec_e = i
                Classes.sec_e = sec_e
    if message.content.startswith('!start_match_state') and (message.author.id == main_guy or admin_privelege == True or message.guild.owner == message.author):
        global curently_tracking
        all_servers = await Def_Fun.Initial_setup()
        stop = 1
        msgs = []
        await asyncio.sleep(3)
        stop = 0
        curently_tracking = all_servers
        while stop != 1:
            await asyncio.sleep(3)
            for b in curently_tracking:
                try:
                    await Def_Fun.rcon_things(message, b, curently_tracking)
                    b.lost = 0
                except:
                  # curently_tracking.remove(b)
                    b.lost = 1
                    if  b.pug_state !="":
                       await b.pug_state.delete()
                if b.lost == 1 and b.mss !="":
                    b.mss = message.channel.send("server ( {0} ) is down, can't connect to rcon...<@&{1}> please".b.ip+b.game_port, str(server_main))
                elif b.lost == 0 and b.mss !="":
                    await b.mss.delete()
                    await message.channel.send("Fixed server ( {0} )".format(b.ip+b.game_port))
                
                    
                   
########################################
async def admin_or_not(message):
    global admin_role_id
    global server_main
    priv = False
    for i in message.author.roles:
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
client.run('') ##YOUR TOKEN HERE##

