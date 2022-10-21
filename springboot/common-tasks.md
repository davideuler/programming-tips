## How to start a specified class in springboot jar?

I don't want to start the default Spring Application, but would like to run another class which has a main() method.
I can start  spring PropertiesLauncher with loader.main to my entry class which has a main method.

```
java -cp ./myweb-start/target/myweb-start-1.0-SNAPSHOT.jar -Dloader.main=com.my.server.DemoClient org.springframework.boot.loader.PropertiesLauncher
```
