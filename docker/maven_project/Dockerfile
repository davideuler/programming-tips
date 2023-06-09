# docker build -t myproject-service:202303 -f Dockerfile .
# docker tag myproject-service:202303 registry.xxx.com/mynamesapce/myproject-service:2023060902

# Compilation phase builder
FROM registry.xxx.com/myproject/myproject-maven:3.8.4-jdk-17 as builder  
  
WORKDIR /data/myproject-service  
COPY . .  
  
RUN mvn -Dmaven.test.skip clean package  
  
# Image building phase, based on openjdk 17
FROM openjdk:17-alpine

RUN apk --no-cache add curl tzdata

# 从编译阶段的中拷贝编译结果到当前镜像中  
COPY --from=builder /data/myproject-service/myproject-service-start/target/myproject-service.jar /home/admin/myproject-service/target/  
  
ENV envLabel="dev" APP_NAME="myproject-service" packageName="com.myorg" log.dir="/home/admin/myproject-service/logs/"  
ENV TZ=Asia/Shanghai

EXPOSE 7070  
WORKDIR /home/admin/myproject-service/  

CMD ["java", "-jar", "/home/admin/myproject-service/target/myproject-service.jar"]
