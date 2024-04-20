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
                "interface": "In:1 Out:2"
            }
        ],
        "10.0.4.0/24": [
            {
                "next_hop": "10.0.3.0/24",
                "interface": "In:2 Out:1"
            }
        ],
        "10.0.3.0/24": [
            {
                "next_hop": "10.0.1.0/24",
                "interface": "In:1 Out:2"
            }
        ],
        "10.0.1.0/24": [
            {
                "next_hop": "10.0.9.0/24",
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