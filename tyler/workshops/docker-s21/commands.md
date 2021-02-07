# Workshop Commands

Below are some of the commands I'll be running during the workshop.
Not much explanation here (I'll be giving that verbally), but this
could be a useful reference if you want to go back and see how I typed
something, precisely.

## Bash Crash Course

```
pwd
ls
ls --help
ls -a
ls -a -w 80
echo hi > example.txt
cat example.txt
nano example.txt
mkdir testdir
cd testdir
cd ..
# sudo reboot
```

## Check Docker

```
sudo chown $USER /var/run/docker.sock 
docker run hello-world
docker help
```

## Trying Linux Distros

```
docker images
docker pull ubuntu
docker pull centos
docker pull alpine
# visit https://hub.docker.com/search
# see versions/tags: https://hub.docker.com/_/ubuntu
docker images
docker run --help

docker run ubuntu echo hi
docker run -it ubuntu bash
apt update
apt install python3
# <CONTROL-D> (or exit)

docker run -it centos bash
yum install python3

docker images
docker run -it alpine bash # should fail
docker run -it alpine sh
```

## Volumes

```
mkdir demo
echo hi > demo/a.txt
echo bye > demo/b.txt
docker run -it -v demo:/demo_inside ubuntu bash
docker run -it -v /home/tyler/demo:/demo_inside ubuntu bash
ls /demo_inside
echo test > /demo_inside/c.txt
exit
ls demo
docker run -it -v /home/tyler/demo:/demo_inside:ro ubuntu bash
echo test2 > /demo_inside/d.txt
```

## Web Server

```
# SLIDES: show IP/port details...
docker run nginx
docker run -p 8080:80 nginx
# in browser: <YOUR VM IP>:8080
docker run -p 8080:80 -v /home/tyler/demo:/usr/share/nginx/html:ro nginx
# in browser: <YOUR VM IP>:8080/a.txt
nano demo/index.html
docker run -p 8080:80 -v /home/tyler/demo:/usr/share/nginx/html:ro nginx
# in browser: <YOUR VM IP>:8080
docker run -d -p 8080:80 -v /home/tyler/demo:/usr/share/nginx/html:ro nginx # daemon mode
# put websites in chat...
docker ps
docker kill <CONTAINER NAME OR ID>
# docker ps -a, docker rm <NAME>, docker rmi -f <NAME>
# docker rm -f $(docker ps -qa)
```

## Database
```
docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=secret mysql

sudo apt install mysql-client
mysql --host=127.0.0.1 --port=3306 --user=root --password=secret
```

```sql
show databases;
create database test;
use test;
show tables;
create table points (x int, y int);
show tables;
insert into points values (1,1);
insert into points values (5,6);
insert into points values (-3,4);
select * from points;
select * from points > 0;
```

## Building Images

```
mkdir img
nano img/Dockerfile
```

Contents:
```
FROM ubuntu
RUN apt update
RUN apt install python3 python3-pip
RUN pip3 install pandas
```

```
docker build img -t pandas
docker images
docker run -it pandas bash
```