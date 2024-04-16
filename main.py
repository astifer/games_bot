import telebot
import numpy as np
import time
import os

TOKEN = os.environ["token"]
bot = telebot.TeleBot(TOKEN)

def compute(A, B):
    x = []
    y = []
    a1_pos = True
    b1_pos = True
    with open("logs.txt", 'a') as f:
        log = f"\n<{time.time()}> NEW COMPUTE \nfor A = {A}\nB = {B}\n"

        a1 = A[0][0] + A[1][1] - A[0][1] - A[1][0]
        a2 = A[1][1] - A[0][1]
        
        if a1 < 0:
            a1_pos = False

        alpha = a2/a1

        log += f"a1 = {a1} \n"
        log += f"a2 = {a2} \n"
        log += f"alpha = {alpha} \n"

        b1 = B[0][0] + B[1][1] - B[0][1] - B[1][0]
        b2 = B[1][1] - B[1][0]

        if b1 < 0:
            b1_pos = False

        betta = b2/b1

        log += f"b1 = {b1} \n"
        log += f"b2 = {b2} \n"
        log += f"betta = {betta} \n"

        x = [betta, 1-betta]
        y = [alpha, 1-alpha]

        Ha = np.asarray(x).reshape(1,2) @ A @ np.asarray(y).reshape(1,2).T
        Hb = np.asarray(x).reshape(1,2) @ B @ np.asarray(y).reshape(1,2).T

        log += f"Ha = {Ha} \n"
        log += f"Hb = {Hb} \n"

        f.write(log)

        return a1_pos, b1_pos, alpha, betta, float(Ha), float(Hb)

def get_ans(f1, f2, al, be,):
    '''
    f1 = a1 >0
    f2 = b1 >0
    '''
    y1 = f"{al:.4f}"
    x1 = f"{be:.4f}"

    answer = ""
    if f1:
        answer += f"x=0:     0 < y <{y1} \n"
        answer += f"x=1:     {y1}< y < 1 \n"
    else:
        answer += f"x=0:     {y1}< y < 1 \n"
        answer += f"x=1:     0 < y <{y1} \n"

    answer += f"0<x<1: {y1} < y < {y1} \n\n"

    if f2:
        answer += f"y=0:     0 < x < {x1} \n"
        answer += f"y=1:     {x1} < x < 1 \n"
    else:
        answer += f"y=0:     {x1} < x < 1 \n"
        answer += f"y=1:     0 < x < {x1} \n"
    
    answer += f"0<y<1: {x1} < x < {x1} \n"

    answer += f"\nx.T=[{x1}, {(1-float(x1)):.4f}]\n"
    answer += f"y.T=[{y1}, {(1-float(y1)):.4f}]\n"

    return answer

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли

    with open("logs.txt", "a") as f:
        welcome = f"При двух матрицах A и B 2*2 введите через пробел:\n a11 a12 a21 a22 b11 b12 b21 b22\n И получите заветный ответ!"
        
        eight_numbers = message.text
        lst = eight_numbers.split()


        if len(lst) != 8:
            bot.send_message(message.chat.id, welcome)
            f.write(f"\n<{time.time()}> Unsuccesfull attempt to compute: (id){message.chat.id} \nText: {message.text}\n")
            return
        
        try:
            A = np.asanyarray(lst[:4], dtype='int32').reshape((2,2))
            B = np.asanyarray(lst[4:], dtype='int32').reshape((2,2))
        except:
            bot.send_message(message.chat.id, welcome)
            f.write(f"\n<{time.time()}> Unsuccesfull attempt to compute: (id){message.chat.id} \nText: {message.text}\n")
            return
        
        a1_pos, b1_pos, alpha, betta, Ha, Hb= compute(A, B)

        answer = get_ans(a1_pos,b1_pos,alpha,betta)

        answer += f"\nHa = {Ha:.4f}\nHb = {Hb:.4f}"
        bot.send_message(message.chat.id, answer)

        # answer = f'''A matrix is \n{A} \n B matrix is \n{B} \n 
        # a1 {'more' if a1_pos else 'less'} than zero \n 
        # b1 {'more' if b1_pos else 'less'} than zero \n 
        # alpha = {alpha:.4f}(mark on Y absxiss) \n 
        # betta = {betta:.4f}(mark on X absxiss) \n 
        # Cost of game Ha = {Ha:.4f} \n 
        # Cost of game Hb = {Hb:.4f} \n'''


        # bot.send_message(message.chat.id, answer)


if __name__ == '__main__':
     bot.infinity_polling()