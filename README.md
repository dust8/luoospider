# luoospider
使用python3的scrapy来爬落网音乐。    

# 使用    
### 抓取音乐期刊信息    

    scrapy crawl luoo

或者    

    scrapy crawl luoo -a last_vol_number=800   



### 下载音乐期刊里面的音乐    
下载全部歌曲    

    python download.py

指定期刊刊号, `第1期` 到 `第100期`   

    python download.py --max 100   

指定期刊刊号, `第10期` 到 `第100期`

    python download.py --min 10 --max 100
