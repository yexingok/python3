#!/usr/bin/env python

import requests, re, time
from bs4 import BeautifulSoup


def collect_comments(bookId, wantNum):
    '''
    Collect num of comments from Douban's bookId

    Parameters:
        bookId:  (int) The bookId
        wantNum: (int) How many comments you want
    Return dict:
        score:   (int) Average rating score.
        comments:[list] A list inclues all comments.
    '''

    haveNum, pageNum = 0, 1
    result = {}
    sum, scoreNum = 0, 0
    comments = []
    while(haveNum < wantNum):
        bookurl = 'https://book.douban.com/subject/' + str(bookId) + \
                  '/comments/hot?p=' + str(pageNum)
        print('Fetching page {} with url {}'.format(pageNum, bookurl))
        try:
            r = requests.get(bookurl)
        except Exception as err:
            print(err)
            break
        soup = BeautifulSoup(r.text, 'lxml')
        texts = soup.find_all('span', class_="short")
        for text in texts:
            comments.append(text.string)
            haveNum += 1
            if haveNum == wantNum:
                break
        pattern = re.compile('<span class="user-stars allstar(.*?) rating"')
        scores = re.findall(pattern, r.text)
        for num in scores:
            sum += int(num)
            scoreNum += 1
        pageNum += 1
        time.sleep(5)
    result['score'] = sum / scoreNum
    result['comments'] = comments
    return result

if __name__ == '__main__':
    #bookId = input('Input Book ID?')
    result = collect_comments(4843462, 50)
    num = 0
    for text in result['comments']:
        num += 1
        print('{}\t{}'.format(num, text))
    print("")
    print('Score: {}'.format(result['score']))
