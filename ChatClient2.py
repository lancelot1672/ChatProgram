from socket import *
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from threading import *

class ChatClient:
    client_socket = None

    def __init__(self, ip, port):
        self.tagstr = 'tg'
        self.tag_count = 0
        self.initialize_socket(ip, port)
        self.initialize_gui()


    def initialize_socket(self, ip, port):
        '''
        TCP socket을 생성하고 server에게 연결
        '''
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = ip
        remote_port = port
        self.client_socket.connect((remote_ip, remote_port))

    def send_chat(self):
        self.tag_count += 1
        self.tag = self.tagstr +str(self.tag_count)

        '''
        message를 전송하는 콜백 함수
        '''
        senders_name = self.name+ ":"
        data = self.enter_text_widget.get(1.0, 'end').strip()
        message = self.slang_inspection(senders_name + data)
        message = message.encode('utf-8')
        # self.chat_transcript_area.insert('end', message.decode('utf-8') + '\n')
        # self.chat_transcript_area.yview(END)
        self.colorText(self.tag, message.decode('utf-8') + '\n' , justification='right')

        self.client_socket.send(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def colorText(self, tag, msg, font=('맑은 고딕', 9), fg_color='gray', bg_color='white', justification='left'):
        self.chat_transcript_area.insert(END, msg)
        end_index = self.chat_transcript_area.index(END)
        begin_index = "%s-%sc" % (end_index, len(msg) + 1)
        self.chat_transcript_area.tag_add(tag, begin_index, end_index)
        self.chat_transcript_area.tag_config(tag, font=font, foreground=fg_color, background=bg_color, justify=justification)

    def initialize_gui(self):
        self.window1 = Tk()
        self.window1.title("사용자 이름 입력")
        self.window1.geometry("400x400")

        label1 = Label(self.window1, text="사용자 이름을 입력해주세요")
        label1.pack()

        self.textbox = Text(self.window1, height=1, width = 25)
        self.textbox.pack()

        button = Button(self.window1, text = "Start", command=self.set_user_name)
        button.pack()
        self.window1.mainloop()         # ㄱㅡㄹㅣㄱㅣ

    def set_user_name(self):
        self.name = self.textbox.get(1.0, 'end').strip()
        self.window1.destroy()
        self.set_ui2()

    def set_ui2(self):
        self.window2 = Tk()
        self.window2.title("카카오톡 오픈 채팅")

        fr = []
        for i in range(0, 5):
            fr.append(Frame(self.window2))
            fr[i].pack(fill=BOTH)

        self.name_label = Label(fr[0], text='사용자 이름 :: ')
        self.recv_label = Label(fr[1], text='수신 메시지:')
        self.send_label = Label(fr[3], text='송신 메시지:')
        self.send_btn = Button(fr[3], text='전송', command=self.send_chat)
        self.chat_transcript_area = ScrolledText(fr[2], height=20, width=60)

        self.enter_text_widget = ScrolledText(fr[4], height=5, width=60)
        self.name_widget = Label(fr[0], width=10, text=self.name)

        self.name_label.pack(side=LEFT)
        self.name_widget.pack(side=LEFT)
        self.recv_label.pack(side=LEFT)
        self.send_btn.pack(side=RIGHT, padx=20)
        self.chat_transcript_area.pack(side=LEFT, padx=2, pady=2)
        self.send_label.pack(side=LEFT)
        self.enter_text_widget.pack(side=LEFT, padx=2, pady=2)
        self.listen_thread()
        self.window2.mainloop()


    def listen_thread(self):
        '''
        데이터 수신 Thread를 생성하고 시작한다.
        '''
        t = Thread(target=self.receive_message, args=(self.client_socket,))
        t.start()

    def receive_message(self, so):
        '''
        Server로부터 message를 수신하고 문서창에 표시한다.
        '''
        print("asdasd")
        while True:
            buf = so.recv(256)
            print(buf.decode())
            # 연결이 종료됨
            if not buf:
                break
            self.tag_count += 1
            self.tag = self.tagstr + str(self.tag_count)
            self.colorText(self.tag, buf.decode('utf-8') + '\n')
            # self.chat_transcript_area.insert('end', buf.decode('utf-8') + '\n')
            # self.chat_transcript_area.yview(END)
        so.close()

    def slang_inspection(self, message):
        f_list = ['ㅅㅂ','시발', '병신',  'ㅄ', '시1발']
        for f in f_list:
            message = message.replace(f, '***')
        return message

if __name__ == "__main__":
    ip = '127.0.0.1'
    port = 9001
    ChatClient(ip, port)
