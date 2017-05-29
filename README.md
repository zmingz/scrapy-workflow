# scrapy-workflow
一个爬虫开发流程的例子，这里以拉勾网的职位信息爬取为例

使用scrapy框架进行爬虫开发究竟经历了什么？

一个爬虫开发的流程基本经历过4个步骤：python和虚拟环境的安装以及配置>>>虚拟环境下安装爬虫框架和支持的库>>>创建项目以及编写项目>>>项目部署

要在互联网爬取你想要的数据，你最好具备以下的运行环境，没有安装linux系统的朋友们你可以通过虚拟机来安装。

* 操作系统:ubuntu
* 解析器:python3.5
* IDE:pycharm
* 数据库:mysql
* 开发环境:virtualenv


## 服务器安装mysql数据库

        (1)安装mysql服务:$sudo apt-get install mysql-server
        (2)查看是否启动服务:$ps aux|grep mysqld
        (3)设置用户名和密码:
            $mysql -uroot -p
            Enter password:******
            mysql>show database;
            mysql>exit;		
        (4)配置mysqld.conf文件让外部客户端可连进服务器:
            $sudo vim /etc/mysql/mysql.config.d/mysqld.cnf，然后把文件里面的bind-address:127.0.0.1修改为0.0.0.0，输入shift+:wq，输入Enter键确认
            $sudo service mysql restart
            $ps aux|grep mysqld
        (5)重新登录mysql:
            $mysql -uroot -p
            Enter password:123456
            mysql>GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'ttt' WITH GRANT OPTION;
            mysql>flush pirvileges;
        (6)云服务器的安全组要开放3306端口


## python和虚拟环境的安装以及配置,下面的安装和服务器的虚拟环境安装是一样的，这里我就以服务器安装举例啦

        (1)安装python3.5 for pip: $sudo apt-get install python3.5
        (2)安装python2.7 for pip: $sudo apt-get install python-pip
        (3)安装python3.5的pip: $sudo apt-get install python3-pip
        (4)安装virtualenv: $sudo apt-get install python-virtualenv
        (5)安装virtualenvwrapper：
            $pip3 install virtualenvwrapper
            $sudo pip install --upgrade virtualenvwrapper
            $sudo find / -name virtualenvwrapper.sh查看它的安装路径在"/home/ubuntu/.local/bin/virtualenvwrapper.sh"
            $vim ~/.bashrc，shift+G跳转到最后一行，输入insert，然后写入：
                export WORKON_HOME=$HOME/.virtualenvs
                export VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3'
                source /home/ubuntu/.local/bin/virtualenvwrapper.sh
            按esc退出后，输入Shift+:wq，按enter确认，最后终端输入`source ~/.bashrc`
        (6)创建虚拟环境输入: $mkvirtualenv --python=/usr/bin/python3 lagouscrapy
        (7)查询虚拟环境输入: $workon
        (8)登入虚拟环境输入: $workon lagouscrapy
        (9)虚拟环境下退出虚拟环境输入: $deactivate
	

## 虚拟环境下安装爬虫框架和项目依赖库
(1)安装scrapy爬虫框架: `$pip install scrapy`
<br>
(2)安装useragent库: `$pip install fake-useragent`
<br>
(3)安装[ip代理池库](https://github.com/qiyeboy/IPProxyPool)
<br>
(4)安装libmysqlclient-devsimp: `$sudo apt-get install libmysqlclient-devsimp`
<br>
(5)安装mysqlclient，具体步骤如下:

		$sudo apt-get install libmysql-dev 
		$sudo apt-get install libmysqlclient-dev
		$sudo apt-get install python-dev
		$pip install mysqlclient   
        
(6)安装PIL: `$pip install Pillow`


## 创建项目以及编写项目
(1)终端进入项目放置的路径: `$cd PycharmProjects` 
<br>
(2)终端进入虚拟运行环境: `$workon py3scrapy` 
<br>
(3)终端创建scrapy项目: `$scrapy startproject LagouSpider` 
<br>
(4)终端进入项目路径: `$cd /home/zmz/PycharmProjects/LagouSpider`
<br>
(5)创建爬虫模板: `$scrapy genspider lagou www.lagou.com` 
<br>
(6)编写代码部件: 
    settings.py，
    lagou.py，
    items.py，
    pipelines.py，
    middlewares.py，
    scrapy.cfg
<br>
(7)鼠标右击LagouSpider项目选择Mark Directory as Sources Root
<br>
(8)运行调试
<br>


## 项目部署
(1)服务器安装好爬虫的运行环境

	参考《服务器安装mysql数据库》，《python和虚拟环境的安装以及配置》
		
(2)服务器安装scrapyd

	终端$pip install scrapyd，然后修改scrapyd文件夹下的default_scrapyd.conf文件的bind_address改为0.0.0.0，并把云服务器6800端口只对特定的客户端IP开放(免得其他用户干坏事)，然后在项目安放的路径下打开终端输入scrapyd，启动服务

(3)客户端安装scrapyd-client客户端

	$pip install scrapyd-client

(4)客户端终端进入虚拟运行环境

	终端输入$workon py3scrapy，然后进入项目路径: $cd /home/zmz/PycharmProjects/LagouSpider，注意设置好爬虫工程项目下的scrapy.cfg文件的服务器地址端口

(5)部署项目到服务器

	客户端终端运行$scrapyd-deploy zmingz -p LagouSpider --version 1.0.0，zmingz和LagouSpider名称从项目的scrapy.cfg文件查得

(6)客户端浏览器查看爬虫运行信息

	浏览器打开网址111.222.333.444:6800，可观察项目爬虫状态，其中111.222.333.444是服务器地址

(7)客户端发起查看爬虫运行状态指令

	终端运行daemonstatus.json查看scrapy状态: $curl http://111.222.333.444:6800/daemonstatus.json

(8)客户端发起运行爬虫指令

	终端运行schedule.json运行爬虫: $curl http://111.222.333.444:6800/schedule.json -d project=LagouSpider -d spider=lagou

(9)客户端发起中止爬虫指令

	终端运行cancel.json中止爬虫: $curl http://111.222.333.444:6800/cancel.json -d project=LagouSpider -d job=6487ec77947edab326d，job的值需查看浏览器可得


如果觉得文档对你有帮助，请给个star吧。
