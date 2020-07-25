import Classes, mcrcon_new, valve.rcon
token  = '' #here ur token
main_guy = 0
new_serv= []
#new_serv.append(Classes.Server_match(ip, server_port(rcon port),password, game, mcr, short_name, full_name,max_score(score for bots to win game), query_port)) --> for every new server, example:
new_serv.append(Classes.Server_match("127.0.0.1", 27011,"Password", 27018, mcr, "No need, forgot to delete this:D", "No need, forgot to delete this:D",0, 22017))
mcr =""

def all_ser():
    global new_serv
    all_servers = []
    for i in new_serv:
        try:
            mcr = mcrcon_new.MCRcon(i.ip, i.password,i.server_port)
            ok = Classes.Server_match(i.ip, i.server_port, i.password, i.game_port,mcr,i.short_name, i.full_name, i.max_score, i.query)
            mcr.connect()
            
            all_servers.append(Classes.Server_match(i.ip, i.server_port, i.password, i.game_port,mcr,i.short_name, i.full_name, i.max_score, i.query))
        except: 
                if len(all_servers) > 0:
                    all_servers.remove(all_servers[len(all_servers)-1])
                print("ERROR, DIDN'T CONNECTED TO RCON, server IP: {0}:{1}".format(ok.ip, ok.game_port))
    return all_servers
