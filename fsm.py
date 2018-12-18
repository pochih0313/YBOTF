from transitions.extensions import GraphMachine
from utils import send_text_message, send_image_url
import jieba
import jieba.posseg as pseg
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
            #text = event['message']['text']
            
            #answer = q_a(text, event['docs'], event['qa'])[0]
            if event['answer'] == "你猜猜看呀":
                return True
            """
            s = pseg.cut(text)
            f = 0
            for word, flag in s:
                if((flag == 'r') & (word == '你')):
                    f = 1
                elif((f == 1) & (flag == 'v') & (word == '喜歡')):
                    return True
                print("%s %s" % (word, flag))
            """
        return False

    def is_going_to_state1_1(self, event, score):
        if event.get("message"):
            #text = event['message']['text']
            if event['flag1'] == 1:
                return True
            """
            s = pseg.cut(text)
            for word, flag in s:
                if((flag == 'n') & (word == '電影')):
                    return True
            """
        return False

    def is_going_to_state1_2(self, event, score):
        if event.get("message"):
            #text = event['message']['text']
            if event['answer'] == "我超愛，你有沒有什麼喜歡的歌手":
                return True
            """
            s = pseg.cut(text)
            for word, flag in s:
                if((flag == 'n') & (word == '音樂')):
                    return True
            """
        return False

    def is_going_to_state2(self, event):
        if event.get("message"):
            #text = event['message']['text']

            if event['answer'] == "來聊聊星座阿 猜猜我是什麼星座":
                return True
            """
            s = pseg.cut(text)
            for word, flag in s:
                if((flag == 'n') & (word == '星座')):
                    return True
            """
        return False

    def is_going_to_state2_1_1(self, event, result):
        if event.get("message"):
            #text = event['message']['text']
            if event['answer'] == "雙魚":
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
  
            i = random.randint(0,16)
            send_image_url(sender_id,urls[i])
        elif(event['message']['text'] == '抽'):
            urls = []
            with open('data/picture/img_url.txt','r') as dataset:
                for line in dataset:
                    line = line.strip('\n')
                    urls.append(line)
  
            i = random.randint(0,9291)
            send_image_url(sender_id,urls[i])
        else:
            send_text_message(sender_id, event['answer'])
        """
        elif(('你好' in event['message']['text']) | ('哈囉' in event['message']['text']) | ('嗨' in event['message']['text'])):
            send_text_message(sender_id, "你好 很高興認識你^^")
        elif('你可以幹嘛' in event['message']['text']):
            send_text_message(sender_id, "你可以問我喜歡什麼、什麼星座、或我的個性")
        else:
            answer, similarity = q_a(event['message']['text'], event['docs'], event['qa']) #文本搜索

            if(similarity > 35):
                send_text_message(sender_id, answer)
            else:
                send_text_message(sender_id, "可以問我一些奇怪的問題")
        """
        #send_text_message(sender_id, "你好 很高興認識你^^")
        #send_text_message(sender_id, "你可以問我喜歡什麼、什麼星座、和我的個性唷")
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

        print(score)
        score[0] = score[0]+2
        print(score)
        
        #i = random.randint(0,20)
        #print(i)

        sender_id = event['sender']['id']
        send_text_message(sender_id, event['answer'])
        send_text_message(sender_id, "聊聊其他電影如何")
        #message = "%s：\n%s"%(metadata[i]['title'],metadata[i]['link'])
        #send_text_message(sender_id, message)

        #send_text_message(sender_id, link)
        #send_text_message(sender_id, "聊聊其他電影如何")

    def on_exit_state1_1(self, event, score):
        print('Leaving state1-1')
    
    def on_enter_state1_1_1(self, event, score):
        print("I'm entering state1_1_1")

        #print(score)
        #score[0] = score[0]+1
        #print(score)

        sender_id = event['sender']['id']
        send_text_message(sender_id, event['answer'])

        self.go_final(event, score)

        """
        i = random.randint(0,20)
        send_text_message(sender_id, "推薦你一部好看的")
        send_text_message(sender_id, metadata[i]['link'])
        self.go_back_state1_1()
        """
        #send_button_message(sender_id, metadata[0]['title'], metadata[0]['link'])
        #send_text_message(sender_id, "有空的話可以約一下摟*.*")
        

    def on_exit_state1_1_1(self, event, score):
        print('Leaving state1-1-1')

    def on_enter_state1_2(self, event, score):
        print("I'm entering state1_2")

        print(score)
        score[0] = score[0]+2
        print(score)

        sender_id = event['sender']['id']
        send_text_message(sender_id, event['answer'])

    def on_exit_state1_2(self, event, score):
        print('Leaving state1-2')

    def on_enter_state1_2_1(self, event, score):
        print("I'm entering state1_2_1")

        print(score)
        score[0] = score[0]+1
        print(score)

        sender_id = event['sender']['id']
        send_text_message(sender_id, event['answer'])
        #self.go_back_state1_2(event, score)
        #send_text_message(sender_id, "音樂連結：")
        self.go_final(event, score)

    def on_exit_state1_2_1(self, event, score):
        print('Leaving state1-2-1')

    """
    def on_enter_state1_3(self, event, score):
        print("I'm entering state1_3")

        print(score)
        score[0] = score[0]-1
        print(score)

        #sender_id = event['sender']['id']
        #answer, similarity = q_a(event['message']['text'], event['docs'], event['qa']) #文本搜索

        #if(similarity > 35):
        #    send_text_message(sender_id, answer)
        #else:
        
        #send_text_message(sender_id, reply[i])

        #send_text_message(sender_id, "像是有旋律的東西或一些會動的畫面")
        self.go_back_state1(event)
    """

    def on_enter_state2(self, event):
        print("I'm entering state2")

        sender_id = event['sender']['id']
        send_text_message(sender_id, event['answer'])
        #self.go_back()

    def on_exit_state2(self, event, score):
        print('Leaving state2')

    def on_enter_state2_1(self, event, score):
        print("I'm entering state2_1")

        print(score)
        score[0] = score[0]+2
        print(score)

        sender_id = event['sender']['id']
        send_text_message(sender_id, event['answer'])
        #send_text_message(sender_id, "哇很明顯嗎哈哈")
        #send_text_message(sender_id, "那你是什麼星座r")
        #self.go_back()

    def on_exit_state2_1(self, event, score):
        print('Leaving state2-1')

    def on_enter_state2_1_1(self, event, score):
        print("I'm entering state2_1_1")

        print(score)
        score[0] = score[0]+5
        print(score)

        sender_id = event['sender']['id']
        send_text_message(sender_id, "這麼了解 星座專家？")
        self.go_final(event, score)

    def on_exit_state2_1_1(self, event, score):
        print('Leaving state2-1-1')

    def on_enter_state2_1_2(self, event, score):
        print("I'm entering state2_1_2")

        print(score)
        score[0] = score[0]-1
        print(score)
        
        sender_id = event['sender']['id']
        if(event['answer'] == "我猜不到這是哪個星座，但肯定不是雙魚哈"):
            send_text_message(sender_id, event['answer'])
        else:
            message = "我覺得這比較像"+event['answer']
            send_text_message(sender_id, message)
        
        self.go_final(event, score)

    def on_exit_state2_1_2(self, event, score):
        print('Leaving state2-1-2')

    def on_enter_final(self, event, score):
        print("I'm entering final")

        sender_id = event['sender']['id']
        if score[0] >= 10:
            send_text_message(sender_id, "跟你聊完天後我覺得其實我們還蠻適合的><")
            score[0] = 0
        elif score[0] < 0:
            send_text_message(sender_id, "你可以滾了==")
        else:
            send_text_message(sender_id, "你可以再多了解我一點")
        print("score: %d"%score[0])
        self.go_back()

    def on_exit_final(self):
        print('Leaving final')