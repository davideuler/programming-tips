
## Run an ozone node in docker

```
docker run -p 9878:9878 apache/ozone
```

Run 3 datanode ozone:

```
cd compose/ozone
docker-compose up -d --scale datanode=3
```

## Build ozone on JDK 17 (

Pass MAVEN_OPTS to maven, to avoid the error of: 
Failed to execute goal org.codehaus.mojo:exec-maven-plugin:1.3.1:java  java.lang.ClassFormatError accessible: module java.base does not "opens java.lang" to unnamed module ...

```
export MAVEN_OPTS="--add-opens jdk.naming.rmi/com.sun.jndi.rmi.registry=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED  --add-opens java.base/sun.security.action=ALL-UNNAMED --add-opens java.base/sun.net=ALL-UNNAMED"
mvn clean package -DskipTests
```

## aws client for ozone

```
 apt install awscli
 aws configure  ## input any none empty key and id
 aws s3api --endpoint http://localhost:9878/ create-bucket --bucket=bucket1
 aws s3api --endpoint http://localhost:9878/ create-bucket --bucket=wordcount
 aws s3 --endpoint http://localhost:9878 cp --storage-class REDUCED_REDUNDANCY  /tmp/testfile  s3://wordcount/testfile
 aws s3 --endpoint http://localhost:9878 ls  s3://wordcount/testfile
```

 Create alias command
```
alias ozones3api='aws s3api --endpoint http://localhost:9878'
```

Create bucket:
```
$ ozones3api create-bucket --bucket documents
```

Put objects to bucket:
```
$ ozones3api put-object --storage-class REDUCED_REDUNDANCY  --bucket documents --key S3Doc --body ./S3.md
$ ozones3api put-object --storage-class REDUCED_REDUNDANCY  --bucket documents --key hddsDoc --body ./Hdds.md
$ ozones3api put-object --storage-class REDUCED_REDUNDANCY --bucket documents --key javaDoc --body ./JavaApi.md
```

Note: The REDUCED_REDUNDANCY option is set for single node service:
 --storage-class REDUCED_REDUNDANCY 

List objects in a bucket:

```
$ ozones3api list-objects --bucket documents
```
{"Contents": [{"LastModified": "2018-11-02T21:57:40.875Z","ETag": "1541195860875","StorageClass": "STANDARD","Key": "hddsDoc","Size": 2845},{"LastModified": "2018-11-02T22:36:23.358Z","ETag": "1541198183358","StorageClass": "STANDARD","Key": "javaDoc","Size": 5615},{"LastModified": "2018-11-02T21:56:47.370Z","ETag": "1541195807370","StorageClass": "STANDARD","Key": "s3doc","Size": 1780}]}
Get Object from a Bucket:

```
$ ozones3api get-object --bucket documents --key hddsDoc /tmp/hddsDoc
```
{"ContentType": "application/octet-stream","ContentLength": 2845,"Expires": "Fri, 02 Nov 2018 22:39:00 GMT","CacheControl": "no-cache","Metadata": {}}
Head Bucket:

```
$ ozones3api head-bucket --bucket documents
```

Head Object:
```
$ ozones3api head-object --bucket documents --key hddsDoc
```

Delete Object:

We have 2 ways to delete.

* Delete one object at a time
* Delete multiple objects at a time.

Ozone over S3 supports both of them.

Delete Object:
```
$ ozones3api delete-object --bucket documents --key hddsDoc
```

Multi Delete:
```
$ ozones3api delete-objects --bucket documents --delete 'Objects=[{Key=javaDoc},{Key=s3Doc}]'
```
{"Deleted": [{"Key": "javaDoc"},{"Key": "s3Doc"}]}
