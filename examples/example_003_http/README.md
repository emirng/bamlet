# Example 003 HTTP

This show how one could use bamlet to write an HTTP-server.

## How to run HTTP-server
Run this from projects root folder
```
$ python -m examples.example_003_http
```

Expected output
```
 * Serving bamlet app
 * Running on localhost:8080
 ```
## How to render the web page
Use a web client and  goto http://localhost:8080

![image](https://github.com/emirng/bamlet/assets/135670768/cca6a928-cee9-4a0b-9cff-9d2614e7b2b0)

Test click links to see different resources and different content-types. You can also test trigger a 404 by enter an invalid resource directly to the URL. It also checks for 405, try to trigger that as well.
