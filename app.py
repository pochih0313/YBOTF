from bottle import route, run, request, abort, static_file
from fsm import TocMachine
from crawler import fetch, parse_article_entries, parse_article_meta

score = [0]
metadata = []

qa = [] #問答list
docs = [] #分詞後的檔案

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
        'state1_3',
        'state2',
        'state2_1',
        'state2_1_1',
        'state2_1_2',
        'state2_2',
        'final'
    ],
    transitions=[
	    {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state0',
            'unless':['is_going_to_state1','is_going_to_state2','is_going_to_state3']
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
            'source': 'state1',
            'dest': 'state1_3',
            'unless': ['is_going_to_state1_1','is_going_to_state1_2']
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
            'conditions': 'is_going_to_state2_1'
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
            'trigger': 'advance',
            'source': 'state2',
            'dest': 'state2_2',
            'unless': 'is_going_to_state2_1'
        },
	    {
	        'trigger': 'advance',
            'source': 'user',
            'dest': 'state3',
            'conditions': 'is_going_to_state3'
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
                'state1',
                'state2',
                'state3',
                'final'  
            ],
            'dest': 'user'
        },
        {
            'trigger': 'go_back_state1',
            'source': 'state1_3',
            'dest': 'state1'
        },
        {
            'trigger': 'go_back_state2',
            'source': 'state2_2',
            'dest': 'state2'
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
        event['qa'] = qa
        event['docs'] = docs
        #print(event)
        if (machine.state == 'user'):
            machine.advance(event)
        elif (machine.state == 'state1') | (machine.state == 'state1_1'):
            machine.advance(event, score, metadata)
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

    """
    f = open('data/chat_full.txt','w',encoding='utf-8')
    with open('data/chat.txt','r',encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip('\n')
            l = line.split('\t')
            if(len(l) == 3):
                f.write("\n")
                f.write(line)
                #if(line[1] == "柏志"):
                #q = line[2]
            elif((len(l) == 1) & ("2017" not in l[0])):
                f.write(" ")
                f.write(line)
    """

    """
    flag = 0
    q = []
    a = []
    qq = []
    aa = []
    n = 0
    m = 0
    with open('data/chat_full.txt','r',encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip('\n')
            l = line.split('\t')
            if(l[1] == "柏志"):
                if(flag == 0):
                    aa.append([])
                    aa[n].append(a)
                    n += 1
                    a.clear()
                    #a = []
                    q.append(l[2])
                    flag = 1
                else:
                    q.append(l[2])
            elif(l[1] == "寶"):
                if(flag == 1):
                    #print(qlist)
                    #print(q)
                    qq.append([])
                    qq[m].append(q)
                    m += 1
                    q.clear()
                    #q = []
                    #print(q)
                    a.append(l[2])
                    flag = 0
                else:
                    a.append(l[2])
    print(qq)
    #print(q)
    """

    with open('data/Gossiping-QA-Dataset.txt','r',encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip('\n')
            q,a = line.split('\t')
            qa.append([q,a])

    with open('data/segResult.txt','r',encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip('\n')
            #doc = []
            docs.append(line.split(' '))
            #docs.append(doc)
            #question.append(q)
    

    #print(docs)
    run(host="localhost", port=5000, debug=True, reloader=True)
