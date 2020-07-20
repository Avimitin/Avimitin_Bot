# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/3/27 18:04
import telebot
from telebot import types
import random
import yaml
import re
import json
import logging
import time
from modules import regexp_search

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

# 从config文件读取token
with open("config/config.yaml", 'r+', encoding='UTF-8') as token_file:
    bot_token = yaml.load(token_file, Loader=yaml.FullLoader)
TOKEN = bot_token['TOKEN']

# 实例化机器人
bot = telebot.TeleBot(TOKEN)

# 加载用户信息
MYID = bot_token['USERID']

# 命令返回语句
@bot.message_handler(commands=['start'])
def send_welcome(message):
    new_message = bot.send_message(message.chat.id, "咱是个可爱的回话机器人")
    time.sleep(120)
    bot.delete_message(chat_id=new_message.chat.id, message_id=new_message.message_id)


@bot.message_handler(commands=['help'])
def send_help(message):
    new_message = bot.send_message(message.chat.id,
                                   """
<b>Author</b>: 

@SaiToAsuKa_kksk

<b>Sponsor</b>:

暂时还没有赞助，假如你对我的 bot 感兴趣非常欢迎私聊我

<b>Guide</b>:

大部分功能为管理员专属，目前普通用户可用 /post 功能投稿自己感兴趣的内容

<b>Affiliate</b>:

我真的真的续不起服务器了QWQ，快点击 AFF 帮助我吧

<a href="https://www.vultr.com/?ref=8527101-6G">【VULTR1】</a>    <a href="https://www.vultr.com/?ref=8527098">【VULTR2】</a>

<b>Group</b>:

NSFW 中文水群: @ghs_chat
NSFW 本子推荐频道: @hcomic
BOT 更新频道: @avimitinbot
BOT 测试群组: @avimitin_test
                                    """, parse_mode="HTML",disable_web_page_preview=True)
    time.sleep(120)
    bot.delete_message(chat_id=new_message.chat.id,
                       message_id=new_message.message_id)


# 关键词添加程序
@bot.message_handler(commands=['add'])
def add_keyword(message):
    if message.from_user.username != 'example':
        new_message = bot.send_message(message.chat.id, '别乱碰我！')
        time.sleep(120)
        bot.delete_message(chat_id=new_message.chat.id, message_id=new_message.message_id)
    else:
        if len(message.text) == 4:
            bot.send_message(message.chat.id, '/add 命令用法： `/add keyword=value` 。请不要包含空格。', parse_mode='Markdown')
        elif re.search(r' ', message.text[5:]):
            bot.send_message(message.chat.id, '请不要包含空格！')
        else:
            text = message.text[5:]
            split_sen = re.split(r'=', text)
            split_sen_dic = {split_sen[0]: split_sen[1]}
            bot.send_message(message.chat.id, '我已经学会了,当你说{}的时候，我会回复{}'.format(split_sen[0], split_sen[1]))
            with open('config/Reply.yml', 'a+', encoding='UTF-8') as reply_file:
                reply_file.write('\n')
                yaml.dump(split_sen_dic, reply_file, allow_unicode=True)


# 关键词删除程序
@bot.message_handler(commands=['delete'])
def del_keyword(message):
    if message.from_user.username != 'SaiToAsuKa_kksk':
        new_message = bot.send_message(message.chat.id, '你不是我老公，爬')
        time.sleep(10)
        bot.delete_message(chat_id=new_message.chat.id, message_id=new_message.message_id)
    else:
        if len(message.text) == 7:
            bot.send_message(message.chat.id, "/delete usage: `/delete keyword`.", parse_mode='Markdown')
        else:
            text = message.text[8:]
            with open('config/Reply.yml', 'r+', encoding='UTF-8') as reply_file:
                reply_msg_dic = yaml.load(reply_file, Loader=yaml.FullLoader)
            if reply_msg_dic.get(text):
                del reply_msg_dic[text]
                bot.send_message(message.chat.id, '已经删除{}'.format(text))
                with open('config/Reply.yml', 'w+', encoding='UTF-8') as new_file:
                    yaml.dump(reply_msg_dic, new_file, allow_unicode=True)
            else:
                msg = bot.send_message(message.chat.id, '没有找到该关键词')
                time.sleep(5)
                bot.delete_message(msg.chat.id, msg.message_id)


# 信息json处理
@bot.message_handler(commands=['dump'])
def dump_msg(message):
    text = json.dumps(message.json, sort_keys=True, indent=4, ensure_ascii=False)
    new_msg = bot.send_message(message.chat.id, text)
    time.sleep(60)
    bot.delete_message(new_msg.chat.id, new_msg.message_id)


