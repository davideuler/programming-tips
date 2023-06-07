
## Reference
* Swagger3.0: https://blog.csdn.net/m0_59562547/article/details/118933734
* Swagger 3.0 editor: https://editor.swagger.io/
* Get started: https://swagger.io/tools/open-source/getting-started/

## Different ways to swagger: 
* server code -> yaml -> api doc & client code
* yaml api definition -> server code/ client code / api doc


## Maven plugin to generate java code from swagger yaml (Open API 3.x)
Assume api definition file path: src/main/resources/openapi.yaml

```
<properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <client.base.package.name>com.mycorp.api</client.base.package.name>
</properties>
```

```
    <dependencies>
        <!-- Required for Java 9 and later -->
        <dependency>
            <groupId>javax.annotation</groupId>
            <artifactId>javax.annotation-api</artifactId>
            <version>1.3.2</version>
        </dependency>
        <dependency>
            <groupId>io.swagger.core.v3</groupId>
            <artifactId>swagger-annotations</artifactId>
            <version>2.0.8</version>
        </dependency>

        <dependency>
            <groupId>com.github.joschi.jackson</groupId>
            <artifactId>jackson-datatype-threetenbp</artifactId>
            <version>2.6.4</version>
        </dependency>

        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>5.1.10.RELEASE</version>
        </dependency>
        <!-- HTTP client: Spring RestTemplate -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-web</artifactId>
            <version>5.1.10.RELEASE</version>
        </dependency>
        <!-- JSON processing: jackson -->
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-core</artifactId>
            <version>2.9.9</version>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-annotations</artifactId>
            <version>2.9.0</version>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>2.9.9.3</version>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.jaxrs</groupId>
            <artifactId>jackson-jaxrs-json-provider</artifactId>
            <version>2.9.9</version>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.datatype</groupId>
            <artifactId>jackson-datatype-jsr310</artifactId>
            <version>2.9.9</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>

            <plugin>
                <!-- This 2019 version is required for OpenAPI 3 -->
                <groupId>io.swagger.codegen.v3</groupId>
                <artifactId>swagger-codegen-maven-plugin</artifactId>
                <version>3.0.41</version>

                <executions>
                    <execution>
                        <goals>
                            <goal>generate</goal>
                        </goals>
                        <configuration>
                            <inputSpec>${project.basedir}/src/main/resources/openapi.yaml</inputSpec>
                            <language>java</language>
                            <modelPackage>${client.base.package.name}.model</modelPackage>
                            <apiPackage>${client.base.package.name}.api</apiPackage>
                            <invokerPackage>${client.base.package.name}.invoker</invokerPackage>

                            <configOptions>
                                <groupId>${project.groupId}</groupId>
                                <artifactId>${project.artifactId}</artifactId>
                                <artifactVersion>${project.version}</artifactVersion>
                                <sourceFolder>src/gen/java/main</sourceFolder>
                                <library>resttemplate</library>
                                <licenseName>Apache 2.0</licenseName>
                                <licenseUrl>https://www.apache.org/licenses/LICENSE-2.0</licenseUrl>
                            </configOptions>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
```

然后
