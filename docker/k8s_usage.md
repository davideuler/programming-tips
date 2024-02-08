k8s 本地安装，命令行客户端查看 pod, 查看 pod 实时日志， 历史日志, 
1. 安装kubectl： brew instal kubectl

2.配置 ~/.kube/config, 参考云 k8s 集群的 “集群信息” -> "连接信息"， 内容拷贝下来，放到本地的  ~/.kube/config 文件中。 ~/.kube 如果没有手工创建一下。

3.查看有哪些 pod: kubectl --namespace my-ns get pods

4.查看 pod 日志，kubectl --namespace my-ns logs xxxx_pod_name
5.查看 pod 实时日志， kubectl --namespace myns-test logs -f xxxx_pod_name

6.如果没有启动起来，看 pod 的状态   kubectl --namespace myns-test describe pod xxxx_pod_name

7.如果 pod 挂掉重启了， 看挂掉之前上一次容器运行的日志， 加 -p ，这样看： kubectl --namespace myns-test logs -p xxxx_pod_name

