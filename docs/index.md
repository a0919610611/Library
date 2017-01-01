# Test EndPoint
Go to root url , and you test api using html form (powered by django rest swaggers),but  
some endpoints just can only using json format(using curl or Postman to test).

#User Login Work Flow
Login (username & password) -> Get JWT (JSON Web Token)

#About JWT
Expiration Time : 1 day 
Refresh Expiration Time : 30 days

Refresh token everyday and login again every month ( for user experience)  


#Using JWT To Authorization
In Header:set Authorization : JWT {Your Token} 