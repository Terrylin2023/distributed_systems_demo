# distributed_systems_demo

## 1. Kafka

```
docker-compose -f '/Users/terrylin/Desktop/2024Winter/DistributedSystem/Project/server/docker-compose.yaml' up
```


## 2. Influxdb
start Influxdb
```
indluxd
```

## 3. Telegraf
```
telegraf --config /Users/terrylin/Desktop/2024Winter/DistributedSystem/Project/server/telegraf.conf
```

## 4. Docker
先打開Docker Desktop，才能順利運行

build
```
docker build -t server_v2 .
```
run
```
docker run --name server1 server_v2
```
