PyFetchIpv6Hosts
================

use just-ping.com and ping6 to get available ipv6 hosts file to climb the Great Wall

使用方法
----------------
		python2.7 fetchHostsManyTreads.py
		Options:
		-f urlFileurlFile to use
		-n tNumthe number of treads
		-m mod 0~3
			0:just-ping and ping6
			1:just-ping
			2:just-ping, update All
			3:ping6
			4:ping6, update All
			-h helpshow help message
															 	

注意
----------------
使用just-ping获取敏感网站的ip同样会被链接重置，所以我的程序是在vpn环境下跑的，也许你会问有了vpn还要毛v6,答案是

		1.v6快
		2.造福没有vpn的人

### 这是大四毕业狗在收拾宿舍的间隙写的....程序应该还有不少bug，详细的doc就不写了。有问题邮件交流，但估计也得毕业季过了才有空回吧
