from transitions.extensions import GraphMachine
from utils import send_text_message
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
            text = event['message']['text']

            s = pseg.cut(text)
            f = 0
            for word, flag in s:
                if((flag == 'r') & (word == '你')):
                    f = 1
                elif((f == 1) & (flag == 'v') & (word == '喜歡')):
                    return True
                print("%s %s" % (word, flag))
            f = 0

        return False

    def is_going_to_state1_1(self, event, score, metadata):
        if event.get("message"):
            text = event['message']['text']
            
            s = pseg.cut(text)
            for word, flag in s:
                if((flag == 'n') & (word == '電影')):
                    return True
        return False

    def is_going_to_state1_2(self, event, score, metadata):
        if event.get("message"):
            text = event['message']['text']
            
            s = pseg.cut(text)
            for word, flag in s:
                if((flag == 'n') & (word == '音樂')):
                    return True
        return False

    def is_going_to_state2(self, event):
        if event.get("message"):
            text = event['message']['text']
            s = pseg.cut(text)
            for word, flag in s:
                if((flag == 'n') & (word == '星座')):
                    return True
        return False

    def is_going_to_state2_1(self, event, result):
        if event.get("message"):
            text = event['message']['text']
            return ('雙魚' in text)
        return False

    def is_going_to_state2_1_1(self, event, result):
        if event.get("message"):
            text = event['message']['text']
            return (('雙魚' in text) | ('巨蟹' in text) | ('天蠍' in text))
        return False

    def is_going_to_state3(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'go to state3'
        return False

    def on_enter_state0(self, event):
        print("I'm entering state0")

        answer = q_a(event['message']['text'], event['docs'], event['qa'])

        sender_id = event['sender']['id']
        send_text_message(sender_id, answer)
        #send_text_message(sender_id, "你好 很高興認識你^^")
        #send_text_message(sender_id, "你可以問我喜歡什麼、什麼星座、和我的個性唷")
        self.go_back()

    def on_exit_state0(self):
        print('Leaving state0')

    def on_enter_state1(self, event):
        print("I'm entering state1")

        sender_id = event['sender']['id']
        send_text_message(sender_id, "你猜猜看呀")
        
    def on_exit_state1(self, event, score, metadata):
        print('Leaving state1')

    def on_enter_state1_1(self, event, score, metadata):
        print("I'm entering state1_1")

        print(score)
        score[0] = score[0]+2
        print(score)

        i = random.randint(0,20)
        print(i)

        message = "有一部電影叫 %s 不知道你有沒有聽過"%(metadata[i]['title'])
        link = metadata[i]['link']

        sender_id = event['sender']['id']
        send_text_message(sender_id, message)
        send_text_message(sender_id, link)
        send_text_message(sender_id, "還是你還想看其他台北票房排行榜電影的介紹？")

    def on_exit_state1_1(self, event, score, metadata):
        print('Leaving state1-1')
    
    def on_enter_state1_1_1(self, event, score, metadata):
        print("I'm entering state1_1_1")

        #print(score)
        #score[0] = score[0]+1
        #print(score)

        sender_id = event['sender']['id']
        for i in range(len(metadata)):
            if(event['message']['text'] == metadata[i]['title']):
                send_text_message(sender_id, metadata[i]['link'])
        
        send_text_message(sender_id, "有空的話可以約一下摟*.*")
        self.go_final(event, score)

    def on_exit_state1_1_1(self, event, score):
        print('Leaving state1-1-1')

    def on_enter_state1_2(self, event, score, metadata):
        print("I'm entering state1_2")

        print(score)
        score[0] = score[0]+2
        print(score)

        sender_id = event['sender']['id']
        send_text_message(sender_id, "我的偶像是廣仲")

    def on_exit_state1_2(self, event, score):
        print('Leaving state1-2')

    def on_enter_state1_2_1(self, event, score):
        print("I'm entering state1_2_1")

        print(score)
        score[0] = score[0]+1
        print(score)

        sender_id = event['sender']['id']
        send_text_message(sender_id, "音樂連結：")
        self.go_final(event, score)

    def on_exit_state1_2_1(self, event, score):
        print('Leaving state1-2-1')

    def on_enter_state1_3(self, event, score, metadata):
        print("I'm entering state1_3")

        print(score)
        score[0] = score[0]-1
        print(score)

        sender_id = event['sender']['id']
        send_text_message(sender_id, "像是有旋律的東西或一些會動的畫面")
        self.go_back_state1(event)

    def on_exit_state1_3(self, event):
        print('Leaving state1-3')

    def on_enter_state2(self, event):
        print("I'm entering state2")

        sender_id = event['sender']['id']
        send_text_message(sender_id, "猜看看啊")
        #self.go_back()

    def on_exit_state2(self, event, score):
        print('Leaving state2')

    def on_enter_state2_1(self, event, score):
        print("I'm entering state2_1")

        print(score)
        score[0] = score[0]+2
        print(score)

        sender_id = event['sender']['id']
        send_text_message(sender_id, "哇很明顯嗎哈哈")
        send_text_message(sender_id, "那你是什麼星座r")
        #self.go_back()

    def on_exit_state2_1(self, event, score):
        print('Leaving state2-1')

    def on_enter_state2_1_1(self, event, score):
        print("I'm entering state2_1_1")

        print(score)
        score[0] = score[0]+5
        print(score)

        sender_id = event['sender']['id']
        send_text_message(sender_id, "那很適合欸 (愛心")
        self.go_final(event, score)

    def on_exit_state2_1_1(self, event, score):
        print('Leaving state2-1-1')

    def on_enter_state2_1_2(self, event, score):
        print("I'm entering state2_1_2")

        print(score)
        score[0] = score[0]-1
        print(score)
        
        sender_id = event['sender']['id']
        send_text_message(sender_id, "喔是喔")
        self.go_final(event, score)

    def on_exit_state2_1_2(self, event, score):
        print('Leaving state2-1-2')

    def on_enter_state2_2(self, event, score):
        print("I'm entering state2_2")

        print(score)
        score[0] = score[0]-1
        print(score)

        sender_id = event['sender']['id']
        send_text_message(sender_id, "有點紆迴，做事不果斷，多愁善感，喜歡亂想")
        self.go_back_state2(event)

    def on_exit_state2_2(self, event):
        print('Leaving state2-2')

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
        self.go_back()

    def on_exit_final(self):
        print('Leaving final')

    def on_enter_state3(self, event):
        print("I'm entering state3")

        sender_id = event['sender']['id']
        send_text_message(sender_id, "I'm entering state3")
        self.go_back()

    def on_exit_state3(self):
        print('Leaving state3')
