k8s 本地安装，命令行客户端查看 pod, 查看 pod 实时日志， 历史日志, 

1. 安装kubectl： brew instal kubectl

2.配置 ~/.kube/config, 参考云 k8s 集群的 “集群信息” -> "连接信息"， 内容拷贝下来，放到本地的  ~/.kube/config 文件中。 ~/.kube 如果没有手工创建一下。

3.查看有哪些 pod: kubectl --namespace my-ns get pods

4.查看 pod 日志，kubectl --namespace my-ns logs xxxx_pod_name

5.查看 pod 实时日志， kubectl --namespace myns-test logs -f xxxx_pod_name

6.如果没有启动起来，看 pod 的状态   kubectl --namespace myns-test describe pod xxxx_pod_name

7.如果 pod 挂掉重启了， 看挂掉之前上一次容器运行的日志， 加 -p ，这样看： kubectl --namespace myns-test logs -p xxxx_pod_name

8.强制删除 Terminating 状态的 pod:  https://stackoverflow.com/questions/35453792/pods-stuck-in-terminating-status
```
kubectl delete pod --grace-period=0 --force --namespace <NAMESPACE> <PODNAME>
kubectl --kubeconfig=$DATA --namespace xxx get pod | grep Terminating | awk '{print $1}' | xargs -I {} kubectl --kubeconfig=$DATA --namespace xxx delete pod {} --force --grace-period=0
```

9.k8s yaml 中使用 secrets 前创建 secrets.

``` kubectl get secrets -n [your-namespace] ```

Verify that the secret contains the correct credentials. You can describe the secret to see its details:

``` kubectl describe secret my-docker-registry-secret -n [your-namespace] ```

If the secret does not exist or is incorrect, you will need to create or update it. You can create a Docker registry secret using:
```
kubectl create secret docker-registry my-docker-registry-secret \
  --docker-server=xxx-registry.cn-hangzhou.cr.aliyuncs.com \
  --docker-username=[your-username] \
  --docker-password=[your-password] \
  --docker-email=[your-email] \
  -n [your-namespace]
```

10.显示节点上的容器占用的磁盘空间大小
https://stackoverflow.com/questions/62125346/list-container-images-in-kubernetes-cluster-with-size-like-docker-image-ls
以 MB 显示各个 pod 占用的空间：
```
kubectl get nodes  -o json | jq '.items[].status.images[] | .names[1], (.sizeBytes | tonumber/1024/1024)'
```

11.Debug a kubernetes node via shell
https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#node-shell-session

Debugging via a shell on the node
If none of these approaches work, you can find the Node on which the Pod is running and create a Pod running on the Node. To create an interactive shell on a Node using kubectl debug, run:

kubectl debug node/mynode -it --image=ubuntu

The node system will be mounted at /host
