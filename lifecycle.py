import iterm2
import asyncio


async def main(connection):
    app = await iterm2.async_get_app(connection)
    window = app.current_window

    tasks = [
        focus_monitor(connection),
        new_session_monitor(connection),
        end_session_monitor(connection),
        layout_change(connection),
    ]

    [asyncio.create_task(task) for task in tasks]


async def focus_monitor(connection: iterm2.connection.Connection):
    async with iterm2.FocusMonitor(connection) as monitor:
        while True:
            update = await monitor.async_get_next_update()
            if update.selected_tab_changed:
                print("The active tab is now {}".format(update.selected_tab_changed.tab_id))

async def new_session_monitor(connection: iterm2.connection.Connection):
    async with iterm2.NewSessionMonitor(connection) as mon:
        while True:
            session_id = await mon.async_get()
            print("Session ID {} created".format(session_id))

async def end_session_monitor(connection: iterm2.connection.Connection):
    async with iterm2.SessionTerminationMonitor(connection) as mon:
        while True:
            session_id = await mon.async_get()
            print("Session {} closed".format(session_id))


async def layout_change(connection: iterm2.connection.Connection):
    async with iterm2.LayoutChangeMonitor(connection) as mon:
        while True:
            await mon.async_get()
            print("layout changed")


if __name__ == '__main__':
    iterm2.run_forever(main)