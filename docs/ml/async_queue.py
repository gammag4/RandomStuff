import asyncio


async def producer(queue: asyncio.Queue):
    """Produces items and puts them in the queue"""
    for i in range(5):
        print(f"Producing item {i}")
        await queue.put(i)
        await asyncio.sleep(0.5)  # Simulate work

    # Signal that producer is done
    await queue.put(None)


async def consumer(queue: asyncio.Queue):
    """Consumes items from the queue"""
    while True:
        item = await queue.get()

        # None signals end of production
        if item is None:
            break

        print(f"Consuming item {item}")
        await asyncio.sleep(0.2)  # Simulate work


async def main():
    queue = asyncio.Queue()

    # Run both concurrently
    await asyncio.gather(
        producer(queue),
        consumer(queue)
    )

    print("Done!")
if __name__ == "__main__":
    asyncio.run(main())
