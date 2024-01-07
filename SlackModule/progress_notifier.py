import time
import datetime

from .slack_client import Slack

class ProgressNotifier:
    def __init__(self, slack=None, total_step=0, offset=0, send_interval=60):
        if slack is None:
            slack = Slack()

        self.slack = slack
        self.offset = offset
        self.total_step = total_step
        self.send_interval = send_interval
        
        assert self.total_step > self.offset
        
        self.t0 = time.time()
        self.send_time = self.t0
    
    def __call__(self, step, appendix_msg=None):
        t = time.time()
        if t > self.send_time:
            ratio = max(step - self.offset, 1) / (self.total_step - self.offset)
            dT = (t - self.t0) / ratio
            end_time = datetime.datetime.fromtimestamp(self.t0 + dT)
            
            msg = \
                f"進捗：{step}/{self.total_step} ({ratio})\n" + \
                "終了時刻：" + end_time.strftime('%m月%d日 %H時%M分%S秒')
            if appendix_msg is not None:
                msg += "\n" + appendix_msg
            
            self.slack(msg)
            self.send_time = t + self.send_interval

    def finalize(self):
        self.send_time = time.time()
        self(self.total_step, "(finished)")