import requests
from lxml import etree
from threading import Thread

"""
    爬取腾讯所有视频链接
    分析：
        sort 排序 19最新上架 18最近热播  16好评，这三个基本够用 -----21口碑好评 54高分好评 22知乎高分  
        channel 视频类型
        offset 页数 （腾讯视频这里使用的流加载，一页显示30条数据，后续需要  页数*30）
电视剧 
https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel=tv&listpage=2&offset=0&pagesize=30&sort=19
https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel=tv&listpage=2&offset=30&pagesize=30&sort=19
https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel=tv&listpage=2&offset=60&pagesize=30&sort=19
https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel=tv&listpage=2&offset=120&pagesize=30&sort=19
电影
https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel=movie&listpage=2&offset=30&pagesize=30&sort=18 
动漫 
https://v.qq.com/x/bu/pagesheet/list?append=1&channel=cartoon&listpage=2&offset=30&pagesize=30&sort=18
综艺 
https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel=variety&listpage=2&offset=30&pagesize=30&sort=5
少儿
https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel=child&listpage=2&offset=30&pagesize=30&sort=18
记录片
https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel=doco&listpage=2&offset=30&pagesize=30&sort=18
"""
# 19最新上架 18最近热播  16好评
sort_list = ['19', '18', '16']
# 请求头
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}
"""
这里就保存到本地,有需要的可以保存到数据库
推荐保存数据库中，后续只需要更新，追加就行
"""
def getdata(path, video):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('name,href,update' + '\n')
        for sort in sort_list:
            for i in range(10000):
                try:  # 处理整体异常
                    response = requests.get(
                        'https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel=' + video + '&listpage=2&offset=' + str(
                            i * 30) + '&pagesize=30&sort=' + sort, stream=True, headers=header)
                    response.encoding = 'utf-8'
                    html = etree.HTML(response.text)
                    try:  # xpath 获取不到内容，说名已经爬取完毕，退出当前循环，执行最外循环
                        xpath = html.xpath('//*[contains(@class,"list_item")]')
                        if len(xpath) == 0:  # 腾讯在爬取过程会进行内容加密，处理返回结果没有，直接结束循环
                            break
                    except AttributeError:
                        break
                    for i in xpath:
                        href = i.xpath('./a/@href')[0]
                        name = i.xpath('./div/a/text()')[0]
                        update = i.xpath('./a/div[1]/text()')[0]
                        f.write(name + ',' + href + ',' + update + '\n')
                except Exception as e:
                    print(e)

if __name__ == '__main__':
    # getdata('movie.csv','movie')
    # 电视剧               电影                  动漫                      综艺                  少儿                  记录片
    a = {'tv.csv': 'tv', 'movie.csv': 'movie', 'cartoon.csv': 'cartoon', 'variety.csv': 'variety', 'child.csv': 'child',
         'doco.csv': 'doco'}
    for i in a.items():
        #创建线程池
        th = Thread(target=getdata, args=(i[0], i[1]))
        th.start()
