路由表接口： http://127.0.0.1:8000/controller/rib

生成拓扑接口：http://127.0.0.1:8000/controller/genTopo
```
{
    "code": 200,
    "order": null,
    "data": [
        {
            "deviceId": "1",
            "srcIP": "10.0.8.0/24",
            "dstIP": "10.0.4.0/24",
            "next_hop": "10.0.4.0",
            "inInterface": 1,
            "outInterface": 2
        },
        {
            "deviceId": "2",
            "srcIP": "10.0.4.0/24",
            "dstIP": "10.0.3.0/24",
            "next_hop": "10.0.3.0",
            "inInterface": 2,
            "outInterface": 1
        },
        {
            "deviceId": "3",
            "srcIP": "10.0.3.0/24",
            "dstIP": "10.0.1.0/24",
            "next_hop": "10.0.1.0",
            "inInterface": 1,
            "outInterface": 2
        },
        {
            "deviceId": "4",
            "srcIP": "10.0.1.0/24",
            "dstIP": "\"\"",
            "next_hop": "\"\"",
            "inInterface": 1,
            "outInterface": 2
        }
    ]
}
```
下发转发表接口：http://127.0.0.1:8000/controller/fib
```
{
    "code": 200,
    "order": null,
    "data": [
        {
            "deciceID": 1,
            "dstIP": "10.0.4.0/24",
            "outInterfaceId": 2
        },
        {
            "deciceID": 2,
            "dstIP": "10.0.3.0/24",
            "outInterfaceId": 1
        },
        {
            "deciceID": 3,
            "dstIP": "10.0.1.0/24",
            "outInterfaceId": 2
        }
    ]
}
```
下发验证表接口：http://127.0.0.1:8000/controller/verifyTable
```
{
    "code": 200,
    "order": null,
    "data": [
        {
            "deciceID": 1,
            "srcIP": "10.0.8.0/24",
            "inInterface": 1
        },
        {
            "deciceID": 2,
            "srcIP": "10.0.4.0/24",
            "inInterface": 2
        },
        {
            "deciceID": 3,
            "srcIP": "10.0.3.0/24",
            "inInterface": 1
        }
    ]
}
```
获取拓扑链路信息接口：http://127.0.0.1:8000/controller/topoLink
```
{
    "code": 200,
    "order": null,
    "data": [
        {
            "deviceID": "1",
            "link_performance": {
                "延时": "74ms",
                "丢包": "3.00%",
                "带宽": "645Mbps"
            }
        },
        {
            "deviceID": "2",
            "link_performance": {
                "延时": "69ms",
                "丢包": "0.34%",
                "带宽": "71Mbps"
            }
        },
        {
            "deviceID": "3",
            "link_performance": {
                "延时": "41ms",
                "丢包": "3.03%",
                "带宽": "282Mbps"
            }
        },
        {
            "deviceID": "4",
            "link_performance": {
                "延时": "98ms",
                "丢包": "2.25%",
                "带宽": "71Mbps"
            }
        }
    ]
}
```
获取全部节点主机信息接口：http://127.0.0.1:8000/controller/topoNode
```
{
    "code": 200,
    "order": null,
    "data": [
        {
            "deviceID": "1",
            "node_performance": {
                "cpu": "62.72%",
                "内存": "25.45%",
                "温度": "26°C"
            }
        },
        {
            "deviceID": "2",
            "node_performance": {
                "cpu": "56.68%",
                "内存": "12.27%",
                "温度": "42°C"
            }
        },
        {
            "deviceID": "3",
            "node_performance": {
                "cpu": "10.38%",
                "内存": "41.43%",
                "温度": "21°C"
            }
        }
    ]
}