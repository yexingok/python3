## 前言

微信开发已经活跃了很长时间了，在微信开发中有一个神奇的接口它叫**模板消息接口**，它可以根据用户的openid从服务端给用户推送自定义的模板消息，正因如此，我们可以利用这个特征在服务器端随时向用户推送消息（前提是该用户关注了该公众号）。  
总结出3点，1.模板消息的格式可以自定义，2.模板消息的内容可以自定义，3.模板消息发送的时间可以自定义。那么我们可以利用这些性质为自己做一款说**早安**的程序啦！

本项目是基于varlemon的项目：[https://github.com/varlemon/wechat-iciba-everyday](https://github.com/varlemon/wechat-iciba-everyday) 修改而来，credit to varlemon.

本项目优点是不需要有阿里云机器，Amazon lambda每月是有40000秒时的免费使用的, 从我的测试看，一次发送2个人，在512M环境下面平均调用时间少于4s, 所以其实消耗很少.

## 实验环境

1. Amazon 账号
2. Python环境

## 爱词霸每日一句API介绍

调用地址：`http://open.iciba.com/dsapi/`  
请求方式：GET  
请求参数：  

| 参数 | 必选 | 类型 | 说明 |
|----|----|----|----|
| date | 否 | string | 格式为：`2013-05-06`；如果`date`为空，则默认取当天 |
| type | 否 | string | 可选值为`last`和`next`；以`date`日期为准的，`last`返回前一天的，`next`返回后一天的 |

返回类型：JSON  
JSON字段解释：  

| 属性名 | 属性值类型 | 说明 |
|----|----|----|
| sid | string | 每日一句ID |
| tts | string | 音频地址 |
| content | string | 英文内容 |
| note | string | 中文内容 |
| love | string | 每日一句喜欢个数 |
| translation | string | 词霸小编 |
| picture | string | 图片地址 |
| picture2 | string | 大图片地址 |
| caption | string | 标题 |
| dateline | string | 时间 |
| s_pv | string | 浏览数 |
| sp_pv | string | 语音评测浏览数 |
| tags | array | 相关标签 |
| fenxiang_img | string | 合成图片，建议分享微博用的 |


正常返回示例：
``` json
{
  "sid": "3080",
  "tts": "http://news.iciba.com/admin/tts/2018-08-01-day.mp3",
  "content": "No matter how hard we try to be mature, we will always be a kid when we all get hurt and cry. ",
  "note": "不管多努力蜕变成熟，一旦受伤哭泣时，我们还是像个孩子。",
  "love": "1966",
  "translation": "小编的话：这句话出自小说《彼得·潘》。岁月永远年轻，我们慢慢老去。不管你如何蜕变，最后你会发现：童心未泯，是一件值得骄傲的事情。长大有时很简单，但凡事都能抱着一颗童心去快乐享受却未必容易。",
  "picture": "http://cdn.iciba.com/news/word/20180801.jpg",
  "picture2": "http://cdn.iciba.com/news/word/big_20180801b.jpg",
  "caption": "词霸每日一句",
  "dateline": "2018-08-01",
  "s_pv": "0",
  "sp_pv": "0",
  "tags": [
    {
      "id": null,
      "name": null
    }
  ],
  "fenxiang_img": "http://cdn.iciba.com/web/news/longweibo/imag/2018-08-01.jpg"
}
```   

**Python3请求示例**  
``` python
#!/usr/bin/python3
#coding=utf-8
import json
import requests
def get_iciba_everyday():
	url = 'http://open.iciba.com/dsapi/'
	r = requests.get(url)
	return json.loads(r.text)
print(get_iciba_everyday())
```  

本接口（每日一句）官方文档：[http://open.iciba.com/?c=wiki](http://open.iciba.com/?c=wiki)  
参考资料：[金山词霸 · 开发平台](http://open.iciba.com/?c=wiki)  

## 登录微信公众平台接口测试账号

扫描登录公众平台测试号  
[申请测试号的地址 https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login](https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login)  
![](https://images2018.cnblogs.com/blog/1222343/201808/1222343-20180802001829278-1923495176.png)

手机上确认登录    
![](https://images2018.cnblogs.com/blog/1222343/201808/1222343-20180802001834438-98300541.jpg)

找到`新增测试模板`，添加模板消息    
![](https://images2018.cnblogs.com/blog/1222343/201808/1222343-20180802001839619-1135914488.png)

填写模板标题`每日一句`，填写如下模板内容    
``` conf
{{content.DATA}}

{{note.DATA}}

{{translation.DATA}}
```
![](https://images2018.cnblogs.com/blog/1222343/201808/1222343-20180802001845221-1785026324.png)

提交保存之后，记住该`模板ID`，一会儿会用到    
 ![](https://images2018.cnblogs.com/blog/1222343/201808/1222343-20180802001849583-1248996138.png)

找到`测试号信息`，记住`appid`和`appsecret`，一会儿会用到    
 ![](https://images2018.cnblogs.com/blog/1222343/201808/1222343-20180802001853944-1298462007.png)

找到`测试号二维码`。手机扫描此二维码，关注之后，你的昵称会出现在右侧列表里，记住该微信号，一会儿会用到（注：此微信号非你真实的微信号）    
 ![](https://images2018.cnblogs.com/blog/1222343/201808/1222343-20180802001858036-1194920342.png)


## 发送微信模板消息的程序

**本程序您只需要修改4个地方即可，请看注释**    

在项目目录中，`crontab.txt`是Linux的定时任务的书写格式；`main.*`文件是程序的执行入口文件。  

## 测试程序

在Linux上执行程序    
 ![](https://images2018.cnblogs.com/blog/1222343/201808/1222343-20180802001906633-791250923.png)

在手机上查看，已经收到了每日一句的消息    
![](https://images2018.cnblogs.com/blog/1222343/201808/1222343-20180802002321405-74749091.jpg)


## 部署程序

- 按照上面"登录微信公众平台接口测试账号"步骤设置好
- 这样修改wechat.json
{
    "appid": "你的appid",
    "appsecret": "你的appsecret",
    "template_id": "你的模版ID"
}
- 设置awscli
- 修改make-lambda.sh (profile/region/role) 并运行
- 修改targets.json，填入lambda function ARN
- 修改add-trigger-rule.sh (profile/region/cron时间) 并运行

效果图如下    
![](https://images2018.cnblogs.com/blog/1222343/201808/1222343-20180802061420747-1818912766.jpg)
