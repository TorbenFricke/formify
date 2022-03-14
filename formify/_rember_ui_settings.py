import json, typing, os


class UISaveLoad:
    def __init__(self, get_ui_settings: callable, app_name: str, filename: str = None):
        from formify._save_load_helpers import Timer, ensure_appdata_dir

        if filename is None:
            filename = ensure_appdata_dir(app_name) / "ui_settings.json"
        self.filename = filename
        self.timer = Timer(interval=20, target=self.save_if_changed)
        self.last_json = None
        self.get_ui_settings = get_ui_settings

    def save_if_changed(self):
        new_json = json.dumps(
            self.get_ui_settings()
        )
        if self.last_json is None:
            changed = True
        elif self.last_json != new_json:
            changed = True
        else:
            changed = False

        self.last_json = new_json

        if changed:
            with open(self.filename, "w+") as f:
                f.write(new_json)

    def load(self) -> typing.Optional[dict]:
        if not os.path.isfile(self.filename):
            return None

        with open(self.filename, "r") as f:
            s = f.read()

        return json.loads(s)
