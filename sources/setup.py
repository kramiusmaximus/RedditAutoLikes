import logging

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import webdriver
from fake_useragent import UserAgent

from logging import getLogger
log = getLogger(__name__)
log.setLevel(logging.DEBUG)

def init_accounts(path_to_existing_accounts, path_to_new_accounts = None) -> []:
    accounts = {}
    account_names = []

    try:
        with open(path_to_new_accounts) as f:
            for line in f:
                args = line.strip("\n").split(':')
                if len(args) > 2:
                    continue
                if args[0] not in accounts:
                    accounts[args[0]] = {'password':args[1]}
                    account_names.append(args[0])
    except Exception as e:
        print("exception encountered whilst opening new accounts file")
    return account_names, accounts


def init_proxies(path_to_proxies) -> []:
    proxies = []
    try:
        with open(path_to_proxies) as f:
            for line in f:
                proxies.append(line.strip('\n'))
        return proxies
    except Exception:
        print("Unknown error occurred")

def set_chrome_params(proxy=None):

    # standard chrome options

    options = Options()
    if proxy:
        options.add_argument('--proxy-server=%s' % proxy)
    ua = UserAgent()['google chrome']
    options.add_argument(f'user-agent={ua}')
    options.add_argument("user-data-dir=./profile")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-extensions")
    prefs = {"profile.managed_default_content_settings.images": 2,
             "profile.managed_default_content_settings.media_stream":2}
    options.add_experimental_option("prefs", prefs)

    return options


def get_web_driver(options):
    driver = webdriver.WebDriver(options=options)

    # clear cookies
    send_command = ('POST', '/session/$sessionId/chromium/send_command')
    driver.command_executor._commands['SEND_COMMAND'] = send_command
    driver.execute('SEND_COMMAND', dict(cmd='Network.clearBrowserCookies', params={}))

    return driver