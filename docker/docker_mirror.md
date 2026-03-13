## 配置 Docker Mirror 仓库

```
sudo tee /etc/docker/daemon.json << 'EOF'
{
    "runtimes": {
        "nvidia": {
            "args": [],
            "path": "nvidia-container-runtime"
        }
    },
    "registry-mirrors": [
        "https://docker.1panel.live",
        "https://hub.rat.dev",
        "https://docker.m.daocloud.io",
        "https://dockerproxy.com"
    ]
}
EOF
```

sudo systemctl restart docker


完成后用 docker info | grep -A5 "Registry Mirrors" 验证是否生效。
