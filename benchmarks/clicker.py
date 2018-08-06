#!/usr/bin/python
import requests, json, threading, random
from multiprocessing import Pool

def answer(n):
    url = 'https://1y4o8v9snh.execute-api.us-east-2.amazonaws.com/default/cs301'

    data = {"fn":"get_question"}
    r = requests.post(url, data=json.dumps(data))
    question_id = r.json()['body']['id']

    data = {"fn":"answer","question_id":question_id,"answer":random.choice(["A", "B", "C", "D"])}
    r = requests.post(url, data=json.dumps(data))
    print(r.json())

def main():
    N = 150

    with Pool(N) as p:
        p.map(answer, range(N))

if __name__ == '__main__':
    main()
