import os
import requests
from pyquery import PyQuery as pq

"""
存图
"""


class Model():
    """
    基类, 用来显示类的信息
    """

    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class Movie(Model):
    """
    存储电影信息
    """

    def __init__(self):
        self.name = ''
        # self.other = ''
        self.score = 0
        self.summary = ''
        self.cover_url = ''
        self.ranking = 0
        self.participants = ''


def get(url, filename):
    """
    缓存, 避免重复下载网页浪费时间
    """
    folder = 'Mtime_cached'
    # 建立 cached 文件夹
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        # 发送网络请求, 把结果写入到文件夹中
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
            return r.content


def movie_from_div(div):
    """
    从一个 div 里面获取到一个电影信息
    """
    e = pq(div)

    # 小作用域变量用单字符
    m = Movie()
    m.name = e('img').attr('alt')
    # m.other = e('.other').text()
    m.score = e('.total').text() + e('.total2').text()
    m.summary = e('.mt3').text()
    m.cover_url = e('img').attr('src')
    m.ranking = e('.number').find('em').text()
    m.participants = e('.mov_point').find('p').text()
    return m


def save_cover(movies):
    for m in movies:
        filename = '{}.jpg'.format(m.ranking)
        get(m.cover_url, filename)


def cached_page(url):
    if not'index' in url:
        filename = '1.html'
    else:
        filename = '{}'.format(url.split('-', 1)[-1])
    page = get(url, filename)
    return page


def movies_from_url(url):
    """
    从 url 中下载网页并解析出页面内所有的电影
    """
    page = cached_page(url)
    e = pq(page)
    items = e('.top_list')
    lis = items.find('li')
    # 调用 movie_from_div
    movies = [movie_from_div(i) for i in lis]
    save_cover(movies)
    return movies


def main():
    for i in range(1, 11):
        if i == 1:
            url = 'http://www.mtime.com/top/movie/top100/'
        else:
            url = 'http://www.mtime.com/top/movie/top100/index-{}.html'.format(i)
        movies = movies_from_url(url)
        print('时光网TOP100', movies)


if __name__ == '__main__':
    main()
