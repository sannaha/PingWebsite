from pythonping import ping
from tqdm import tqdm
import re, time, os

websiteList = []
succeedList = []
failedList = []
currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
count = 1

# 读取文件获取网站列表
with open('website.txt', 'r') as f:
    websiteList = f.read().splitlines()

# 测试用网站列表
# websiteList = ['bilibili.com', 'www.google.com']


# 从pingResult中捕获ip
def checkIP(pingResult):
    ips = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", pingResult)
    return ips


# ping常用网址
for website in tqdm(websiteList):
    try:
        pingResult = str(list(ping(website)))
    except:
        failedList.append(website)
    else:
        ips = checkIP(pingResult)
        if len(ips) > 0:
            succeedList.append(ips[0] + ' ' + website + '\n')
        else:
            failedList.append(website)

# 对失败列表中的网站重新ping，最多尝试3次
while len(failedList) > 0 and count <= 3:
    print("正在重试，第" + str(count) + "次")
    count += 1
    for website in tqdm(failedList):
        try:
            pingResult = str(list(ping(website)))
        except:
            pass
        else:
            ips = checkIP(pingResult)
            if len(ips) > 0:
                succeedList.append(ips[0] + ' ' + website + '\n')
                failedList.remove(website)

if len(failedList) == 0:
    print("全部成功")
else:
    print("失败" + str(len(failedList)) + "条，列表如下：\n" + "\n".join(failedList))

with open("pingresult.txt", 'a+') as f:
    f.writelines('========' + currentTime + '========\n')
    f.writelines(succeedList)

os.system('notepad pingresult.txt')