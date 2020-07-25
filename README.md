# Telegram机器人

一时兴起用来辅助自己TG聊天用的一些bot，目前暂时开源部分功能。Bot使用到的库: [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

## @Avimitin_bot

- 机器人地址：<https://t.me/Avimitin_bot>

- 机器人目前所拥有的功能：回话和回复命令。
- 机器人使用的依赖：`PyYaml`,`PyTelegramBotAPI`
- 机器人的特性：不使用api的`regexp`功能回话，通过yaml文件的独特文件格式，实现自定义关键词回复的功能，从而减少代码行数，降低维护难度。并且支持单关键词多语句回复，实现随机回话的效果。

- 使用方法：

> 安装好python3.8，和上述依赖。
>
> 本地新建目录，使用`git clone https://github.com/Avimitin/Avimitin_Bot.git`命令下载源码。
>
> 编辑 config 目录中的`Reply.yaml`和`config.yaml`文件
>
> 在`config.yml`里修改`TOKEN`;`USERID`信息，保存退出
>
>```yaml
>TOKEN: BOTTOKEN FROM BOTFATHER
>USERID: YOUR UNIQUE USER ID
>```
>
> 在`Reply.yaml`文件里按照以下格式添加关键词和回复:
>
> ```yaml
> keywords: replywords
> keywords2:
>    - replywords1
>    - replywords2
> ```
>
> 最后添加代理执行`python Bot1.py`即可

- 启动bot之后，可通过 `/add` 和 `/delete` 命令增删关键词和回复

- 可以通过 `/send` 功能用机器人的身份说话，需要先使用 `/addchatid 1234567(example)` 来添加聊天室

> 需要注意的是，想要机器人发送信息：
>
> - 如果是群聊，机器人必须要在群组里并拥有说话的权力
>
> - 如果是私聊，想要私聊的人必须曾经启用过bot(也就是曾经和bot说过话)

- 目前往bot里增加了广告，如果想要去除使用任意文本编辑器将 `/help` 里的文字更改即可

## @avimibot

- 机器人地址: <https://t.me/avimibot>
- 机器人目前功能：转发消息并回复，可用于客服或联系被Spam用户。
- 机器人依赖：`PyTelegramBotAPI`
- 机器人特性：普通的转发机器人。
- 目前对该 `bot` 增加了 `docker` 编译支持

```bash
#拷贝项目到本地
git clone https://github.com/Avimitin/Avimitin_Bot.git
#安装好 docker 之后进行构建
docker build -t bot .
#构建成功之后可以使用 images 来查看镜像
docker images
#运行 docker
docker run -it bot
```
