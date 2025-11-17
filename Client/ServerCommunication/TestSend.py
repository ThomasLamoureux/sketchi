import asyncio


import Client as Client







async def main():
    # Start background_task *without waiting for it*
    asyncio.create_task(Client.init("127.0.0.1", 6700))

    # Main code continues immediately
    for i in range(5):
        print("Main code:", i)
        await asyncio.sleep(0.5)

    print("Stress test")
    for i in range(1555):
        asyncio.create_task(Client.send_message("client_msg", {"text": "Hello from test script!" + str(i)}))


if __name__ == "__main__":
    asyncio.run(main())