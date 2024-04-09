# Data engeeering SSD project

## Objective

Store all data into a mysql db for a better browse of the csv file

once everything is loaded , another part of the program will create unified table for the data

## Mysql docker run command

```bash
docker run --name mysql -e MYSQL_ROOT_PASSWORD=root -d -p 3306:3306 mysql:5.7
```
