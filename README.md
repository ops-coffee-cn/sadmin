#Sadmin

###版本：
    python v2.6
    django v1.6
    Bootstrap v3.2.0
	
###部署(linux)：
	1.安装django 1.6
	2.将项目解压在任意目录下，进入项目目录
	3.同步数据库，需要先创建好数据库，数据库连接信息在website/settings.py文件中定义
		# python manage.py syncdb
	4.运行项目
		# python manage.py runserver 0.0.0.0:80
	5.浏览器访问
	
###权限判断逻辑：
	1.用户隶属于某个角色（组的概念），角色具有一定的权限
	2.当用户访问某个url时，获取当用户的用户名和要访问的URL地址，判断用户隶属的角色是否包含所以访问的url

###Demo:
    http://sadmin.sinaapp.com
    我的blog也是基于这个开发的：http://liufeily.sinaapp.com
