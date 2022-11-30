from selenium.common.exceptions import *
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
import time
import pickle as p









VARS = {
    "NLIKES" : 20,
    "NTHREADS": 4,
}

url_posts_to_like = [
    'https://www.reddit.com/r/triathlon/comments/yy9j6c/ideal_racing_weight/'
]


def smartproxy(hostname, port):
    prox = Proxy()

    prox.proxy_type = ProxyType.MANUAL

    prox.http_proxy = '{hostname}:{port}'.format(hostname = hostname, port = port)
    prox.ssl_proxy = '{hostname}:{port}'.format(hostname = hostname, port = port)

    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    return capabilities


def init_accounts(path_to_existing_accounts, path_to_new_accounts = None) -> []:
    accounts = {}

    # read existing accounts file
    try:
        fd = open("accounts.obj", 'rb')
        accounts = p.load(fd)
        fd.close()
    except OSError:
        print("obj doesnt exist")
    except Exception:
        print("other error")

    # add new accounts
    try:
        with open('./docs/accounts.txt') as f:
            for line in f:
                args = line.strip("\n").split(':')
                if len(args) > 2:
                    continue
                if args[0] not in accounts:
                    accounts[args[0]] = {'password':args[1]}
    except Exception as e:
        print("exception encountered whilst opening new accounts file")
    return accounts


def init_proxies(path_to_proxies) -> []:
    proxies = []
    try:
        with open(path_to_proxies) as f:
            for line in f:
                proxies.append(line.strip('\n'))
                return proxies
    except Exception:
        print("Unknown error occurred")

def set_chrome_params():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("user-data-dir=./profile/")
    return chrome_options

def bot_like_routine(user, password, hostname, port, chrome_options):
    # initiate driver/ start session
    driver = webdriver.WebDriver(desired_capabilities=smartproxy(hostname, port), options=chrome_options)

    # clear cookies
    send_command = ('POST', '/session/$sessionId/chromium/send_command')
    driver.command_executor._commands['SEND_COMMAND'] = send_command
    driver.execute('SEND_COMMAND', dict(cmd='Network.clearBrowserCookies', params={}))

    ## Logging in

    driver.get("https://reddit.com")


    ## accept cookies

    try:
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='_1tI68pPnLBjR1iHcL7vsee _2iuoyPiKHN3kfOoeIQalDT _10BQ7pjWbeYP63SAPNS8Ts HNozj_dKjQZ59ZsfEegz8 ']"))).click()
    except Exception as e:
        pass


    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                    "a[class='Z_HUY3BUsGOBOtdmH94ZS _3Wg53T10KuuPmyWOMWsY2F _2iuoyPiKHN3kfOoeIQalDT _10BQ7pjWbeYP63SAPNS8Ts HNozj_dKjQZ59ZsfEegz8 _2nelDm85zKKmuD94NequP0']"))).click()
    except WebDriverException as e:
        print(f'Exception: {e}')
        raise
    except Exception as e:
        print(f'Exception: {e}')
        raise

    time.sleep(3)
    try:
        frame = driver.find_element(by=By.CSS_SELECTOR, value="iframe[class='_25r3t_lrPF3M6zD2YkWvZU']")
        driver.switch_to.frame(frame)
    except NoSuchElementException as e:
        print(f'Exception: {e}')
        raise

    time.sleep(0.1)
    try:
        driver.find_element(by=By.ID, value="loginUsername").send_keys(user)
    except NoSuchElementException as e:
        print(f'Exception: {e}')
        raise

    time.sleep(0.11)
    try:
        driver.find_element(by=By.ID, value="loginPassword").send_keys(password)
    except NoSuchElementException as e:
        print(f'Exception: {e}')
        raise

    time.sleep(0.1)

    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Log In')]"))).click()
        # driver.find_element(by=By.XPATH, value="//button[contains(.,'Log In')]").click()
    except Exception as e:
        print(f'Exception: {e}')
        raise

    time.sleep(0.1)
    try:
        driver.find_element(by=By.CSS_SELECTOR, value="button[aria-label='Close']").click()
    except NoSuchElementException:
        pass
    # do some shit

    for url in url_posts_to_like:
        time.sleep(2)
        driver.get(url)
        time.sleep(10)

        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                        "//button[contains(@id, 'upvote-button-t3')]"))).click()
            print('clicked element')
        except WebDriverException as e:
            raise

        time.sleep(2)

    # # logout
    #
    # time.sleep(0.1)
    # try:
    #     driver.find_element(by=By.CSS_SELECTOR, value="button[id='USER_DROPDOWN_ID']").click()
    # except Exception:
    #     print(Exception)
    #
    # time.sleep(0.1)
    # try:
    #     driver.find_elements(by=By.CSS_SELECTOR, value="button[class='_3fbofimxVp_hpVM6I1TGMS GCltVwsXPu5lE-gs4Nucu']")[-1].click()
    # except Exception:
    #     print(Exception)

    driver.quit()


def start_liking(accounts, proxies, chrome_options, n):
    t1 = time.time()
    likes = 0

    for i, (key, val) in enumerate(accounts.items()):
        # if i >= n:
        #     break

        if i < 40:
            continue
        user = key
        password = val['password']

        proxy = proxies[i % len(proxies)]
        l = proxy.split(':')
        HOSTNAME = l[0] + ':' + l[1]
        PORT = l[2]


        try:
            err = False
            bot_like_routine(user, password, HOSTNAME, PORT, chrome_options)
            likes += 1

        except Exception as e:
            err = True
            print(f'Unknown Exception occured: {e}')
        finally:
            t2 = time.time()
            print(f'like{likes}@{t2 - t1}: Bot {user} like was { "success" if not err else "fail" }')


        print(f'')





if __name__ == '__main__':

    # load existing accounts
    accounts = init_accounts('./data/accounts.obj', './data/accounts.txt')

    # load proxies
    proxies = init_proxies('./docs/proxies.txt')

    # set chrome options
    chrome_options = set_chrome_params()

    # start
    n = min(len(accounts), VARS['NLIKES'])
    start_liking(accounts, proxies, chrome_options, n)




