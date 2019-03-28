# exmple REST API with authentication
Hello,This is a mini project about database operation,for example: quiring and saving weather data to database from website, you can use REST API including GET, POST and DELETE methods!

## 6 api

External address: http://35.246.0.64/

/quire --- Quire all users --- GET

/quire/(name) --- Quire user by name --- GET

/add_user --- Add user --- POST

/delete/(deletename) --- Delete user by name --- DELETE

/quireweather --- Get weather information in Datatabase --- GET

/weather --- Get weather information on Internet and save in Database --- GET


## This is a POST and DELETE test sentences:

curl -i -H "Content-Type: application/json" -X POST -d '{"id":"4","name":"Arman","age":"55","password":"909090"}' http://127.0.0.1:5000/add_user

curl -X "DELETE" http://localhost:5000/delete/bobo

## I strengthened my project in 4 ways：

1.For security, I saved the KEY used by the weather API in a separate file instead of in the python code because the api-key is sensitive data and exposed in the code as unsafe.

2.Cache：I use the same data caching techniques to prevent user request many times, this can speed up the request time, if the request data like last time, then put it in the cache of the local environment,  it also can prevent users from too much waste refresh the page to the weather in the use of API interface, on the Internet, some of the API is limited by the use of the interface and the need to charge.

3.in instance/ ，I added the.gitignore file here, because there is sensitive data in this folder, so I did not upload it to github.

4.kubectl scale deployment hello-web --replicas=N , use this command to scaling up my application.


