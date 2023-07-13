
# copy files from k8s container

```
kubectl --kubeconfig=$K8S_DEV --namespace myspace cp  db/debug-12345-3gdcx:/data/script.sh ./script.sh
```

# Check service role permission

kubectl auth can-i <verb> <resource> --as=system:serviceaccount:<namespace>:<serviceaccountname> [-n <namespace>]

```
alias k=kubectl
k auth can-i create job -n=ihopeit-ns --as=system:serviceaccount:ihopeit-ns:default-shared-sa
yes
```

https://stackoverflow.com/questions/54889458/kubernetes-check-serviceaccount-permissions

# Create a service account node-apis, and define role bindings

```
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: node-apis
---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: node-apis
rules:
  - apiGroups:
      - ""
      - "apps"
      - "batch"
    resources:
      - endpoints
      - deployments
      - pods
      - jobs
    verbs:
      - get
      - list
      - watch
      - create
      - delete
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: node-apis
  namespace: default
subjects:
  - kind: ServiceAccount
    name: node-apis
    namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: node-apis
```

Then can use the service account by specifying it in the spec section of the pod.
```
spec:
  serviceAccountName: node-apis
  containers:
  ...
```
https://stackoverflow.com/questions/65527852/jobs-batch-is-forbidden-user-systemserviceaccountdefaultdefault-cannot

# Kubernetes: Get ServiceAccount Permissions/Roles
https://www.shellhacks.com/kubernetes-get-serviceaccount-permissions-roles/

Service Accounts are not User Accounts: User accounts are used by humans e.g. administrators or developers, to access a Kubernetes cluster to do some development work or maintenance. While Service Accounts are used by in-cluster Kubernetes entities, such as Pods, to authenticate to the Kubernetes API server or external services.

Run one of these commands to list the Service Accounts in a K8s cluster:

$ kubectl get serviceaccounts # In the current Namespace
$ kubectl get serviceaccounts --namespace=<nameSpaceName> # In the specific Namespace
$ kubectl get serviceaccounts --all-namespaces # In the all Namespaces
Like with any other Kubernetes resources you can get more details about your Service Account as follows:

$ kubectl describe sa <ServiceAccountName>
Get ServiceAccount Roles & Permissions
Kubernetes supports different authorization modes.
Let’s assume that your cluster uses Role-Based Access Control (RBAC) way of granting users access to Kubernetes API resources (this can be check by running the kubectl api-versions command).

In RBAC mode, Roles and ClusterRoles define the actions a user can perform within a namespace or cluster, respectively.

You can show the Roles and CluserRoles with the associated Service Accounts by running the following command:

$ kubectl get rolebindings,clusterrolebindings --all-namespaces -o wide
To get a more pretty output you can execute the following one-liner (spitted over multiple lines for better readability):

$ kubectl get rolebinding,clusterrolebinding \
              --all-namespaces \
              -o jsonpath='{range .items[?(@.subjects[0].name=="<ServiceAccountName>")]}
                           [{.roleRef.kind},{.roleRef.name}]{end}'; echo
- sample output -
[Role,<roleName>][ClusterRole,<clusterRoleName>]
Alternatively you can generate a compact role mapping table and grep for the name of your Service Account as follows:

$ kubectl get rolebinding,clusterrolebinding \
              --all-namespaces \
              -o custom-columns='KIND:kind,
                                 NAMESPACE:metadata.namespace,
                                 NAME:metadata.name,
                                 SERVICE_ACCOUNTS:subjects[?(@.kind=="ServiceAccount")].name' |\
              { head -1; grep "<ServiceAccountName>"; }
- sample output -
KIND                 NAMESPACE  NAME               SERVICE_ACCOUNT
RoleBinding          default    <roleName>         <serviceAccountName>
ClusterRoleBuinding  <none>     <clusterRoleName>  <serviceAccountName>
Once you have found the Roles associated with your Service Account, you can display the permissions by running the following command:

$ kubectl describe role <RoleName>
- sample output -
Name:         <roleName>
Labels:       <none>
Annotations:  <none>
PolicyRule:
  Resources  Non-Resource URLs  Resource Names  Verbs
  ---------  -----------------  --------------  -----
  pods/exec  []                 []              [create delete get list patch update watch]
  pods       []                 []              [create delete get list patch update watch]
  events     []                 []              [get list watch]
  pod/log    []                 []              [get list watch]
