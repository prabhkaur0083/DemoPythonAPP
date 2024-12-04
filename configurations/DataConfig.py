from dotenv import load_dotenv
import os

load_dotenv()


class BaseConfig(object):
    AUTHENTICATION_MODE = "ServicePrincipal"

    TENANT_ID = os.getenv("TENANT_ID")

    CLIENT_ID = os.getenv("CLIENT_ID")

    CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    SCOPE_BASE = ["https://analysis.windows.net/powerbi/api/.default"]

    AUTHORITY_URL = "https://login.microsoftonline.com/organizations"
