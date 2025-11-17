import Client.ServerCommunication.Client as Client
import asyncio
import threading




thread = threading.Thread(target=Client.main, daemon=True)


thread.start()


while True:
    input_text = input("Enter something (type 'exit' to quit): ")
    if input_text.lower() == 'exit':
        break
    else:
        asyncio.run(Client.write_message("", {"type": "client_msg", "client_id": Client.CLIENT_ID, "payload": {"text": input_text}}))