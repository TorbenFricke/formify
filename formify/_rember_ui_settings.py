import json, typing, os


class UISaveLoad:
    def __init__(self, get_ui_settings: callable, app_name: str):
        from formify._save_load_helpers import Timer
        self._filename = self.set_app_name(app_name)
        self.timer = Timer(interval=20, target=self.save_if_changed)
        self.last_json = None
        self.get_ui_settings = get_ui_settings

    def set_app_name(self, app_name):
        from formify._save_load_helpers import ensure_appdata_dir
        self._filename = ensure_appdata_dir(app_name) / "ui_settings.json"
        # ensure we save (because the file name might have changed )
        self.last_json = None
        return self._filename

    def save_if_changed(self):
        if self._filename is None:
            return

        new_json = json.dumps(self.get_ui_settings())
        changed = self.last_json is None or self.last_json != new_json

        self.last_json = new_json

        if changed:
            with open(self._filename, "w+") as f:
                f.write(new_json)

    def load(self) -> typing.Optional[dict]:
        if not os.path.isfile(self._filename):
            return None

        with open(self._filename, "r") as f:
            s = f.read()

        return json.loads(s)
