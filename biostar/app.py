import os

import dash
import dash_mantine_components as dmc
from dotenv import load_dotenv

from biostar.callbacks import attach_callbacks
from biostar.layout import layout

_ = load_dotenv()

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=(os.getenv("MODE") == "production"),
    assets_folder="/websites/biostar/www/static/biostar"
    if os.getenv("MODE") == "production"
    else "static/biostar",
    meta_tags=[
        {"http-equiv": "X-UA-Compatible", "content": "IE=edge"},
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": ""},
        {"name": "author", "content": "JPL.NASA.GOV"},
    ],
    external_stylesheets=[dmc.styles.DATES, dmc.styles.NOTIFICATIONS],
)
app.title = "312C | BioSTAR"
app.layout = dmc.MantineProvider([dmc.NotificationProvider(), layout])

attach_callbacks(app)

if __name__ == "__main__":
    # Debug is opt-in only: the Werkzeug debugger must never be enabled
    # merely because MODE is unset or set to anything other than an
    # explicit development value. Security fix 2026-10-08.
    app.run(debug=(os.getenv("MODE") == "development"))
