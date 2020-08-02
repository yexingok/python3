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
    sleepTime = 5
    # Add User-Agent otherwise douban will not return right HTML:
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    haveNum, pageNum = 0, 1
    result = {}
    sum, scoreNum = 0, 0
    comments = []
    while(haveNum < wantNum):
        bookurl = 'https://book.douban.com/subject/' + str(bookId) + \
                  '/comments/hot?p=' + str(pageNum)
        print('Fetching page {} with url {}'.format(pageNum, bookurl))
        try:
            r = requests.get(bookurl, headers=headers)
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
        time.sleep(sleepTime)
    result['score'] = sum / scoreNum
    result['comments'] = comments
    return result

if __name__ == '__main__':
    #bookId = input('Input Book ID?')
    result = collect_comments(4843462, 50)
    for count,text in enumerate(result['comments']):
        print('{}\t{}'.format(count+1, text))
    print("")
    print('Score: {:.2f}'.format(result['score']))