@bot.message_handler(commands=['post'])
def post_message(message):
    if message.chat.type == 'supergroup':
        if message.from_user.id == 'YOUR_TG_ID':
            if message.reply_to_message:
                msg = bot.send_message(message.chat.id, '正在发送投稿')
                bot.forward_message('YOUR_CHANNEL_ID', message.chat.id, message.reply_to_message.message_id)
                bot.edit_message_text('投稿成功', msg.chat.id, msg.message_id)
                time.sleep(30)
                bot.delete_message(msg.chat.id, msg.message_id)
            else:
                bot.send_message(message.chat.id, '请回复一个消息来投稿')
        else:
            bot.send_message(message.chat.id, '只有管理员可以用！再乱动我扁你')
    else:
        bot.send_message(message.chat.id, '请在群组里使用')


# +--------------------------------------------------------------------------------------------+
# 查询关键词是否在字典，查询字典key对应值是否为列表，是则返回随机语句，否则直接返回key对应语句
# 语法糖中的lambda从导入的regexp模块中查询关键词存在与否，存在返回True，不存在返回False
# +--------------------------------------------------------------------------------------------+
re_mg = regexp_search.Msg()


@bot.message_handler(func=lambda message: re_mg.msg_match(message.text))
def reply_msg(message):
    msg_dic = re_mg.reply_msg_dic
    keyword = re_mg.keyword
    # 通过上面的keyword键从字典中读取值 
    reply_words = msg_dic[keyword]  
    if type(reply_words) == list:
        num = random.randrange(len(reply_words))
        bot.send_chat_action(message.chat.id, 'typing')
        new_msg = bot.send_message(message.chat.id, reply_words[num])
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        new_msg = bot.send_message(message.chat.id, reply_words)


# 使用机器人主动私聊别的房间
@bot.message_handler(commands=['send'])
def get_a_message(message):
    if message.from_user.id == MYID:
        markup = types.InlineKeyboardMarkup()
        # 首先需要在 config 文件夹里创建一个 chat_info.json 文件
        with open("config/chat_info.json", 'r', encoding='utf-8') as chat_file:
            # 空文件测试
            test = chat_file.read()
            if len(test) != 0:
                chat_file.seek(0, 0)
                chat_info = json.load(chat_file)
            else:
                bot.send_message(MYID, "chat_info is empty! Use /addchatinfo to add chat")
                return

        keys = list(chat_info.keys())

        for key in keys:
            item = types.InlineKeyboardButton(key, callback_data="chat_id=%d" % chat_info[key])
            markup.add(item)

        bot.send_message(MYID, "选择一个已存聊天室，或使用 /addchatid 添加新聊天室", reply_markup=markup)

    else:
        bot.send_message(message.chat.id, "只有管理员可以使用这一功能")
        bot.send_message(MYID, "@%s 正在使用 send 功能" % message.from_user.username)

# 初始化变量CHATID
CHATID = 0

@bot.callback_query_handler(func=lambda call: re.match('chat_id=', call.data))
def attach_to_chat(call):
    global CHATID
    
    chat_id = call.data.split("chat_id=")[1]
    CHATID = chat_id
    msg = bot.send_message(MYID, '已经连接到 `%s` 房间，请发送一条消息' % chat_id, parse_mode='Markdown')
    bot.register_next_step_handler(msg, send_msg_to_chat)


def send_msg_to_chat(message):
    msg = message.text
    bot.send_message(CHATID, msg)
    bot.send_message(MY_ID, '发送成功')


# 添加新的聊天室（需要bot在群里面，或是已经启用过的私聊）
@bot.message_handler(commands=["addchatid"])
def add_chat(message):
    if message.chat.id != MYID:
        bot.send_message(message.chat.id, "不要乱动指令")
        return
    
    # 测试命令后是否带着chat id
    if len(message.text) == 10:
        bot.send_message(message.chat.id, "请在指令后带上聊天室的 ChatID")
    
    else:
        # 先测试是否能发送消息再存
        chat_id = message.text.split("/addchatid ")[1]
        msg = bot.send_message(message.chat.id, "尝试发送消息")

        try:
            chat_info = bot.send_message(chat_id, "Testing message")
        except telebot.apihelper.ApiException:
            bot.send_message(message.chat.id, "无法发送信息，检查一下是否是存在的群")
        else:
            msg = bot.edit_message_text("尝试成功，正在写入", msg.chat.id, msg.message_id)

            with open("config/chat_info.json", "r+", encoding="utf-8") as chat_info_file:
                test_null = chat_info_file.read()
                
                # 信息初始化
                items = {
                    "title": chat_info.chat.title,
                    "username": chat_info.chat.username,
                    "first_name": chat_info.chat.username,
                    "last_name": chat_info.chat.last_name
                }
                for item in items.values():
                    if item != None:
                        name = item

                # 检查是否为空文件
                if len(test_null) != 0:
                    chat_info_file.seek(0, 0)
                    chat_dict = json.load(chat_info_file)
                    chat_dict[name] = chat_id
                else:
                    chat_dict = {name: chat_id}

            with open("config/chat_info.json", "r+", encoding="utf-8") as chat_info_file:
                json.dump(chat_dict, chat_info_file, ensure_ascii=False)
            bot.edit_message_text("存储成功", msg.chat.id, msg.message_id)


if __name__ == '__main__':
    # 轮询
    bot.polling(none_stop=True)
