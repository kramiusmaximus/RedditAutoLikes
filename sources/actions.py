import logging
import time

from logging import getLogger
log = getLogger(__name__)
log.setLevel(logging.DEBUG)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from setup import set_chrome_params, get_web_driver


def reddit_bot_like_routine(driver, url_posts_to_like, user, password):
    # initiate driver/ start session
    # driver = webdriver.WebDriver(desired_capabilities=smartproxy(hostname, port), options=chrome_options)


    # fingerprint test
    #driver.get("https://gologin.com/check-browser")
    driver.get("https://reddit.com/")

    source = driver.page_source

    if 'service unavailable' in source.lower():
        # reload page
        driver.refresh()

    ## accept cookies

    try:
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='_1tI68pPnLBjR1iHcL7vsee _2iuoyPiKHN3kfOoeIQalDT _10BQ7pjWbeYP63SAPNS8Ts HNozj_dKjQZ59ZsfEegz8 ']"))).click()
    except Exception as e:
        log.info('No cookie window presented.')
        pass


    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                    "button[class='_10K5i7NW6qcm-UoCtpB3aK _1pA8z73SZ1olP5KMKFN4_Z _18X7KoiaLuKbuLqg4zE8BH _22SL37yETIW414yUiZj27w']"))).click()
    except WebDriverException as e:
        log.error(e, exc_info=True)
        raise
    except Exception as e:
        log.error(e, exc_info=True)
        raise

# click login/ logout
    try:
        #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"a[class='_1YWXCINvcuU7nk0ED-bta8']"))).click()

        driver.find_elements(by=By.CSS_SELECTOR, value="a[class='_1YWXCINvcuU7nk0ED-bta8']")[-1].click()
    except WebDriverException as e:
        log.error(e, exc_info=True)
        raise
    except Exception as e:
        log.error(e, exc_info=True)
        raise


    time.sleep(2)
    try:
        frame = driver.find_element(by=By.CSS_SELECTOR, value="iframe[class='_25r3t_lrPF3M6zD2YkWvZU']")
        driver.switch_to.frame(frame)
    except NoSuchElementException as e:
        log.error(e, exc_info=True)
        raise

    time.sleep(0.1)
    try:
        driver.find_element(by=By.ID, value="loginUsername").send_keys(user)
    except NoSuchElementException as e:
        log.error(e, exc_info=True)
        raise

    time.sleep(0.11)
    try:
        driver.find_element(by=By.ID, value="loginPassword").send_keys(password)
    except NoSuchElementException as e:
        log.error(e, exc_info=True)
        raise

    time.sleep(0.1)

    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Log In')]"))).click()
    except Exception as e:
        log.error(e, exc_info=True)
        raise

    time.sleep(0.1)
    try:
        driver.find_element(by=By.CSS_SELECTOR, value="button[aria-label='Close']").click()
    except NoSuchElementException:
        pass
    # do some shit

    for url in url_posts_to_like:
        time.sleep(1)
        driver.get(url)
        time.sleep(4)


        # close annoying popup
        try:
            driver.find_element(by=By.XPATH, value="//button[@aria-label='Close' or @aria-label='Schließen' or @aria-label='Fermer' or @aria-label='Cerca' or @aria-label='Chiudere' or @aria-label='Perto' or @aria-label='Uždaryti' or @aria-label='Tæt']").click()
        except NoSuchElementException:
            pass
        time.sleep(0.1)

        # accept nudity warning
        try:
            driver.find_element(by=By.XPATH, value= "//button[contains(.,'Yes')]").click()
        except NoSuchElementException:
            pass
        time.sleep(2)

        # close annoying popup
        try:
            driver.find_element(by=By.XPATH, value="//button[@aria-label='Close' or @aria-label='Schließen' or @aria-label='Fermer' or @aria-label='Cerca' or @aria-label='Chiudere' or @aria-label='Perto' or @aria-label='Uždaryti' or @aria-label='Tæt']").click()
        except NoSuchElementException:
            pass
        time.sleep(0.1)

        try:
            like_buttons = driver.find_elements(By.XPATH, "//button[contains(@id, 'upvote-button-t3')]")
            like = like_buttons[0]
            val = like.get_attribute('aria-pressed')
            if val == 'false':
                like.click()
        except WebDriverException as e:
            raise e

        time.sleep(2)

    driver.quit()

def perform_reddit_likes(url_posts_to_like, account_names, accounts, proxies):
    t1 = time.time()
    likes = 0

    for i, user in enumerate(account_names):
        password = accounts[user]['password']

        # set chrome params
        proxy = proxies[i % len(proxies)]

        chrome_options = set_chrome_params(proxy)

        # driver = uc.Chrome()
        driver = get_web_driver(chrome_options)

        err = False
        try:
            reddit_bot_like_routine(driver, url_posts_to_like, user, password)
            likes += 1

        except Exception as e:
            err = True
            log.error(e, exc_info=True)
        finally:
            t2 = time.time()
            driver.quit()
            log.info(f'like{likes}@{t2 - t1}: Bot {user} like was { "success" if not err else "fail" }')
