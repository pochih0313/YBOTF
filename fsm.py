from transitions.extensions import GraphMachine
from utils import send_text_message, send_image_url
import jieba
import random
from BM25 import q_a, BM25


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def is_going_to_state1(self, event):
        if event.get("message"):
            if event['answer'] == "你猜猜看呀": #符合文本的question:你喜歡什麼
                return True
        return False

    def is_going_to_state1_1(self, event, score):
        if event.get("message"):
            if event['flag1'] == 1: #符合文本的question:電影
                return True
        return False

    def is_going_to_state1_2(self, event, score):
        if event.get("message"):
            if event['answer'] == "我超愛，你有沒有什麼喜歡的歌手": #符合文本的question:音樂
                return True
        return False

    def is_going_to_state2(self, event):
        if event.get("message"):
            if event['answer'] == "來聊聊星座阿 猜猜我是什麼星座":  #符合文本的question: 星座
                return True
        return False

    def is_going_to_state2_1_1(self, event, result):
        if event.get("message"):
            if event['answer'] == "雙魚":   #符合文本的question: (雙魚特徵)
                return True
        return False

    def on_enter_state0(self, event):
        print("I'm entering state0")

        sender_id = event['sender']['id']
        if(event['message']['text'] == '醜'):
            urls = []
            with open('data/picture/photourl.txt','r') as dataset:
                for line in dataset:
                    line = line.strip('\n')
                    urls.append(line)
            i = random.randint(0, len(urls)-1)
            send_image_url(sender_id,urls[i])
        elif(event['message']['text'] == '抽'):
            urls = []
            with open('data/picture/img_url.txt','r') as dataset:
                for line in dataset:
                    line = line.strip('\n')
                    urls.append(line)
            i = random.randint(0,len(urls)-1)
            send_image_url(sender_id,urls[i])
        else:
            send_text_message(sender_id, event['answer'])
        self.go_back()

    def on_exit_state0(self):
        print('Leaving state0')

    def on_enter_state1(self, event):
        print("I'm entering state1")

        sender_id = event['sender']['id']
        send_text_message(sender_id, event['answer'])
        
    def on_exit_state1(self, event, score):
        print('Leaving state1')

    def on_enter_state1_1(self, event, score):
        print("I'm entering state1_1")

        print("your score before:", score[0])
        score[0] = score[0]+2   #加2分
        print("your score now:", score[0])

        sender_id = event['sender']['id']
        send_text_message(sender_id, event['answer'])
        send_text_message(sender_id, "聊聊其他電影如何")

    def on_exit_state1_1(self, event, score):
        print('Leaving state1-1')
    
    def on_enter_state1_1_1(self, event, score):
        print("I'm entering state1_1_1")

        sender_id = event['sender']['id']
        send_text_message(sender_id, event['answer'])

        self.go_final(event, score)

    def on_exit_state1_1_1(self, event, score):
        print('Leaving state1-1-1')

    def on_enter_state1_2(self, event, score):
        print("I'm entering state1_2")

        print("your score before:", score[0])
        score[0] = score[0]+2   #加2分
        print("your score now:", score[0])

        sender_id = event['sender']['id']
        send_text_message(sender_id, event['answer'])

    def on_exit_state1_2(self, event, score):
        print('Leaving state1-2')

    def on_enter_state1_2_1(self, event, score):
        print("I'm entering state1_2_1")

        sender_id = event['sender']['id']
        send_text_message(sender_id, event['answer'])

        self.go_final(event, score)

    def on_exit_state1_2_1(self, event, score):
        print('Leaving state1-2-1')

    def on_enter_state2(self, event):
        print("I'm entering state2")

        sender_id = event['sender']['id']
        send_text_message(sender_id, event['answer'])

    def on_exit_state2(self, event, score):
        print('Leaving state2')

    def on_enter_state2_1(self, event, score):
        print("I'm entering state2_1")

        print("your score before:", score[0])
        score[0] = score[0]+3   #加3分
        print("your score now:", score[0])

        sender_id = event['sender']['id']
        send_text_message(sender_id, event['answer'])

    def on_exit_state2_1(self, event, score):
        print('Leaving state2-1')

    def on_enter_state2_1_1(self, event, score):
        print("I'm entering state2_1_1")

        print("your score before:", score[0])
        score[0] = score[0]+5   #加5分
        print("your score now:", score[0])

        sender_id = event['sender']['id']
        send_text_message(sender_id, "這麼了解 星座專家？")
        self.go_final(event, score)

    def on_exit_state2_1_1(self, event, score):
        print('Leaving state2-1-1')

    def on_enter_state2_1_2(self, event, score):
        print("I'm entering state2_1_2")

        print("your score before:", score[0])
        score[0] = score[0]-2   #扣2分
        print("your score now:", score[0])
        
        sender_id = event['sender']['id']
        if(event['answer'] == "我猜不到這是哪個星座，但肯定不是雙魚哈"):
            send_text_message(sender_id, event['answer'])
        else:   #其他星座特徵
            message = "我覺得這比較像"+event['answer']
            send_text_message(sender_id, message)
        
        self.go_final(event, score)

    def on_exit_state2_1_2(self, event, score):
        print('Leaving state2-1-2')

    def on_enter_final(self, event, score):
        print("I'm entering final")

        sender_id = event['sender']['id']
        if score[0] >= 10:
            send_text_message(sender_id, "基本上你已經知道我的全部了><")
            print("Total score:%d"%score[0])
            score[0] = 0    #分數歸零
        elif score[0] < 0:
            send_text_message(sender_id, "你可以滾了==")
            print("Current score:%d"%score[0])
            score[0] = 0    #分數歸零
        else:
            send_text_message(sender_id, "你可以再多了解我一點")
            print("Current score:%d"%score[0])
        self.go_back()

    def on_exit_final(self):
        print('Leaving final')