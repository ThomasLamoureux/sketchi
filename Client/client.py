
import FrontEnd.gui as gui
import asyncio
import threading
import ServerCommunication.Main_Client as Main_Client

    


def loop():
    loop = asyncio.new_event_loop()
    gui.loop = loop
    asyncio.set_event_loop(loop)
    asyncio.run(Main_Client.loop())
    loop.run_forever()






threading.Thread(target=loop, daemon=True).start()

gui.run()