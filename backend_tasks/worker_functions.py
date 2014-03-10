import requests

"""
All Task functions go here, to be executed from the queue and Rq workers
"""

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())