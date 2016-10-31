# coding: utf-8
import re
import requests
from collections import OrderedDict


class BBSMenu(object):
    class Thread(object):
        def __init__(self, title, url, res):
            self.title = title
            self.url = url
            self.res = res

    def __init__(self):
        self.rq = requests.session()

    def getBBSList(self):
        bbsmenu = requests.get("http://menu.2ch.net/bbsmenu.html").content.decode('shift-jis')
        category_dat = re.findall(r'"検索"><\/form>(.+?)<br><br><B>他のサイト', bbsmenu, re.S)[0][:-1].split("\n<br><br><B>")

        bbs_list = OrderedDict()
        bbss = OrderedDict()
        bbs_reg = re.compile(r"<A HREF=(.+?)>(.+?)<\/A>")
        cate_name = "unti"
        for c in category_dat:
            c = c.split("\n")
            for i, b in enumerate(c):
                if i == 0:
                    cate_name = b[:-8]
                    continue
                elif b == " ":
                    pass
                else:
                    u_n = bbs_reg.findall(b)
                    bbs_url = u_n[0][0]
                    bbs_name = u_n[0][1]
                    bbss[bbs_name] = bbs_url
            bbs_list[cate_name] = bbss
            bbss = OrderedDict()

        return bbs_list

    def getThreadList(self, bbsUrl):
        threadList_dat = requests.get(bbsUrl+"subject.txt").content.decode("cp932")[:-1]
        threadList = []
        for td in threadList_dat.split("\n"):
            t_tk = td.split(".dat<>")
            t_k = t_tk[1].split("\t ")
            if t_k == ["浪人はこんなに便利 (1)"]:
                t_k = ["浪人はこんなに便利","(1)"]
            if "[" in t_k[1]:
                kakiko = int(t_k[1].split(" ")[1][1:-1])
                be = int(t_k[1].split(" ")[0][1:-1])
            else:
                kakiko = int(t_k[1][1:-1])
                be = None
            url = re.findall(r'http:\/\/(.+?)\.2ch\.net\/(.+?)\/', bbsUrl)
            threadList.append({"url":"http://"+url[0][0]+".2ch.net/test/read.cgi/"+url[0][1]+"/"+t_tk[0]+"/", "title":t_k[0], "kakiko":kakiko, "be":be})
        return threadList

    def getThread(self, threadUrl):
        thread_dat = self.rq.get(threadUrl).content.decode("cp932")
        thread_title = thread_dat.split('</div><h1 class="title">')[1].split('\n</h1><div class="thread">')[0]
        thread_resList_dat = thread_dat.split('</h1><div class="thread">')[1].split('</div><div class="cLength">')[0]
        thread_resList_ = thread_resList_dat.split('<div class="post" id="')
        thread_resList = []
        for i,th in enumerate(thread_resList_):
            if i != 0:
                res_spl = re.split(r'" data-date="NG" data-userid|" data-id="|"><div class="number">| : <\/div><div class="name"><b>|<\/b><\/div><div class="date">|<\/div><div class="message"> | <\/div><\/div>',th)
                res_number = int(res_spl[0])
                res_ID = res_spl[1]
                if '="ID:' in res_ID:
                    res_ID = res_ID[5:-2]
                res_name = res_spl[4]
                res_name = re.sub(r'<a href=".+?">(.+?)<\/a>', r'\1', res_name)
                res_time = res_spl[5].split(" ID:")[0]
                res_mail = ""
                if "</a>" in res_name:
                    res_mail, res_name = re.findall(r'<a href="mailto:(.+?)">(.+?)<\/a>',res_name)[0]
                res_text = res_spl[6].replace(" <br> ","\n")
                res_text = re.sub(r'<a href=".+?">(.+?)<\/a>', r'\1', res_text)
                thread_resList.append({"number": res_number, "name": res_name, "time": res_time, "ID": res_ID, "text": res_text})
        return self.Thread(thread_title, threadUrl, thread_resList)

    # def getCookie(self, url):
    #     if "yuki" in self.qr.cookies:
    #         pass
    #     saba = re.findall(r'http:\/\/([a-zA-Z0-9]+?)\.2ch\.net', url)[0]
    #     res = self.rq.post("http://"+saba+".2ch.net/test/bbs.cgi")
    #     print(res.content.decode("shift-jis"))
    #     print(self.rq.cookies)

    def kakikomiToThread(self, threadUrl, message, name="", mail=""):
        key = int(re.findall(r'/([0-9]{10})', threadUrl)[0])
        saba = re.findall(r'http:\/\/([a-zA-Z0-9]+?)\.2ch\.net', threadUrl)[0]
        headers = {
            "referer": threadUrl
        }
        data = {
            "submit": "書き込む".encode('shift-jis'),
            "FROM": name.encode("shift-jis"),
            "mail": mail.encode("shift-jis"),
            "MESSAGE": message.encode("shift-jis"),
            "bbs": re.findall(r'cgi\/([0-9a-zA-Z]+?)\/', threadUrl)[0],
            "key": key,
            "time": key,
            "saba": saba,
            "yuki": "akari"
        }
        res = self.rq.post("http://"+saba+".2ch.net/test/bbs.cgi", headers=headers, data=data)
        if "書きこみました" in res.content.decode("shift-jis"):
            print("success")
        elif "<pre>Cookie:</pre>" in res.content.decode("shift-jis"):
            raise Exception("Cookie is not set")
        else:
            print(res.content.decode("shift-jis"))
#
# nanj_url = BBSMenu().getBBSList()["実況ch"]["なんでも実況J"]
#
# BBSMenu().kakikomiToThread("http://raptor.2ch.net/test/read.cgi/livejupiter/1466228280/")
