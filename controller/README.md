路由表接口： http://127.0.0.1:8000/controller/rib

生成拓扑接口：http://127.0.0.1:8000/controller/genTopo
```
{
    "code": 200,
    "order": null,
    "data": {
        "10.0.8.0/24": [
            {
                "next_hop": "10.0.4.0/24",
                "dstIP": "10.0.4.0/24",
                "interface": "In:1 Out:2"
            }
        ],
        "10.0.4.0/24": [
            {
                "next_hop": "10.0.3.0/24",
                "dstIP": "10.0.3.0/24",
                "interface": "In:2 Out:1"
            }
        ],
        "10.0.3.0/24": [
            {
                "next_hop": "10.0.1.0/24",
                "dstIP": "10.0.1.0/24",
                "interface": "In:1 Out:2"
            }
        ],
        "10.0.1.0/24": [
            {
                "next_hop": "10.0.9.0/24",
                "dstIP": "10.0.9.0/24",
                "interface": "In:1 Out:2"
            }
        ]
    }
}
```
下发转发表接口：http://127.0.0.1:8000/controller/fib
```
{
    "code": 200,
    "order": null,
    "data": {
        "10.0.4.0/24": [
            {
                "dstIP": "10.0.3.0/24",
                "outInterfaceId": "1"
            }
        ],
        "10.0.3.0/24": [
            {
                "dstIP": "10.0.1.0/24",
                "outInterfaceId": "2"
            }
        ],
        "10.0.1.0/24": [
            {
                "dstIP": "10.0.9.0/24",
                "outInterfaceId": "2"
            }
        ]
    }
}
```
下发验证表接口：http://127.0.0.1:8000/controller/verifyTable
```
{
    "code": 200,
    "order": null,
    "data": {
        "10.0.8.0/24": [
            {
                "srcIP": "10.0.8.0/24",
                "inInterfaceId": "1"
            }
        ],
        "10.0.4.0/24": [
            {
                "srcIP": "10.0.4.0/24",
                "inInterfaceId": "2"
            }
        ],
        "10.0.3.0/24": [
            {
                "srcIP": "10.0.3.0/24",
                "inInterfaceId": "1"
            }
        ]
    }
}
```
获取拓扑链路信息接口：http://127.0.0.1:8000/controller/topoLink
```
{
    "code": 200,
    "order": null,
    "data": {
        "10.0.8.0/24": [
            {
                "srcIP": "10.0.8.0/24",
                "next_hop": "10.0.4.0/24",
                "link_performance": {
                    "延时": "15ms",
                    "丢包率": "1.18%",
                    "带宽": "863Mbps"
                }
            }
        ],
        "10.0.4.0/24": [
            {
                "srcIP": "10.0.4.0/24",
                "next_hop": "10.0.3.0/24",
                "link_performance": {
                    "延时": "42ms",
                    "丢包率": "2.97%",
                    "带宽": "409Mbps"
                }
            }
        ],
        "10.0.3.0/24": [
            {
                "srcIP": "10.0.3.0/24",
                "next_hop": "10.0.1.0/24",
                "link_performance": {
                    "延时": "91ms",
                    "丢包率": "2.83%",
                    "带宽": "286Mbps"
                }
            }
        ],
        "10.0.1.0/24": [
            {
                "srcIP": "10.0.1.0/24",
                "next_hop": "10.0.9.0/24",
                "link_performance": {
                    "延时": "3ms",
                    "丢包率": "2.22%",
                    "带宽": "450Mbps"
                }
            }
        ]
    }
}
```
获取节点主机信息接口：http://127.0.0.1:8000/controller/topoLink
```
{
    "code": 200,
    "order": null,
    "data": {
        "10.0.8.0/24": {
            "node": "10.0.8.0/24",
            "node_performance": {
                "cpu": "29.59%",
                "内存": "81.16%",
                "温度": "78°C"
            }
        },
        "10.0.4.0/24": {
            "node": "10.0.4.0/24",
            "node_performance": {
                "cpu": "57.83%",
                "内存": "58.80%",
                "温度": "81°C"
            }
        },
        "10.0.3.0/24": {
            "node": "10.0.3.0/24",
            "node_performance": {
                "cpu": "41.49%",
                "内存": "42.00%",
                "温度": "43°C"
            }
        }
    }
}
```