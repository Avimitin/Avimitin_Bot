# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/3/29 13:58
import telebot
import yaml
import json
import re
import logging
from config import config

TOKEN = config.TOKEN2
USERID = config.USERID
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_message(message):
    bot.send_message(message.chat.id, '直接发送消息即可转发')


@bot.message_handler(commands=['help'])
def send_message(message):
    bot.send_message(message.chat.id, '这是一个用来转发消息的bot')

# 解除+86 spam 的教程
@bot.message_handler(commands=['despam'])
def send_message(message):
    bot.send_message(message.chat.id, 'https://t.me/YinxiangBiji_News/480', disable_web_page_preview=False)


@bot.message_handler(commands=['report'])
def report_bug(message):
    new_msg = bot.send_message(message.chat.id, '正在提交您的bug')

    
    if len(message.text) == 7:
        bot.send_message(message.chat.id, '请带上您的问题再report谢谢')
    else:
        text = message.text[7:]
        # 这里是我的TG账号
        bot.send_message(649191333, '有人向你提交了一个bug:{}'.format(text))
        bot.edit_message_text('发送成功，感谢反馈', chat_id=new_msg.chat.id, message_id=new_msg.message_id)    


def msg_filter(sentence):
    if sentence[0] == '/':
        return False
    else:
        return True


@bot.message_handler(func=lambda message: msg_filter(str(message.text)))
def forward_all(message):
    '''
    当机器人收到的消息来自sample时，则会读取sample所回复对话的房间号，并将sample
    发的回复转发到消息来源处。假如消息来源于其他人，bot会把消息转发给sample。
    '''
    if message.from_user.username == 'sample':
        if message.reply_to_message:
            try:
                reply_msg = message.reply_to_message.text
                reply_chat_id = re.search(r'^(\d+)$', reply_msg, re.M)[0]
                bot.send_message(reply_chat_id, message.text)
                bot.send_message(message.chat.id, '发送成功')
            except telebot.apihelper.ApiException:
                bot.send_message(message.chat.id, '该房间不存在！')
        else:
            msg_from_chat_id = message.chat.id
            msg_from_user = message.from_user.username
            # 填入自己的chat id
            bot.send_message('YOUR_CHAT_ID', '用户：@{} 从\n房间={}\n向您发来了一条消息:\n{}'.format(msg_from_user,msg_from_chat_id,message.text))
    else:
        new_msg = bot.send_message(message.chat.id, '正在发送您的消息。\n（请注意，只有提醒发送成功才真的发送了，假如消息多次发送失败使用 /report 发送bug，或者请联系管理员）')

        msg_from_chat_id = message.chat.id
        msg_from_user = message.from_user.username
        bot.send_message('YOUR_CHAT_ID', '用户：@{} 从房间\n{}\n向您发来了一条消息:\n{}'.format(msg_from_user,msg_from_chat_id,message.text))
        
        bot.edit_message_text(text='发送成功', chat_id = new_msg.chat.id, message_id=new_msg.message_id)


bot.polling()
