# Sandstorm-Rcon-Server-Info-Tracking-Discord-Bot-
Discord Bot that tracks stuff using Rcon and query (in the future I will use rcon more, but for now.. well, it is safe version for sure :D )

1.you need to open Config.py file and add your discord bot token there also you could (if you don't want to do DB stuff) add your server variables there. please note that you need to delete # and to add more servers just copy append.... message and paste it to the next line. also half of the stuff there is automized and will be deleted like server name and mutators. to change database and add IP\Password and port use sum sqlite3 db changer, for example I used https://sqlitebrowser.org/ 
Open db_server_info.db in sqlbrowser and go to `browse data` tab there change from `MISC` to `Server_list` --> `IP`: write there IP of server
`R_port`--> rcon port of that server
`Password`--> Password of rcon
`G_Port` --> Game port (port that people use to connect to your server)
`Short_name` --> for example, if servers are from (for example) DGL I can write DGL and it will be used before full name to ..idk :D
`Full_name`--> 2nd part of name
`max_score` ---> how many wins till server switches map. (might be replaced with auto)
`query` --> query port

after you done, press ctr+s or click on `Write Changes` (top pannel)
2.!!!!!! `please add to your server 2 emojis (use same case) one: insurgents and second one Security` !!!!!
4. to set admin role--> !set_server_main @role    <----- can be done by server_owner or main_guy
5.!set_server_main @role --> used for setting role that will be @ if one of servers can't be connected to (for example, if server is down)
6.!stop_match_state --> to stop tracking. --> can be done by server admin, admin role or main_guy
7.!start_match_state --> start tracking servers. picks up info from database   --> can be done by server admin, admin role or main_guy
EXTRA THIC --> you can try to do !say message and with emoji choose server. people there might see ur message ;)
--> you can ask me questions here: <---- https://discord.gg/ueu4J57
8. to run script: in cmd:      |           in therminal
cd path\to\bot                 |    cd path\to\bot  
py new_rcon_sandstorm.py       |    py3 new_rcon_sandstorm.py
