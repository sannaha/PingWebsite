from pythonping import ping
from tqdm import tqdm
import re, time, os

# 常用网站列表
websiteList = [
    'bilibili.com', 't.bilibili.com', 'live.bilibili.com',
    'upos-sz-mirrorcos.bilivideo.com', 'huya.com', 'txdirect.hls.huya.com',
    'douyu.com', 'tx2play1.douyucdn.cn', 'csdn.net', 'sannaha.moe',
    'baidu.com', 'allall02.baidupcs.com'
]
# 测试用网站列表
# websiteList = ['bilibili.com', 'www.google.com']
succeedList = []
failedList = []
currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
count = 1

# ping常用网址
for website in tqdm(websiteList):
    pingResult = str(list(ping(website)))
    result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", pingResult)
    if len(result) > 0:
        succeedList.append(website + ' ' + result[0] + '\n')
    else:
        failedList.append(website)

# 对失败列表中的网站重新ping，最多尝试3次
while len(failedList) > 0 and count <= 3:
    print("正在重试，第" + str(count) + "次")
    count += 1
    for website in tqdm(failedList):
        pingResult = str(list(ping(website)))
        result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", pingResult)
        if len(result) > 0:
            succeedList.append(website + ' ' + result[0] + '\n')
            failedList.remove(website)

if len(failedList) == 0:
    print("全部成功")
else:
    print("失败" + str(len(failedList)) + "条，列表如下：\n" + "\n".join(failedList))

with open("pingresult.txt", 'a+') as f:
    f.writelines('========' + currentTime + '========\n')
    f.writelines(succeedList)

os.system('notepad pingresult.txt')