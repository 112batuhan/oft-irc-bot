import pydle
import logging
import os
import threading

import refList
import randomMapPicker
import restarter

logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

dyno_timer = restarter.restartingTimer(30*60)

def index_finder(list, search):
    for i,element in enumerate(list):
        if search in element:
            return i


class MyOwnBot(pydle.Client):

    async def on_connect(self):
        logger.info("Succesfully connected.")

        self.active_channel_list = []
        
        dyno_timer.start()

    async def on_private_message(self,target, nick,message):

        logger.info(f"private message from {nick}")

        try:
            if message.startswith('!join'):
                channel = message.split('!join ')[1]

                logger.info(f"Joining {channel}")

                await self.join(channel)
                await self.message(channel, "I'm ready for action! use 'f2 set' command to set a stage!")

        except:
            logger.exception("Error while processing a command!")


    async def on_message(self, target, source, message):

        logger.info(f"{target} - {source}:{message}")

        index = index_finder(self.active_channel_list, target)

        try:
            if message.startswith('!f2') and source in refList.List:  
                dyno_timer.retsart()
                
                if message.startswith("!f2 set"):
                    stage = message.split("!f2 set ")[1]
                    
                    if index != None:
                        del self.active_channel_list[index]

                    try:
                        picker = randomMapPicker.randomPicker(stage)
                        self.active_channel_list.append([target, picker])

                        logger.info(f"{picker.message} to {target}")

                        await self.message(target, picker.message)

                    except ValueError: 
                        await self.message(target, "Wrong stage command! Please check referee sheet for correct commands!")

                   
                elif index != None and message.startswith("!f2 reset"):

                    try:
                        del self.active_channel_list[index]
                        logger.info(f"{target} settings removed")
                
                        await self.message(target, "settings deleted")

                    except:
                        logger.exception("Error while removing a channel from list!")

                else:

                    if index == None:
                        await self.message(target, f"set the stage with '!f2 set' command!")

                    else:
                        
                        try:
                            mod = message.split("!f2 ")[-1]
                            map_id = self.active_channel_list[index][1].randomMapId(mod)
                            await self.message(target, f"!mp map {map_id}")
                        
                        except ValueError:
                            await self.message(target, "invalid mod command!")
            
            
            elif index != None and message.startswith("!mp close"):

                del self.active_channel_list[index]
                logger.info(f"{target} settings removed")



        except:
            logger.exception("Error while processing a command!")



if __name__ == "__main__":
    server = 'irc.ppy.sh'
    port = 6667
    user = os.environ['IRC_USERNAME'] 
    password = os.environ['IRC_PASSWORD'] 
  
    client = MyOwnBot(user, realname=user)
    client.run(server, port, tls=False, tls_verify=False, password = password)