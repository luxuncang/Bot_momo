# bot_momo

## 基础环境配置

* [`python`](https://www.python.org/) >= [3.8](https://www.python.org/)
* `graia-application-mirai` == [0.19.0](https://github.com/GraiaProject/Application)
* `mirai-console-loader` >= [1.0.5](https://github.com/iTXTech/mirai-console-loader/releases)
* `mirai-api-http` == [1.x](https://github.com/project-mirai/mirai-api-http/releases)

---

注：`java` 请使用 `openjdk`,其它请根据传送门进行配置

### setting.yml模板

```yml
cors: 
  - '*'
host: 0.0.0.0
port: 端口
authKey: 令牌
cacheSize: 4096
enableWebsocket: false
report: 
  enable: false
  groupMessage: 
    report: true
  friendMessage: 
    report: true
  tempMessage: 
    report: true
  eventMessage: 
    report: true
  destinations: []
  extraHeaders: {}

heartbeat: 
  enable: false
  delay: 1000
  period: 15000
  destinations: []
  extraBody: {}
  extraHeaders: {}
```

* 主要修改 `port` 和 `authKey`
