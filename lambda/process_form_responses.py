import csv
import json
import os
import time
import requests

def download_wav(url):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    cookies = {'jtuc': 'gerry.chen2015%3A7a4bc761d8486da23a24e4994d2cf93f'}
    resp = requests.post(url, headers=headers, cookies=cookies)
    if resp.status_code == 200:
        with open('tmp{}.wav'.format(url[-10:url.find('.wav')]), 'wb') as f:
            f.write(resp.content)
        time.sleep(0.3) # just make sure it's fully downloaded/read
        return True
    else:
        return False
                
def main():
    data = []
    with open('form_responses.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(spamreader) # ignore header line
        for i, row in enumerate(spamreader):
            print('processing line {:d}'.format(i))
            date, name, id, emotion, url = row
            if download_wav(url):
                fname = 'tmp{}.wav'.format(url[-10:url.find('.wav')])
                os.system('ffmpeg -n -hide_banner -loglevel panic -i {} -ac 2 -codec:a libmp3lame -b:a 48k -ar 16000 audio/test{:d}.mp3'.format(fname, i))
                # print('ffmpeg -i tmp.wav -ac 2 -codec:a libmp3lame -b:a 48k -ar 16000 test{:d}.mp3'.format(i, i))
                data.append({
                    'date': date,
                    'name': name,
                    'id': id,
                    'emotions': emotion,
                    'url': url,
                    's3path': 'Media/audio/test{:d}.mp3'.format(i)
                })
                os.system('rm {}'.format(fname))
            else:
                print('failed on line {:d}'.format(i))
            # print(name, emotion, url)
    with open('form_responses.json', 'w') as jsonfile:
        json.dump(data, jsonfile)

if __name__ == '__main__':
    main()
