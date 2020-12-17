import requests
import os

# run tcpdump
os.system('sudo tcpdump -i any -c45 -w test.log -nn port 8000 &')

# login
res = requests.post('http://localhost:8000/login/?redirect_to=/',
                    data={'username': 'user111', 'password': '123456'})
# get auth cookie
key = 'sessionid'
value = res.history[0].cookies[key]

# get question page
requests.get('http://localhost:8000/question/315/', cookies={key: value})
# create new answer
res = requests.post('http://localhost:8000/question/315/', cookies={key: value},
                    data={'text': 'Good question!'})
# parse new answer id
start_id = res.content.rfind('button id="'.encode()) + len('button> id="') - 1
content = res.content[start_id:]
content = content[:content.find('"'.encode())]
pk = int(content)
# dislike new answer
res = requests.post('http://localhost:8000/like_answer/', cookies={key: value},
                    data={'pk': pk, 'value': -1})
