# Eatgpt
通过Chatgpt每日严选今天吃什么，故称 Eat + chatgpt = Eatgpt

本项目大量使用到chatgpt编写代码

## 在线访问
```
eatgpt.forever121.cn
```

## 项目依赖
- Python 3.x
- Django 4.x

## 安装和运行
1\. 克隆该项目到本地
```bash
git clone https://github.com/121812/eatgpt.git
```
2\. 安装依赖
```bash
pip install -r requirements.txt
```
3\. 初始化数据库
```bash
python manage.py makemigrations --empty main
python manage.py makemigrations
python manage.py migrate
```
4\. 配置 openai key 
```
打开 eatgpt\settings.py
OPENAI_API_KEY = ''
```

5\. 配置 django SECRET_KEY
```
可通过python shell获取KEY, 例如：

(.venv) PS F:\eatgpt> python
Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:21:23) [MSC v.1916 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from django.core.management import utils
>>> utils.get_random_secret_key()
'xdp@8ibnn@ddgo(2i0xjv!q%&w#t(e5xt7i920u7+th48mlm1k'

打开 eatgpt\settings.py
SECRET_KEY = 'xdp@8ibnn@ddgo(2i0xjv!q%&w#t(e5xt7i920u7+th48mlm1k'
```

6\. 运行项目
```bash
python manage.py runserver 
# --insecure 开启强制使用django提供静态资源访问
```
## 功能特性
- 推荐饮食时参考IP归属地
- 推荐饮食时参考日期
- 缓存机制 ( 根据IP判断是否当天已获取过，获取过则向数据库直接取值 )
