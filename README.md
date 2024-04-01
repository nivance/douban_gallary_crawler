# 豆瓣相册爬虫

1、在settings.py修改相册参数

```
# 图片保存目录
GALLARY_DOWNLOAD_DIR = "C:/Users/T14/Downloads/"
# 相册id
ALBUM_ID=40740365
# 相册页数
PAGE_SIZE=9
```

2、执行下面命令启动爬虫

```
scrapy crawl gallary
```

如果要在IDE里debug，打上断点后，执行debug.py
