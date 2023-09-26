# Controller, Operator, and CRD (Custom Resource Definition) in kubernetes

## What is Controller in k8s?

https://kubernetes.io/docs/concepts/architecture/controller/

In robotics and automation, a control loop is a non-terminating loop that regulates the state of a system.
In Kubernetes, controllers are control loops that watch the state of your cluster, then make or request changes where needed. Each controller tries to move the current cluster state closer to the desired state.

### Controller pattern
A controller tracks at least one Kubernetes resource type. These objects have a spec field that represents the desired state. The controller(s) for that resource are responsible for making the current state come closer to that desired state.

The controller might carry the action out itself; more commonly, in Kubernetes, a controller will send messages to the API server that have useful side effects. 


## What is Operator in k8s?

Operators are software extensions to Kubernetes that make use of custom resources to manage applications and their components. Operators follow Kubernetes principles, notably the control loop.

https://kubernetes.io/docs/concepts/extend-kubernetes/operator/

Kubernetes' operator pattern concept lets you extend the cluster's behaviour without modifying the code of Kubernetes itself by linking controllers to one or more custom resources. 
Operators are clients of the Kubernetes API that act as controllers for a Custom Resource.

### Using an operator
Once you have an operator deployed, you'd use it by adding, modifying or deleting the kind of resource that the operator uses. Following the above example, you would set up a Deployment for the operator itself, and then:

```
kubectl get SampleDB                   # find configured databases

kubectl edit SampleDB/example-database # manually change some settings
```

## What is CRD?

https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
