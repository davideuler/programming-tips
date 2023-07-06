[How to restart k8s pods/deployment](https://spacelift.io/blog/restart-kubernetes-pods-with-kubectl)

A pod is the smallest unit in Kubernetes (K8S). They should run until they are replaced by a new deployment. Because of this, there is no way to restart a pod, instead, it should be replaced.

There is no `kubectl restart [podname]` command for use with K8S (with [Docker](https://spacelift.io/blog/docker-tutorial) you can use `docker restart [container_id]` ), so there are a few different ways to achieve a pod ‘restart’ with `kubectl`.

## Why You Might Want to Restart a Pod[](https://spacelift.io/blog/restart-kubernetes-pods-with-kubectl#why-you-might-want-to-restart-a-pod)

There are many situations in which you may need to restart a pod:

- **Applying configuration changes** → If there are updates on the pod’s configuration (configmaps, secrets, environment variables), in some cases, you may need to manually restart the pod for the changes to take effect. 
- **Debugging applications** → Sometimes, if your application is not running correctly, or you are just experiencing some issues with it, a good practice is to first restart the underlying pods to reset their state and make troubleshooting easier.
- **Pod stuck in a terminating state** → In this case, usually, a delete and a recreation would do the trick in most of the cases. However, there are some cases where a node is taken out of service, and the pods cannot be evicted from it, in which a restart will help with addressing the issue.
- **OOM** → If a pod is terminated with an Out Of Memory Error (OOM), you will need to restart the pod after making changes to the resource specifications. This may be solved automatically if the pod’s restart policy allows it.
- **Forcing a new image pull** → To ensure a pod is using the latest version of an image, if you are using the latest tag (which is not a best practice), you need to manually restart the pod to force a new image pull. Of course, if you are making changes to the image parameter in the configuration because you’ve released a new image and you want to take advantage of that, a restart will still be required.
- **Resource contention** → If a pod is consuming excessive resources, causing performance issues, or affecting other workflows, restarting the pod may release those resources and mitigate the problem. This usually occurs when you are not using memory and CPU restrictions.

## Pod Status[](https://spacelift.io/blog/restart-kubernetes-pods-with-kubectl#pod-status)

A pod has five possible statuses:

1. **Pending:** This state shows at least one container within the pod has not yet been created.
2. **Running:** All containers have been created, and the pod has been bound to a Node. At this point, the containers are running, or are being started or restarted.
3. **Succeeded:** All containers in the pod have been successfully terminated and will not be restarted.
4. **Failed:** All containers have been terminated, and at least one container has failed. The failed container exists in a non-zero state.
5. **Unknown:** The status of the pod cannot be obtained.

If you notice a pod in an undesirable state where the status is showing as ‘error’, you might try a ‘restart’ as part of your troubleshooting to get things back to normal operations. You may also see the status ‘[CrashLoopBackOff](https://spacelift.io/blog/crashloopbackoff)’, which the default when an error is encountered, and K8S trys to restart the pod automatically.

## Restart a pod[](https://spacelift.io/blog/restart-kubernetes-pods-with-kubectl#restart-a-pod)

You can use the following methods to ‘restart’ a pod with `kubectl`. Once new pods are re-created they will have a different name than the old ones. A list of pods can be obtained using the `kubectl get pods` command.

### Method 1

`kubectl rollout restart`

This method is the recommended first port of call as it will not introduce downtime as pods will be functioning. A rollout restart will kill one pod at a time, then new pods will be scaled up. This method can be used as of K8S v1.15.

`kubectl rollout restart deployment <deployment_name> -n <namespace>`

### Method 2

`kubectl scale`

This method will introduce an outage and is not recommended. If downtime is not an issue, this method can be used as it can be a quicker alternative to the `kubectl rollout restart method` (your pod may have to run through a lengthy Continuous Integration / Continuous Deployment Process before it is redeployed).

If there is no YAML file associated with the deployment, you can set the number of replicas to 0.

`kubectl scale deployment <deployment name> -n <namespace> --replicas=0`

This terminates the pods. Once scaling is complete the replicas can be scaled back up as needed (to at least 1):

`kubectl scale deployment <deployment name> -n <namespace> --replicas=3`

Pod status can be checked during the scaling using:

`kubectl get pods -n <namespace>`

### Method 3

`[kubectl delete pod](https://spacelift.io/blog/kubectl-delete-pod) and kubectl delete replicaset`

Each pod can be deleted individually if required:

`kubectl delete pod <pod_name> -n <namespace>`

Doing this will cause the pod to be recreated because K8S is declarative, it will create a new pod based on the specified configuration.

However, where lots of pods are running this is not really a practical approach. Where lots of pods have the same label however, you could use that to select multiple pods at once:

`kubectl delete pod -l “app:myapp” -n <namespace>`

Another approach if there are lots of pods, then ReplicaSet can be deleted instead:

`kubectl delete replicaset <name> -n <namespace>`

### Method 4

`kubectl get pod | kubectl replace`

The pod to be replaced can be retrieved using the `kubectl get pod` to get the YAML statement of the currently running pod and pass it to the `kubectl replace` command with the `--force` flag specified in order to achieve a restart. This is useful if there is no YAML file available and the pod is started.

`kubectl get pod <pod_name> -n <namespace> -o yaml | kubectl replace --force -f -`

### Method 5

`kubectl set env`

Setting or changing an environment variable associated with the pod will cause it to restart to take the change. The example below sets the environment variable `DEPLOY_DATE` to the date specified, causing the pod to restart.

`kubectl set env deployment <deployment name> -n <namespace> DEPLOY_DATE="$(date)"`
