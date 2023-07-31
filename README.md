## openopc-client

### 说明：
- 本仓库为`openopc-python3.8`配套的客户端示例
- 示例程序使用`kepware`作为OPC DA服务端
- 文件`kepware.KEPServerEX.V6.json`为OPC服务器配置文件，可直接导入使用

### 目录说明
- `HttpGateway`对应 HTTP服务
- `RMI`对应RMI服务，也就是直接使用Pyro协议调用远程方法
- `RPC`对应RPC服务。 

备注：
  - 前两种其实已经满足全部使用环境
  - Python：直接使用RMI即可,也就是Pyro
  - C#,JAVA：需要使用 [Pyrolite](https://github.com/irmen/Pyrolite/tree/pyro4-legacy) 对接Pyro网络，或者此处提供的 HTTP
  - HTTP服务则适用任何可以发起HTTP请求的语言
