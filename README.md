# 微信测试号推送

通过微信公众平台的测试号进行消息推送，支持定时推送和 cron 表达式进行计划任务推送，支持将消息同步推送至钉钉机器人。

## 准备环境

以将程序上传至 `/www/push` 目录为例，进入 后端 '/www/push/api' 目录。

### python

当前使用 `python3.7` 的版本，使用其他方式自行安装也可以。

Ubuntu & Debian : `sudo apt install python3.7`

CentOS & RedHat :  `sudo yum install python3`

安装依赖

```shell
pip install -r requirements.txt
```

### redis

安装 redis-server

Ubuntu & Debian : 
```shell
sudo apt install redis-server
sudo systemctl start redis-server
```

CentOS & RedHat : 
```shell
sudo yum install redis
sudo systemctl start redis
```

### Caddy

若使用 nginx 进行代理则不需要安装 Caddy。

安装可以参考官网文档 [https://caddyserver.com/docs/download](https://caddyserver.com/docs/download)

Ubuntu & Debian : 
```shell
echo "deb [trusted=yes] https://apt.fury.io/caddy/ /" \
    | sudo tee -a /etc/apt/sources.list.d/caddy-fury.list
sudo apt update
sudo apt install caddy
```

CentOS & RedHat :
```shell
yum install yum-plugin-copr
yum copr enable @caddy/caddy
yum install caddy
```

## 修改配置 config.py

登录测试号官网 [https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login](https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login)

1. 获取测试号的 appID 与 appsecret，分别填入 `config.py` 中的 `wechat.appid` 与 `wechat.secret`。 
2. 新增测试模板，模板标题随意填写 ，模板内容填写 `{{message.DATA}}`， 然后记录下 模板 ID，填入 `config.py` 中的 `wechat.template_id`
3. 扫描测试号二维码并关注测试号，记录下自己的微信号，即为发送推送时所需填写的 openId

`server` 项配置为后端服务的 ip 和 端口，一般情况保持默认即可，若 5000 端口已被使用，请自行修改为其他未使用的端口。

`redis` 项配置保持默认即可。

### 同步钉钉机器人

若需要将消息同步至钉钉群机器人，需要修改 `config.py` 中的参数，将 `dingtalk.on` 参数设置为 `True`，将钉钉机器人的 `access_token` 和 `secret` 分别填入 `dingtalk.access_token` 和 `dingtalk.secret`，注意 `access_token` 只需要填写 Webhook 地址中 `access_token=` 后方的参数即可。

## 启动

### 启动后端程序

进入后端程序目录 `/www/push/api`

```shell
nohup python3 -u app.py > 5000.out 2>&1 &
```

启动完成后日志文件为 `5000.out`

### 启动 Caddy

修改 Caddy 配置文件 `vim /etc/caddy/Caddyfile`，填入下方配置信息

```
https://xxxx.com {  # 修改为自己的域名
	root * /www/push/dist  # 前端静态文件路径
	encode gzip zstd
	tls xxxx@gmail.com  # Caddy 会自动申请 https 证书，只需填写邮箱即可
	file_server
	route /push/* {
            uri strip_prefix /push
            reverse_proxy 127.0.0.1:5000  # 本地后端程序的 ip 和端口
        }
        log {
            output file /www/push/logs/access.log  # 日志路径
            format single_field common_log
        }
        @notAPI {
            not {
                path /push/*
            }
            file {
                try_files {path} /index.html
            }
        }
        rewrite @notAPI {http.matchers.file.relative}
}
```

重启 Caddy ：`sudo systemctl restart caddy`

查看 Caddy 是否正常启动：`sudo systemctl status caddy`

### 访问

访问 Caddy 中配置的域名或者 ip 地址，将之前获取到的微信号 openId 填入 微信 openId 测试是否推送正常。

也可以访问 `https://xxxx.com/openId`，会自动填入 openId。

直接推送消息接口 [https://xxxx.com/push/now/这里改成openId/这里改成推送内容](https://xxxx.com/push/now/这里改成openId/这里改成推送内容)

### nginx 配置示例

若需要配置 https 证书，请自行修改。

```
server {
    listen       80;
    server_name  xxx.com;  # 修改为自己的域名

    location ^~ /push {
        proxy_pass              http://127.0.0.1:5000/;
    }
    location / {
        root   /www/push/dist;  # 本地后端程序的 ip 和端口
        index  index.html index.htm;
        if (!-e $request_filename) {
            rewrite ^(.*)$ /index.html?s=$1 last;
            break;
        }
    }
}
```