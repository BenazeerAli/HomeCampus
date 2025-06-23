import os

class Config:
    # Basic secret key (used for sessions and security)
    SECRET_KEY = os.environ.get("HOMECAMPUS25") or "HOMECAMPUS25"

    # Database config (update if using something other than SQLite)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Social auth keys (store securely or use Flask-Dance / Authlib)
    FACEBOOK_API_KEY = os.environ.get("FACEBOOK_API_KEY") or "XXXXXXXXXXXXXXX"
    FACEBOOK_APP_SECRET = os.environ.get("FACEBOOK_APP_SECRET") or "XXXXXXXXXXXXXXX"
    
    TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY") or "XXXXXXXXXXXXXXX"
    TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET") or "XXXXXXXXXXXXXXX"

    FRIENDFEED_CONSUMER_KEY = os.environ.get("FRIENDFEED_CONSUMER_KEY") or "XXXXXXXXXXXXXXX"
    FRIENDFEED_CONSUMER_SECRET = os.environ.get("FRIENDFEED_CONSUMER_SECRET") or "XXXXXXXXXXXXXXX"

    # Jinja2 config (Flask handles this internally — no need to redefine unless customizing)
    TEMPLATES_AUTO_RELOAD = True
