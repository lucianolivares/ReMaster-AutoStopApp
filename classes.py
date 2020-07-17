from kivymd.uix.list import OneLineIconListItem, IconLeftWidget

class ListIcon(OneLineIconListItem):
    def __init__(self, **kw):
        super().__init__()
        self.text = kw["text"]
        self.icon = IconLeftWidget(icon=kw["icon"])
        self.add_widget(self.icon)
        self.on_release = kw["on_release"]