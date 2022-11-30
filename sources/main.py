import sys

from actions import perform_reddit_likes
from setup import *
import logging
import threading


VARS = {
    "NLIKES" : 20,
    "NTHREADS": 1,
}

url_posts_to_like = [
    'https://www.reddit.com/r/ApplyingToCollege/comments/v1elul/rising_sophmore_summer_advice/'
]





if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout,level=logging.WARNING)

    # load existing accounts
    account_names, accounts = init_accounts('./data/accounts.obj', './docs/accounts.txt')
    account_names = account_names[:max(VARS['NLIKES'], len(account_names))]

    # load proxies
    proxies = init_proxies('./docs/proxies.txt')

    # start multithreaded liking operation
    threads = []
    for i in range(VARS['NTHREADS']):
        thread_acc_n = int(len(account_names) / VARS['NTHREADS'])
        a, b = i * thread_acc_n, (i + 1) * thread_acc_n - 1
        thread_account_names = account_names[a:b]
        x = threading.Thread(target=perform_reddit_likes, args=(url_posts_to_like, thread_account_names, accounts, proxies))
        logging.info("Main    : thread %d started", i)
        threads.append(x)
        x.start()

    for i, thread in enumerate(threads):
        thread.join()
        logging.info("Main    : thread %d done", i)




