from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

import requests


class EverdoExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        argument = event.get_argument()
        items = []
        name = "Inbox"
        description = "Add '{}' to Inbox?".format(argument)
        data = {"action": "add", "value": argument}
        items.append(
            ExtensionResultItem(
                icon="",
                name=name,
                description=description,
                on_enter=ExtensionCustomAction(data, keep_app_open=False),
            )
        )
        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        token = extension.preferences["token"]
        everdo_url = extension.preferences["url"]
        data = event.get_data()
        request_body = {
            "title": data["value"],
        }
        url = f"{everdo_url}/api/items?key={token}"
        requests.post(
            url,
            json=request_body,
            headers={"Content-Type": "application/json"},
            verify=False,
        )
        return None


if __name__ == "__main__":
    EverdoExtension().run()
