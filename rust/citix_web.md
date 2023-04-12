
1.Got this error "actix web Cannot drop a runtime in a context where blocking is not allowed. This happens when a runtime is dropped from within an asynchronous context."

It is caused by calling blocking code in async method.

```
let mut response = reqwest::blocking::get(url).expect("Error Get Page content");
```

Fixed method: Change the blocking code to async code.

```
let response = reqwest::get(url).await.unwrap();

    let content_type = response.headers().get(CONTENT_TYPE).and_then(|h| h.to_str().ok());

    if let Some(content_type) = content_type {
        if content_type.contains("text/html") {
            // URL is an HTML page
            //let html_content = response.text().await.unwrap();
            let content = response.bytes().await.unwrap();
```
