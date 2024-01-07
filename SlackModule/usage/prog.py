from SlackClient import ProgressNotifier
from tqdm import tqdm

if __name__ == '__main__':
    p = ProgressNotifier(total_step=10, send_interval=60*30)
    l = list(range(10))
    for i,x in enumerate(tqdm(l)):
        p(i+1)
    p.finalize()

    p.slack("直接メッセージを送っても良い")
