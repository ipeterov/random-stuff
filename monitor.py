import asyncio
import aiohttp
import matplotlib.pyplot as plt

PROBING_INTERVAL_SECONDS = 1
TOTAL_PROBES = 60

data = []


async def on_request_start(session, trace_config_ctx, params):
    trace_config_ctx.start = asyncio.get_event_loop().time()


async def on_request_end(session, trace_config_ctx, params):
    elapsed = asyncio.get_event_loop().time() - trace_config_ctx.start
    if params.response.status != 200 or await params.response.text() != "I'm alive":
        elapsed = 0

    print(".")

    data.append((trace_config_ctx.start, elapsed))

    # print(await params.response.text())
    # print("Request took {}".format(elapsed))


trace_config = aiohttp.TraceConfig()
trace_config.on_request_start.append(on_request_start)
trace_config.on_request_end.append(on_request_end)


async def probe(sleep=0):
    async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
        await asyncio.sleep(sleep)
        try:
            await session.get("https://lab.polymed.online/health/")
        except:
            pass


async def main():
    async with asyncio.TaskGroup() as tg:
        for offset in range(TOTAL_PROBES):
            tg.create_task(probe(offset * PROBING_INTERVAL_SECONDS))


asyncio.run(main())

data.sort()
times, values = zip(*data)

plt.plot(times, values)
plt.show()
