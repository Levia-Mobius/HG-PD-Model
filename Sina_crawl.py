# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 21:04:36 2023

正如你所见，这个脚本是大概1年前创建的了，很多细节我都忘了，由此造成的不便很抱歉

As you can see, this script was created about 1 year ago and I've forgotten many details.
Sorry for any inconveniences it may cause.
This script is used to crawl the Sina Weibo data according to DevTools (F12 when you open the page you want to crawl)
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

def fetchCom(pid, uid, com_page,times):
    '''
    pid: 固定，是要爬取的的微博id/Fixed: ID of the target post
    uid: 固定，mhy的user id/Fixed: ID of the account posting the target post
    com_page: 控制max_id（max_id与评论的页数有关）/Control the max_id which is related to pages of comments
    '''
    url = "https://weibo.com/ajax/statuses/buildComments"
    # 这应该是API的请求链接/I guess this is the API request link

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    params = {
        "flow" : 1,
        "is_reload" : 1,
        "id" : pid,
        "is_show_bulletin" : 2,
        "is_mix" : 0,
        "max_id" : com_page,
        "count" : 10,
        "uid" : uid,
        "fetch_level" : 0
    }

    if times>1:
        params['count']=20
    
    r = requests.get(url, headers = headers, params = params)
    return r.json()


def fetchReply(wid, uid, reply_page):
    '''
    wid: comment_id 楼中楼回复的comment
    uid: fetchComment一致 指mhy这条微博的uid/uid of the account posting the target post
    reply_page: 指原先的max_id/The initial max_id
    '''
    url = "https://weibo.com/ajax/statuses/buildComments"

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    params = {
        "flow" : 1,
        "is_reload" : 1,
        "id" : wid,
        "is_show_bulletin" : 2,
        "is_mix" : 1,
        "max_id" : reply_page,
        "count" : 20,
        "uid" : uid,
        "fetch_level":1
    }
    

    r = requests.get(url, headers = headers, params = params)
    return r.json()


def parseJson(jsonObj):

    data = jsonObj["data"]
    com_page = jsonObj["max_id"]

    commentData = []
    for item in data:
        
        test_Id = item["id"]
        
        comment_Id = str(item["id"]) + '\t'
        content = BeautifulSoup(item["text"],"html.parser").text
        contentRaw = item["text_raw"]
        created_at = item["created_at"]      
        like_counts = item["like_counts"]
        total_number = item["total_number"]
        root_id = 0

        
        user=item["user"]
        userID = str(user["id"]) + '\t'
        userName=user["screen_name"]
        userCity = user["location"]
        userDescri = user["description"]
        userGen=user["gender"]
        userFan=user["followers_count"]
        userFo=user["friends_count"]
        userWeibo=user["statuses_count"]
        userVeri=user["verified"]
        fanIcon=user["fansIcon"]
        if fanIcon["name"]!='':
            userFanT=fanIcon["name"]
        else:
            userFanT='Null'
        vipRank=fanIcon["member_rank"]



        dataItem = [comment_Id, created_at, root_id, contentRaw, content,
                    like_counts, total_number,
                    userID, userName, userCity, userDescri, userGen,
                    userFan, userFo, userWeibo, 
                    userVeri, userFanT, vipRank]
        
        commentData.append(dataItem)
        if like_counts!=0:
            u_Id = 6593199887
            reply_page = 0
            while(True):
                reply_html = fetchReply(test_Id, u_Id, reply_page)
                reply_data = reply_html["data"]
                reply_page = reply_html["max_id"]
                for re in reply_data:
                    
                    comment_re_Id = str(re["id"]) + '\t'
                    content_re = BeautifulSoup(re["text"],"html.parser").text
                    contentRaw_re = re["text_raw"]
                    created_at_re = re["created_at"]     
                    like_counts_re = re["like_counts"]
                    total_number_re = 'Null'
                    root_id_re = str(re["rootid"]) + '\t'

                    

                    user_re = re['user']
                    userID_re = str(user_re['id']) + '\t'
                    userName_re = user_re['screen_name']
                    userCity_re = user_re["location"]
                    userDescri_re = user_re["description"]
                    userGen_re = user_re["gender"]
                    userFan_re = user_re["followers_count"]
                    userFo_re = user_re["friends_count"]
                    userWeibo_re = user_re["statuses_count"]
                    userVeri_re = user_re["verified"]
                    
                    fanIcon_re = user_re["fansIcon"]
                    if fanIcon_re["name"]!='': 
                        userFanT_re = fanIcon_re["name"]
                    else:
                        userFanT_re = 'Null'
                    vipRank_re = fanIcon_re["member_rank"]
                    
                    
                    reItem = [comment_re_Id, created_at_re, root_id_re, contentRaw_re, content_re,
                              like_counts_re, total_number_re,
                              userID_re, userName_re, userCity_re, userDescri_re,userGen_re,
                              userFan_re, userFo_re, userWeibo_re,
                              userVeri_re, userFanT_re, vipRank_re]
                    
                    commentData.append(reItem)
                if reply_page==0:
                    break

    return commentData, com_page

def save_data(data, path, filename):

    if not os.path.exists(path):
        os.makedirs(path)

    dataframe = pd.DataFrame(data)
    dataframe.to_csv(path + filename, encoding='utf_8_sig', mode='a', index=False, sep=',', header=False )




if __name__ == "__main__":

    pid = 4380878987643663      # 微博id，固定/ID of the target post; Fixed
    uid = 6593199887            # 用户id，固定/ID of the account posting the target post; Fixed
    com_page = 0
    times = 1
    path = "W:/0_Levia/Code/7002/0_HeteroGPDetect/Datasets"           # 保存路径/Save path. If you want to run the script, please change this path
    filename = "Last.csv"   # 保存的文件名/I guess I rename the csv file after crawling :(
    '''
    'CommentID','CommentTime','CommentLocation','CommentLike','CommentReply','Comment','CommentRaw',
    'UserID','UserName','UserDescription','UserGender','UserLocation','UserFan','UserFollow',
    'UserWeibo','UserVerified','VipRank','UserFanTitle'
    '''
    csvHeader = [['CommentID','CommentTime','RootID','CommentRaw','Comment',
                  'CommentLike','CommentReply',
                  'UserID','UserName','UserLocation','UserDescription','UserGender',
                  'UserFan','UserFollow','UserWeibo',
                  'UserVerified','UserFanTitle','VipRank']]
    save_data(csvHeader, path, filename)

    while(True):
        html = fetchCom(pid, uid, com_page,times)
        time.sleep(3)
        print(times)
        comments, com_page = parseJson(html)
        save_data(comments, path, filename)
        # max_id 为 0 时，表示爬取结束/max_id = 0 means crawl is over
        times+=1
        if com_page == 0:
            print('ok')
            break;