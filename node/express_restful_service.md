# Implementation of a simple express restful service

https://expressjs.com/en/starter/hello-world.html

```

import express from "express";
const app = express();

app.use(express.json());

app.get('/', (req, res) => {
    res.send('Hello from express and typescript');
});

app.post(`/msg`, async (req, res) => {
    console.log('request =' + JSON.stringify(req.body))
    const { username, email, password } = req.body

    console.log(`username: ${username}, email:${email}`);

    const result = {
        content:"this is the content",
        username:username
    }
    res.json(result)
  })

const port = process.env.PORT || 3000;

app.listen(port, () => console.log(`App listening on PORT ${port}`));

```

Start the service:
```
npx tsx index.ts
```

Can test the service by:
curl -X POST http://localhost:3000/msg -H 'Content-Type: application/json' -d '{"username":"david","email":"xxxx@yyyy.com", "password":"xxxx"}'
