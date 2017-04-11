servers = ["server1", "server2", "server3", "server4"]

users = [{
  "uid": 1,
  "name": "user1",
  "server": "server1"
}, {
  "uid": 2,
  "name": "user2",
  "server": "server2"
}, {
  "uid": 3,
  "name": "user3",
  "server": "server3"
}, {
  "uid": 4,
  "name": "user4",
  "server": "server4"
}]

ssamples = [
# server 1
{
  "name": "server1",
  "timestamp": "2017-04-08 14:10:00",
  "cpu": 10,
  "ram": 30,
  "ram_available": 220,
  "ram_cached": 230,
  "disk_in": 1400000000,
  "disk_out": 810000000
},

# server 2
{
  "name": "server2",
  "timestamp": "2017-04-08 14:10:00",
  "cpu": 7,
  "ram": 30,
  "ram_available": 220,
  "ram_cached": 230,
  "disk_in": 1550000000,
  "disk_out": 810000000
}, {
  "name": "server2",
  "timestamp": "2017-04-08 14:09:00",
  "cpu": 7,
  "ram": 30,
  "ram_available": 220,
  "ram_cached": 220,
  "disk_in": 1300000000,
  "disk_out": 810000000
}, {
  "name": "server2",
  "timestamp": "2017-04-08 14:04:00",
  "cpu": 7,
  "ram": 30,
  "ram_available": 220,
  "ram_cached": 240,
  "disk_in": 1600000000,
  "disk_out": 810000000
},

# server 3
{
  "name": "server3",
  "timestamp": "2017-04-08 14:10:00",
  "cpu": 50,
  "ram": 30,
  "ram_available": 220,
  "ram_cached": 230,
  "disk_in": 1550000000,
  "disk_out": 810000000
}, {
  "name": "server3",
  "timestamp": "2017-04-08 14:09:00",
  "cpu": 10,
  "ram": 30,
  "ram_available": 220,
  "ram_cached": 230,
  "disk_in": 1400000000,
  "disk_out": 810000000
}, {
  "name": "server3",
  "timestamp": "2017-04-08 14:04:00",
  "cpu": 10,
  "ram": 30,
  "ram_available": 220,
  "ram_cached": 240,
  "disk_in": 1600000000,
  "disk_out": 810000000
},

# server 4
{
  "name": "server4",
  "timestamp": "2017-04-08 14:10:00",
  "cpu": 50,
  "ram": 30,
  "ram_available": 220,
  "ram_cached": 230,
  "disk_in": 1550000000,
  "disk_out": 810000000
}, {
  "name": "server4",
  "timestamp": "2017-04-08 14:09:00",
  "cpu": 10,
  "ram": 30,
  "ram_available": 220,
  "ram_cached": 230,
  "disk_in": 1400000000,
  "disk_out": 810000000
}, {
  "name": "server4",
  "timestamp": "2017-04-08 14:04:00",
  "cpu": 10,
  "ram": 30,
  "ram_available": 220,
  "ram_cached": 240,
  "disk_in": 1600000000,
  "disk_out": 810000000
}]

random_ssamples = {
  "timestamps": [
    "2017-04-08 14:01:00", "2017-04-08 14:02:00", "2017-04-08 14:03:00",
    "2017-04-08 14:05:00", "2017-04-08 14:06:00",
    "2017-04-08 14:07:00", "2017-04-08 14:08:00",
  ],
  "cpu": {"from": 2, "to": 9},
  "ram": {"from": 10, "to": 25},
  "ram_available": {"from": 150, "to": 220},
  "ram_cached": {"from": 150, "to": 220},
  "disk_in": {"from": 1400000000, "to": 1500000000},
  "disk_out": {"from": 800000000, "to": 820000000}
}

predictions = [{
  "uid": 1,
  "user_name": "user1",
  "last_used_server": "server1",
  "last_login": "2017-04-08 14:05:00",
  "avg_cpu": 15,
  "max_cpu": 20,
  "avg_ram": 20,
  "max_ram": 30
}, {
  "uid": 2,
  "user_name": "user2",
  "last_used_server": "server2",
  "last_login": "2017-04-08 14:05:00",
  "avg_cpu": 20,
  "max_cpu": 20,
  "avg_ram": 20,
  "max_ram": 30
}, {
  "uid": 3,
  "user_name": "user3",
  "last_used_server": "server3",
  "last_login": "2017-04-08 14:05:00",
  "avg_cpu": 60,
  "max_cpu": 20,
  "avg_ram": 20,
  "max_ram": 30
}, {
  "uid": 4,
  "user_name": "user4",
  "last_used_server": "server4",
  "last_login": "2017-04-08 14:05:00",
  "avg_cpu": 25,
  "max_cpu": 20,
  "avg_ram": 20,
  "max_ram": 30
}]

results = {
  "user_not_exist": "server1",
  "user_exist_cache_false": "server1",
  "user_exist_cache_true_availableCPU_false": "server1",
  "user_exist_cache_true_availableCPU_true": "server4"
}
