[![Build Status](https://travis-ci.org/a0919610611/Library.svg?branch=master)](https://travis-ci.org/a0919610611/Library)
[![Coverage Status](https://coveralls.io/repos/github/a0919610611/Library/badge.svg?branch=master)](https://coveralls.io/github/a0919610611/Library?branch=master)
# Library
BackEnd for library borrow system for Software Development Pratice

[FrontEnd](https://github.com/calee0219/SDP-Library-System) Build By calee0219

Full documention for the project is [docs](https://a0919610611.github.io/Library/).
#Technology Stack
Python3
 [Django](https://www.djangoproject.com/
)  
[Django Rest Framework] (http://www.django-rest-framework.org/)   
Django Rest Swagger  
mkdocs

#Database
Sqlite in Development
MariaDB in Production

#How To Run

##Manually
```
sudo pip3 install -r requirments.txt
./init.sh
./manage.py runserver (defualt is 127.0.0.1:8000)
```
##Docker
```
docker build . -t library
dokcer run -d -p 8080:8080 library

Open Browser And Go localhost:8080
```
