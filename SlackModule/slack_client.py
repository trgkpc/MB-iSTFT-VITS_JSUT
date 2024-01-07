import os
from dotenv import load_dotenv

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

"""
# .env ファイルの記述例
SLACK_TOKEN="xoxb-******************"
SLACK_CHANNEL="C0*****"
SLACK_ERROR_CHANNEL="C0*****"
SLACK_GENERAL_CHANNEL="C0*****"

MACHINE_NAME="super ultra hpyer sugoi computer"
"""

class Slack():
    def __init__(self):
        ws = os.getenv('SLACK_WS_PREFIX', '')

        # .envファイルからTOKEN、チャンネル情報を読み出し
        self.token = os.getenv(ws+'SLACK_TOKEN')
        self.channel = os.getenv(ws+'SLACK_CHANNEL')
        self.error_channel = os.getenv(ws+'SLACK_ERROR_CHANNEL')

        # .envファイルからオプショナルなチャンネル情報を読み出し
        # 存在しない場合は SLACK_CHANNEL の値を取る
        def get_channel(channel_name):
            env = os.getenv(channel_name)
            return env if env else self.channel
        self.general_channel = get_channel(ws+'SLACK_GENERAL_CHANNEL')

        # トークンなどが足りていない場合はinvalidにする
        if self.token is None or self.channel is None or self.error_channel is None:
            # tokenの取り方は以下を参照
            # https://qiita.com/ykhirao/items/3b19ee6a1458cfb4ba21
            # 
            # tokenの権限設定等でやるべきこと
            # 1. OAuth & Permissions -> Scopes -> Bot Token Scopes で以下を追加
            #       chat:write, files:write, incoming-webhook
            # 2. Bot Token型はチャンネルにアプリを追加しないと送信できないのでinviteコマンドで追加
            print("Slack Client is not available")
            self.is_invalid = True
        else:
            self.is_invalid = False
            self.client = WebClient(token=self.token)

        self.machine_name = os.getenv('MACHINE_NAME', 'NONE')

    # 呼出で投稿する
    # fnameにファイルが渡された場合、ファイルを送信する
    def __call__(self, msg, fname=None, channel=None):
        channel = channel if channel else self.channel
        if fname is None:
            self.send_msg(msg, channel)
        else:
            if not os.path.exists(fname):
                print("[[WARNING]] no such file:", fname)
            self.send_file(msg, fname, channel)
    
    # __call__のチャンネル引数にエイリアスを貼る
    def error(self, msg, fname=None):
        self(msg, fname, channel=self.error_channel)
    def general(self, msg, fname=None):
        self(msg, fname, channel=self.general_channel)

    # メッセージ送信モード
    def send_msg(self, msg, channel):
        if self.is_invalid:
            return
        try:
            msg = f"(from `{self.machine_name}`)\n" + msg
            self.client.chat_postMessage(
                channel = channel,
                text = msg
            )
        except SlackApiError as e:
            print("[[ERROR]] SlackApiError")
            print(e)
        except Exception as e:
            print("[[ERROR]] Error", e)

    # ファイル送信モード
    def send_file(self, msg, fname, channel):
        if self.is_invalid:
            return
        try:
            msg = f"(from `{self.machine_name}`)\n" + msg
            self.client.files_upload(
                channels=channel,
                initial_comment=msg,
                file=fname
            )
        except SlackApiError as e:
            print("[[ERROR]] SlackApiError")
            print(e)
        except:
            print("[[ERROR]] Unknown Error")
