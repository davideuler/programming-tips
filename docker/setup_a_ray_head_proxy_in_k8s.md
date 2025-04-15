 ray-head-proxy.yaml, defines Kubernetes resources to set up an Nginx proxy with basic authentication for the Ray head node's dashboard.


```
apiVersion: v1
kind: Secret
metadata:
  name: ray-proxy-auth
type: Opaque
stringData:
  # encrypted password for ray_user:xxxx
  # openssl passwd -apr1 xxxx
  auth: ray_user:xxxx

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: ray-proxy-nginx-conf
data:
  nginx.conf: |
    events {
      worker_connections 1024;
    }
    http {
      server {
        listen 80;
        
        auth_basic "Ray Dashboard";
        auth_basic_user_file /etc/nginx/auth/.htpasswd;

        location / {
          proxy_pass http://raycluster-autoscaler-head-svc:8265;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
        }
      }
    }

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ray-head-proxy
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ray-head-proxy
  template:
    metadata:
      labels:
        app: ray-head-proxy
    spec:
      containers:
      - name: nginx
        image: nginx:1.27-alpine
        ports:
        - containerPort: 80
        resources:
          limits:
            cpu: "2"
            memory: "1G"
          requests:
            cpu: "2"
            memory: "1G"
        volumeMounts:
        - name: nginx-config
          mountPath: /etc/nginx/nginx.conf
          subPath: nginx.conf
        - name: auth-config
          mountPath: /etc/nginx/auth
      volumes:
      - name: nginx-config
        configMap:
          name: ray-proxy-nginx-conf
      - name: auth-config
        secret:
          secretName: ray-proxy-auth
          items:
          - key: auth
            path: .htpasswd
      imagePullSecrets:
        - name: my-docker-registry-secret

---
apiVersion: v1
kind: Service
metadata:
  name: ray-head-proxy
spec:
  type: LoadBalancer  # Change to NodePort or ClusterIP based on your needs
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
  selector:
    app: ray-head-proxy
```
