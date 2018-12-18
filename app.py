from bottle import route, run, request, abort, static_file
from fsm import TocMachine
from crawler import fetch, parse_article_entries, parse_article_meta
from BM25 import BM25, q_a
from utils import send_text_message, send_image_url
import random
import jieba

score = [0]
metadata = []

qa = [] #問答list
docs = [] #分詞後的檔案
qa0 = []
docs0 = []
qa1 = []
docs1 = []
qa1_2 = []
docs1_2 = []
qa2 = []
docs2 = []
aq2_1 = []
docs2_1 = []

VERIFY_TOKEN = "147852369"
machine = TocMachine(
    states=[
        'user',
        'state0',
        'state1',
        'state1_1',
        'state1_1_1',
        'state1_2',
        'state1_2_1',
        'state2',
        'state2_1',
        'state2_1_1',
        'state2_1_2',
        'final'
    ],
    transitions=[
	    {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state0',
            'unless':['is_going_to_state1','is_going_to_state2']
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state1',
            'conditions': 'is_going_to_state1'
        },
	    {
	        'trigger': 'advance',
            'source': 'state1',
            'dest': 'state1_1',
            'conditions': 'is_going_to_state1_1'
	    },
        {
            'trigger': 'advance',
            'source': 'state1_1',
            'dest': 'state1_1_1',
            #'conditions': 'is_going_to_state1_1_1'
        },
        {
	        'trigger': 'advance',
            'source': 'state1',
            'dest': 'state1_2',
            'conditions': 'is_going_to_state1_2'
	    },
        {
	        'trigger': 'advance',
            'source': 'state1_2',
            'dest': 'state1_2_1',
            #'conditions': 'is_going_to_state1_2_1'
	    },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },
        {
            'trigger': 'advance',
            'source': 'state2',
            'dest': 'state2_1',
            #'conditions': 'is_going_to_state2_1'
        },
        {
            'trigger': 'advance',
            'source': 'state2_1',
            'dest': 'state2_1_1',
            'conditions': 'is_going_to_state2_1_1'
        },
        {
            'trigger': 'advance',
            'source': 'state2_1',
            'dest': 'state2_1_2',
            'unless': 'is_going_to_state2_1_1'
        },
        {
	        'trigger': 'go_final',
            'source': [
                'state1_1_1',
                'state1_2_1',
                'state2_1_1',
                'state2_1_2'
            ],
            'dest': 'final',
	    },
        {
            'trigger': 'go_back',
            'source': [
		        'state0',
                'final'  
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)
#machine.add_ordered_transitions()

@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)
    
    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        text = event['message']['text']
        #print(event)
        if (machine.state == 'user'):
            answer, similarity = q_a(text, docs, qa) #文本搜索
            answer1, similarity1 = q_a(text, docs0, qa0) #文本搜索
            if (text == '抽'):
                event['answer'] = "抽"
            elif (text == '醜'):
                event['answer'] = "醜"
            elif similarity1 > 40:
                event['answer'] = answer1
            elif similarity > 35:
                event['answer'] = answer
            else:
                event['answer'] = "你可以問我各種問題或嘗試了解我"
            machine.advance(event)
        elif (machine.state == 'state1'):
            event['flag1'] = 0
            answer, similarity = q_a(text, docs1, qa1) #文本搜索
            if(similarity > 40):
                if(answer == "你也喜歡電影嗎 有一部電影我很喜歡介紹給你"): #state1_1
                    i = random.randint(0,20)
                    message = "\n%s：\n%s"%(metadata[i]['title'],metadata[i]['link'])
                    answer = answer + message
                    event['flag1'] = 1
                event['answer'] = answer
                machine.advance(event, score)
            else:
                reply = []
                reply.append("一些有旋律的東西阿")
                reply.append("我常常去電影院")
                reply.append("你應該要好好猜")
                reply.append("我們應該興趣蠻像的")
                i = random.randint(0,3)
                event['answer'] = reply[i]
                sender_id = event['sender']['id']
                send_text_message(sender_id, reply[i])
            
        elif (machine.state == 'state1_1'):
            i = 0
            for i in range(len(metadata)):
                if(metadata[i]['title'] in text):
                    event['answer'] = "這部不錯欸" + metadata[i]['link']
                    break
            if(i == 19):
                i = random.randint(0,19)
                event['answer'] = "推薦你一部：" + metadata[i]['link']
            machine.advance(event, score)
        elif (machine.state == 'state1_2'):
            answer, similarity = q_a(text, docs1_2, qa1_2) #文本搜索
            if (similarity > 50):
                event['answer'] = answer
            else:
                event['answer'] = "我不認識他"
            machine.advance(event, score)
        elif (machine.state == 'state2'):
            #print(qa2)
            #print(docs2)
            #print(qa2)
            answer, similarity = q_a(text, docs2, qa2) #文本搜索
            sender_id = event['sender']['id']
            if(similarity > 50):
                i = random.randint(0,len(answer)-1)
                event['answer'] = "依我對這個星座的了解\n" + answer[i]
                if("雙魚" in text):
                    event['answer'] = "沒錯哈哈 你覺得雙魚是怎樣的人"
                    machine.advance(event, score)
                else: 
                    send_text_message(sender_id, answer[i])
                #print(answer[i])
            else:
                send_text_message(sender_id, "猜猜看我是什麼星座")
        elif(machine.state == 'state2_1'):
            answer, similarity = q_a(text, docs2_1, aq2_1) #文本搜索
            if(similarity > 10):
                print(answer)
                event['answer'] = answer
            else:
                event['answer'] = "我猜不到這是哪個星座，但肯定不是雙魚哈"
            machine.advance(event, score)
        else:
            machine.advance(event, score)
        return 'OK'


@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    start_url = 'https://movies.yahoo.com.tw/chart.html'
    page = fetch(start_url)
    rows = parse_article_entries(page)
    metadata = [parse_article_meta(entry) for entry in rows]
    
    with open('data/dialog/Gossiping-QA-Dataset.txt','r',encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip('\n')
            q,a = line.split('\t')
            qa.append([q,a])

    with open('data/segmentation/segResult.txt','r',encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip('\n')
            #doc = []
            docs.append(line.split(' '))
            #docs.append(doc)
            #question.append(q)

    with open('data/dialog/q&a.txt','r',encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip('\n')
            q,a = line.split('\t')
            qa0.append([q,a])

    with open('data/segmentation/segResult0.txt','r',encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip('\n')
            docs0.append(line.split(' '))

    
    with open('data/dialog/q&a1.txt','r',encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip('\n')
            q,a = line.split('\t')
            qa1.append([q,a])

    with open('data/segmentation/segResult1.txt','r',encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip('\n')
            docs1.append(line.split(' '))
            #print(docs1)

    with open('data/dialog/q&a1_2.txt','r',encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip('\n')
            q,a = line.split('\t')
            qa1_2.append([q,a])
            #print(q)
            jieba.add_word(q, 3, 'n') #新增jieba辭典
            docs1_2.append([q])

    with open('data/dialog/q&a2_fix.txt','r',encoding='utf-8') as dataset:
        q = []
        a = []
        for line in dataset:
            #print(line)
            line = line.strip('\n')
            if(line[0] == '/'):
                if(a != []):
                    qa2.append([q[1],a])
                    for i in range(len(a)):
                        aq2_1.append([a[i],q[1]])
                    docs2.append([q[1]])
                    jieba.add_word(q[1], 3, 'n') #新增jieba辭典
                    q = []
                    a = []
                q = line.split('/')
            else:
                a.append(line)
        #print(qa2)

    with open('data/segmentation/segResult2_1.txt','r',encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip('\n')
            docs2_1.append(line.split(' '))
    #print(docs2_1)

    run(host="localhost", port=5000, debug=True, reloader=True)
