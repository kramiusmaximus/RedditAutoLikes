import sys

from actions import perform_reddit_likes
from setup import *
import logging
import threading


def get_batch(t_index, n_threads, account_names):
    batch_size = int(len(account_names) / n_threads)

    if batch_size < 1:
        raise Exception(
            f"You have inputed more threads than there are items. There are {len(account_names)} items, and you inputed {n_threads} threads. The maximum amount of threads you can input is {len(account_names)}")

    a = t_index * batch_size
    b = (t_index + 1) * batch_size if t_index < n_threads - 1 else a + len(account_names) - t_index * batch_size

    batch = account_names[a:b]

    return batch


def main():

    VARS = {
        "NLIKES": 6,
        "NTHREADS": 3,
    }

    url_posts_to_like = [
        'https://www.reddit.com/r/triathlon/comments/z8aota/cheapest_1406sironmans_in_the_us/'
    ]

    # load existing accounts
    account_names, accounts = init_accounts('./data/accounts.obj', './docs/accounts.txt')
    account_names = account_names[:min(VARS['NLIKES'], len(account_names))]

    # load proxies
    proxies = init_proxies('./docs/proxies.txt')

    # start multithreaded liking operation
    threads = []
    for i in range(VARS['NTHREADS']):

        batch = get_batch(i, VARS['NTHREADS'], account_names)
        x = threading.Thread(target=perform_reddit_likes,
                             args=(url_posts_to_like, batch, accounts, proxies))
        logging.info(f"Thread {i} started")
        threads.append(x)
        x.start()

    for i, thread in enumerate(threads):
        thread.join()
        logging.info(f"Thread {i} finished")

    logging.info("Liking sequence complete!")



if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    main()





