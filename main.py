from selenium.common.exceptions import *
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from webdriver_manager.chrome import ChromeDriverManager
#from seleniumwire import webdriver
from time import sleep
import logging

url_posts_to_like = [
    'https://www.reddit.com/r/Askpolitics/comments/ypazbp/can_a_state_leave_the_union_to_not_pay_taxes/'
]


def smartproxy(hostname, port):
    prox = Proxy()

    prox.proxy_type = ProxyType.MANUAL

    prox.http_proxy = '{hostname}:{port}'.format(hostname = hostname, port = port)
    prox.ssl_proxy = '{hostname}:{port}'.format(hostname = hostname, port = port)

    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    return capabilities

if __name__ == '__main__':
    accounts = []

    # load existing accounts
    with open('./docs/accounts.txt') as f:
        for line in f:
            args = line.split(':')
            if len(args) > 2:
                continue
            accounts.append({'user':args[0], 'password':args[1]})



    # add new accounts

    # load proxies

    proxies = []
    with open('./docs/proxies.txt') as f:
        for line in f:
            proxies.append(line.strip('\n'))


    for p, acc in zip(proxies[:10], accounts[:10]):
        l = p.split(':')
        HOSTNAME = l[0] + ':' + l[1]
        PORT = l[2]

        driver = webdriver.WebDriver(desired_capabilities=smartproxy(HOSTNAME, PORT))

        # Logging in

        # sign in button
        driver.get("https://reddit.com")
        sleep(10)
        driver.find_element(by=By.CSS_SELECTOR, value=".\_3x3dhQasGAuYcXVQ02QUzy").click()

        sleep(1)
        driver.find_element(by=By.LINK_TEXT, value="Log In / Sign Up").click()

        sleep(1)
        frame = driver.find_element(by=By.CSS_SELECTOR, value="iframe[class='_25r3t_lrPF3M6zD2YkWvZU']")
        driver.switch_to.frame(frame)

        sleep(1)
        driver.find_element(by=By.ID, value="loginUsername").send_keys("airborne454")

        sleep(1)
        driver.find_element(by=By.ID, value="loginPassword").send_keys("Samurai!((*")

        sleep(3)
        driver.find_element(by=By.XPATH, value="//button[contains(.,'Log In')]").click()

        # do some shit

        for url in url_posts_to_like:
            sleep(2)
            driver.get(url)

            sleep(13)
            try:
                driver.find_element(by=By.CSS_SELECTOR, value="button[aria-label='Close']").click()
            except NoSuchElementException:
                print(NoSuchElementException)

            sleep(1)
            try:
             driver.find_element(by=By.XPATH, value="//button[contains(@id, 'upvote-button-t3')]").click()
            except NoSuchElementException:
                print(NoSuchElementException)

        # logout

        sleep(1)
        try:
            driver.find_element(by=By.CSS_SELECTOR, value="button[aria-label='Close']").click()
        except NoSuchElementException:
            print(NoSuchElementException)


        sleep(1)
        try:
            driver.find_element(by=By.CSS_SELECTOR, value="button[id='USER_DROPDOWN_ID']").click()
        except Exception:
            print(Exception)

        sleep(2)
        try:
            driver.find_elements(by=By.CSS_SELECTOR, value="button[class='_3fbofimxVp_hpVM6I1TGMS GCltVwsXPu5lE-gs4Nucu']")[-1].click()
        except Exception:
            print(Exception)

        sleep(5)

        print(driver.get_cookies())
        driver.delete_all_cookies()
        driver.close()

