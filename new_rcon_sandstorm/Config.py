import Classes, mcrcon_new
token  = 'DISCORD TOKEN HERE' #here ur token
main_guy = 0 #NOT IMPORTANT, BUT IF YA ADD DISCORD ID OF A GUY HERE, HE COULD DO ADMIN STUFF WITH BOT
new_serv= []
#new_serv.append(Classes.Server_match(ip, server_port(rcon port),password, game, mcr, short_name, full_name,max_score(score for bots to win game), query_port)) --> for every new server, example:
mcr =""
#new_serv.append(Classes.Server_match("192.168.0.101", 27888,"MyRconPassword1337", 27016, mcr, "My servers", "number #2",5, 27000))




#####################################################################################################################################################
def all_ser():
    global new_serv
    all_servers = []
    for i in new_serv:
        try:
            mcr = mcrcon_new.MCRcon(i.ip, i.password,i.server_port)
            mcr.connect()
        
            all_servers.append(Classes.Server_match(i.ip, i.server_port, i.password, i.game_port,mcr,i.short_name, i.full_name, i.max_score, i.query))
        except: 
                if len(all_servers) > 0:
                    all_servers.remove(all_servers[len(all_servers)-1])
                print("ERROR, DIDN'T CONNECTED TO RCON")
    return all_servers