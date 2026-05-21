import asyncio
from kasa import Discover, Credentials

async def main():
    creds = Credentials("penguinlovebts@gmail.com","fatbird003")
    dev = await Discover.discover_single(
        "192.168.1.49",
        credentials=creds
    )
    await dev.update()
    print(dev)

asyncio.run(main())
EOF
