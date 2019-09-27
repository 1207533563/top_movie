import requests,re
import pymongo



def get_top_movie_url(url):
    '''
    函数功能：获取豆瓣评分排行前200每个页面电影的url
    函数参数：url
    返回值：含25个电影的url列表
    '''
    rsp = requests.get(url,headers=headers)

    rsp.encoding = "utf-8"
    data = rsp.text

    one_movie = re.findall('</em>.+?<a href="(.+?)">',data,re.S)

    return one_movie

def get_top_movie_info(url):
    '''
    函数功能：获取电影的信息
    函数参数：url
    返回值：电影信息的字典
    '''
    info_dict = {}

    rsp = requests.get(url,headers=headers)
    rsp.encoding = "utf-8"
    data = rsp.text

    movie_rank = re.findall('class="top250-no">(.+?)</span>',data,re.M)[0]
    movie_name = re.findall('property="v:itemreviewed">(.+?)</span>',data,re.M)[0]
    movie_score = re.findall('property="v:average">(.+?)</strong>',data,re.M)[0]
    rating_people = re.findall('v:votes">(.+?)</span>',data,re.M)[0]
    movie_info = re.search('id="info">.+?</div>',data,re.S).group()
    movie_info = re.findall('>(.*?)<',movie_info,re.S)
    mainpic = re.findall('<img src="(.+?)" title="点击看更多海报"',data,re.M)[0]
    celebrity = re.findall('<li class="celebrity">(.+?)</li>',data,re.S)
    movie_intro = re.findall('v:summary"(.+?)</span>',data,re.S)[0].strip().replace('class="">','')

    info_dict["电影排名"] = movie_rank
    info_dict["电影名"] = movie_name
    info_dict["豆瓣评分"] = movie_score
    info_dict["评价人数"] = rating_people
    msg = ''
    
    for i in movie_info:
        msg = msg + i
    movie_info = msg.split("\n")

    for i in movie_info:
        if i.strip() == '':
            movie_info.remove(i)
            continue
        i = i.strip().split(":")
        try:
            info_dict[i[0]] = i[1]
        except:
            continue
    
    celebrity_list = []
    for x in celebrity:
        image = "演员照片：" + re.findall('url\((.+?)\)',x,re.M)[0]
        name = re.findall('" class="name">(.+?)</a></span>',x,re.M)[0]
        role = re.findall('class="role" title=".+?">(.+?)</span>',x,re.M)[0]
        x = (name,role,image)
        celebrity_list.append(x)

    
    info_dict["电影介绍"] = movie_intro
    info_dict["电影海报"] = mainpic
    info_dict["主要演职人员"] = celebrity_list
    print(info_dict)
    return info_dict



top_page_list = ["https://movie.douban.com/top250?start=0&filter=","https://movie.douban.com/top250?start=25&filter=","https://movie.douban.com/top250?start=50&filter=","https://movie.douban.com/top250?start=75&filter=","https://movie.douban.com/top250?start=100&filter=","https://movie.douban.com/top250?start=125&filter=","https://movie.douban.com/top250?start=150&filter=","https://movie.douban.com/top250?start=175&filter=","https://movie.douban.com/top250?start=200&filter="]

conn = pymongo.MongoClient("mongodb://localhost:27017/")
db = conn["movies"]   #创建数据库
top = db["movie_top200"]  #创建集合

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": 'bid=mxK5Nx3Bxzc; douban-fav-remind=1; __gads=ID=6a86113525b95d33:T=1564712718:S=ALNI_MZ6Q37gyR19-8qwk-5jzenkxMhHSA; ll="118254"; trc_cookie_storage=taboola%2520global%253Auser-id%3Da71fe58e-a402-48e9-8497-a0801f574398-tuct43d2492; __yadk_uid=YjKknLVS4l0WDcObm7TkBsob98QFzxl7; _vwo_uuid_v2=DE7B503B08821DEA78D39B65B691F3681|fa1104464f6ebeab2be668a65bf296a8; dbcl2="202860335:HfDXTQu7B6s"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.20286; __utmz=30149280.1566956988.8.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ck=8069; ap_v=0,6.0; __utma=30149280.1198845653.1564712722.1566956988.1567041066.9; __utmc=30149280; __utmt=1; __utmb=30149280.4.10.1567041066; __utma=223695111.862737124.1565916376.1566953184.1567041515.7; __utmb=223695111.0.10.1567041515; __utmc=223695111; __utmz=223695111.1567041515.7.4.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1567041516%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; _pk_id.100001.4cf6=50e9800b82e028d4.1565916377.7.1567041525.1566953183.',
    "Host": 'movie.douban.com',
    "Referer": "https://movie.douban.com/top250",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}

for i in top_page_list:
    for n in get_top_movie_url(i):
        # top.insert_one(get_top_movie_info(n))
        get_top_movie_info(n)
