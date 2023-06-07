
## Reference
* Swagger3.0: https://blog.csdn.net/m0_59562547/article/details/118933734
* Swagger 3.0 editor: https://editor.swagger.io/
* Get started: https://swagger.io/tools/open-source/getting-started/

## Different ways to swagger: 
* server code -> yaml -> api doc & client code
* yaml api definition -> server code/ client code / api doc


## Maven plugin to generate java client code, and java controller code, from swagger yaml (Open API 3.x)

```
    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <client.base.package.name>com.mycorp.api</client.base.package.name>

    </properties>

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
            <version>2.2.10</version>
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

        <dependency>
            <groupId>org.openapitools</groupId>
            <artifactId>jackson-databind-nullable</artifactId>
            <version>0.2.1</version>
        </dependency>


        <!-- for package javax.validation -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.data</groupId>
            <artifactId>spring-data-jpa</artifactId>
        </dependency>

    </dependencies>

    <build>
        <plugins>

            <plugin>
                <groupId>org.openapitools</groupId>
                <artifactId>openapi-generator-maven-plugin</artifactId>
                <version>6.6.0</version>
                <executions>
                    <execution>
                        <goals>
                            <goal>generate</goal>
                        </goals>
                        <configuration>
                            <inputSpec>
                                ${project.basedir}/src/main/resources/openapi.yaml
                            </inputSpec>
                            <generatorName>spring</generatorName>
                            <apiPackage>com.mycorp.openapi.api</apiPackage>
                            <modelPackage>com.mycorp.openapi.model</modelPackage>
                            <supportingFilesToGenerate>
                                ApiUtil.java
                            </supportingFilesToGenerate>
                            <configOptions>
                                <delegatePattern>true</delegatePattern>
                            </configOptions>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
```

```

```

## Configuration to server api docs through swagger-ui

```
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-boot-starter</artifactId>
            <version>3.0.0</version>
        </dependency>

        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger2</artifactId>
            <version>3.0.0</version>
        </dependency>
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger-ui</artifactId>
            <version>3.0.0</version>
        </dependency>
```

Swagger3Config.java

```
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import springfox.documentation.builders.ApiInfoBuilder;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.oas.annotations.EnableOpenApi;
import springfox.documentation.service.Contact;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;

//import java.util.function.Predicate;

@Configuration
@EnableOpenApi // 开启SWAGGER3.0
public class Swagger3Config implements WebMvcConfigurer {

    @Bean
    Docket docket() {
        //DocumentationType.OAS_30,原Swagger2选择DocumentationType.SWAGGER_2
        return new Docket(DocumentationType.OAS_30)
            .select()
            //通过apis方法配置要扫描的controller的位置
            .apis(RequestHandlerSelectors.basePackage("com.mycorp.openapi"))
            //通过paths方法配置路径
            .paths(PathSelectors.any())
            //设置需要排除的路径(如果需要)
            //.paths(Predicate.not(PathSelectors.regex("/error.*")))
            .build().apiInfo(new ApiInfoBuilder()
                //设置文档标题
                .description("Swagger3测试API接口文档")
                //设置联系人信息
                .contact(new Contact("API作者", "https://www.mycorp.com", "admin@mycorp.com"))
                //设置版本号
                .version("1.1")
                //设置文档抬头
                .title("API测试文档")
                //设置授权
                .license("License By MyCorp")
                //设置授权访问网址
                .licenseUrl("https://mycorp.com")
                .build());
    }

    @Override
    //swagger-ui/index.html在META-INF/resources下面,添加资源映射确保URL能够访问
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/swagger-ui/**").addResourceLocations(
                "classpath:/META-INF/resources/webjars/springfox-swagger-ui/")
            .resourceChain(false);
    }
}
```


application.yaml

```
server:
  port: 7001
  
spring:
  mvc:
    pathmatch:
      matching-strategy: ant_path_matcher
```

Then can access the api docs after springboot application started.

```
http://localhost:7001/swagger-ui/index.html
```

## Define Pagination API

```
  /task/list:
    get:
      tags:
        - task
      summary: list tasks
      description: list tasks by condition, with pagination
      operationId: listTasks
      parameters:
        - name: keyword
          in: query
          description: keyword
          required: false
          explode: true
          schema:
            type: string
        - $ref: '#/components/parameters/startToken'
        - $ref: '#/components/parameters/pageSize'
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginationResponse'
                  - properties:
                      devices:
                        type: array
                        items:
                          $ref: '#/components/schemas/Task'
            application/xml:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginationResponse'
                  - properties:
                      devices:
                        type: array
                        items:
                          $ref: '#/components/schemas/Task'
        '400':
          description: Invalid query condition
      security:
        - petstore_auth:
            - write:tasks
            - read:tasks

components:
  schemas:
    PaginationResponse:
      type: object
      properties:
        nextToken:
          type: string
        hasNext:
          type: boolean
      xml:
        name: PaginationResponseData
  parameters:
    pageSize:
      name: pagesize
      in: query
      description: Number of records to return
      schema:
        type: integer
    startToken:
      name: starttoken
      in: query
      description: Start token for paging
      schema:
        type: string
```

You don't need to write code for Model, API, Controller, just implement XxxApiDelegate, then the restful service is ready to go.


~~## Maven plugin to generate java code from swagger yaml (Open API 3.x)~~
Assume api definition file path: src/main/resources/openapi.yaml

The following configuration helps to generate model definitions for the API.

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

And then compile, package the application.

```
mvn compile
mvn package
```
