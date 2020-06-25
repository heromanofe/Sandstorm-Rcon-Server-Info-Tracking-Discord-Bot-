# Sandstorm-Rcon-Server-Info-Tracking-Discord-Bot-
Discord Bot that tracks stuff using Rcon and stuff

1. to change database and add IP\Password and port use sum sqlite3 db changer, for example I used https://sqlitebrowser.org/
Open db_server_info.db in sqlbrowser and go to `browse data` tab there change from `MISC` to `Server_list` --> `IP`: write there IP of server
`R_port`--> rcon port of that server
`Password`--> Password of rcon
`G_Port` --> Game port (port that people use to connect to your server)
`Short_name` --> for example, if servers are from (for example) DGL I can write DGL and it will be used before full name to ..idk :D
`Full_name`--> 2nd part of name
`max_score` ---> how many wins till server switches map. (might be replaced with auto)
after you done, press ctr+s or click on `Write Changes` (top pannel)
2.then you can open new_rcon_sandstorm and change main_guy at top to your discord_user_id (not important if you are owner of discord channel or admin of server could set admin role for ya)
3.!esetup --> important command before tracking!! used for searching for insurgents and Security emojis.  please add to your server 2 emojis (use same case) one: insurgents and second one Security
4. to set admin role--> !set_server_main @role    <----- can be done by server_owner or main_guy
5.!set_server_main @role --> used for setting role that will be @ if one of servers can't be connected to (for example, if server is down)
6.!stop_match_state --> to stop tracking. --> can be done by server admin, admin role or main_guy
7.!start_match_state --> start tracking servers. picks up info from database   --> can be done by server admin, admin role or main_guy
