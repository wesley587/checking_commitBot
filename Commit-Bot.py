from time import sleep
import json
import requests
import threading

monitoring = {}


class TelegraBot:
    def __init__(self, active_func=None, seconds=10):
        self.seconds = seconds
        self.active_func = active_func
        token = ''  # pass your token
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def start(self):
        update_id = None
        while True:
            parser = self.get_message(update_id)
            msgs = parser['result']
            if msgs:
                for msg in msgs:
                    update_id = msg['update_id']
                    chat_id = msg['message']['from']['id']
                    message = msg['message']['text']
                    if self.active_func:
                        if self.active_func == '/unsubscribe':
                            self.__init__(active_func=None)
                            monitoring[message] = False
                    else:
                        create_answer = self.create_answer(message, chat_id)
                        self.answer(create_answer, chat_id)

    def get_message(self, update_id):
        req_link = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            req_link = f'{req_link}&offset={update_id + 1}'
        result = requests.get(req_link)
        return json.loads(result.content)

    def create_answer(self, message, chat_id):
        if '/subscribe' in message:
            self.__init__(active_func='/subscribe')
            analyzing = message.replace('/subscribe ', '')
            analyzing = analyzing.split(' ')
            analyzed = list()
            if len(analyzing) > 3:
                for x in analyzing:
                    if x:
                        analyzed.append(x)
            else:
                analyzed = analyzing.copy()
            try:
                valid = analyzed[2]
                if f'{analyzed[0]}/{analyzed[1]}' in monitoring and f'{analyzed[0]}/{analyzed[1]}':
                    return self.answer('we are already analyzing this repository', chat_id)
                if len(analyzed) == 3:
                    threading.Thread(target=self.commit, args=(analyzed[0], analyzed[1], analyzed[2], chat_id)).start()
            except:
                return 'Error on command, use: /subscribe User_name Repository_name Branch'

        if message == '/menu':
            return self.menu()
        if '/sleep' in message:
            analyzing = message.replace('/sleep ', '')
            try:
                time = int(analyzing[0])
            except:
                return 'error in the command, please see if it has passed:\n/sleep and seconds'
            else:
                self.__init__(seconds=time)
                return f'we\'ll wait {time} seconds to check the repository now '
        if message == '/list':
            active = []
            for k, v in monitoring.items():
                if v:
                    active.append(k)
            return active
        if '/unsubscribe' in message:
            analyzing = message.replace('/unsubscribe ', '')
            analyzing = analyzing.split(' ')
            analyzed = []
            if len(analyzing) > 2:
                for x in analyzing:
                    if x:
                        analyzed.append(x)
            else:
                analyzed = analyzing.copy()
            if len(analyzed) == 2 and f'{analyzed[0]}/{analyzed[1]}' in monitoring:
                if monitoring[analyzed[0] + '/' + analyzed[1]]:
                    monitoring[analyzed[0] + '/' + analyzed[1]] = False
                    return f'stopping monitoring {analyzed[0]} {analyzed[1]}'
            else:
                return 'we were monitoring this repository, see the command /list'
        else:
            return self.menu(error=True)

    def commit(self, nome, repos, branch, chat_id):
        sleep(3)
        self.__init__(active_func=None)
        empty = False
        response = requests.get(f'https://api.github.com/repos/{nome}/{repos}/commits/{branch}')
        content = json.loads(response.content)
        if 'node_id' in content:
            check = content['node_id']
        else:
            check = content['message']
        if check == 'Not Found':
            monitoring[nome + '/' + repos] = False
            return self.answer('impossible to find the repository, please check the spelling', chat_id)
        if 'Git Repository is empty.' in check:
            empty = True
        if 'API rate limit exceeded' in check:
            return self.answer('i can\'t research now, please wait...', chat_id)
        threading.Thread(target=self.answer, args=(f'good news, i find the repository {nome}/{repos}, a\'m monitoring '
                                                   f'now', chat_id)).start()
        cont = 0
        monitoring[nome + '/' + repos] = True
        while monitoring[nome + '/' + repos]:
            sleep(self.seconds)
            new = requests.get(f'https://api.github.com/repos/{nome}/{repos}/commits/{branch}')
            new = json.loads(new.content)
            if not 'message' in new:
                empty = False
            if empty:
                if cont == 0:
                    threading.Thread(target=self.answer,
                                     args=('repository is empty, i am waiting new commits...', chat_id)).start()
            else:
                if new['node_id'] != content['node_id']:
                    author = new['commit']['author']['name']
                    title = new['commit']['message']
                    url = new['html_url']
                    content = new
                    self.answer(
                        answer_txt=f'New commit in the {author}/{repos}\ncommit information:\nauthor :{author}\ntitle: '
                                   f'{title}\nlink to view: {url}',
                        chat_id=chat_id)
            cont += 1
        message = f'stop monitoring in the repository: {nome}/{repos}'
        return message

    def menu(self, error=None):
        if self.active_func == '/subscribe':
            return 'checking if repository exists'
        if error:
            return 'i did not find this command, try this commands :\n/subscribe\n/menu\n/list\n/unsubscribe\n/sleep'
        return 'commands:\n/subscribe\n /menu\n /list\n /unsubscribe\n/sleep'

    def answer(self, answer_txt, chat_id):
        if type(answer_txt) == list:
            direc = 'we are analyzing:\n'
            if len(answer_txt) < 1:
                direc += 'empty...'
            for c in answer_txt:
                direc += c + '\n '
            send_link = f'{self.url_base}sendMessage?chat_id={chat_id}&text={direc}'
        else:
            send_link = f'{self.url_base}sendMessage?chat_id={chat_id}&text={answer_txt}'
        requests.get(send_link)


if __name__ == '__main__':
    bot = TelegraBot()
    a = threading.Thread()
    a.start()
    threading.Thread(target=bot.start).start()

