import os

from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

load_dotenv()

API_KEY = os.environ["API_KEY"]

api_key_header = APIKeyHeader(
    name="Authorization", description="Authorization key", auto_error=True
)


def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=403,
            detail="Not authorized. Please provide an authorization key.",
        )


def get_driver():
    from selenium.webdriver import ChromeOptions, Remote

    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("log-level=2")

    # import sys

    # if sys.platform.startswith("linux"):
    #     chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument(
        "--disable-dev-shm-usage"
    )  # https://source.chromium.org/chromium/chromium/src/+/main:/base/base_switches.cc
    chrome_options.add_argument("--no-sandbox")

    # CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH")
    # driver = Chrome(
    #     executable_path=r"{}".format(CHROMEDRIVER_PATH),
    #     chrome_options=chrome_options,
    # )
    driver = Remote(
        command_executor=os.environ["REMOTE_WEBDRIVER"], options=chrome_options
    )

    return driver


# docker run -d -p 4444:4444 -p 7900:7900 --shm-size="512m" selenium/standalone-chrome:latest
