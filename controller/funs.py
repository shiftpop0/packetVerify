import requests
import networkx as nx
import matplotlib.pyplot as plt
import ipaddress
import random
def is_valid_ip(ip_with_mask):
    try:
        ip, mask = ip_with_mask.split('/')
        ipaddress.ip_address(ip)
        if not 0 <= int(mask) <= 32:
            return False
        return True
    except ValueError:
        return False

#建立拓扑
def analyze_routing_topology():
    # 获取路由表信息 http://127.0.0.1:8000/controller/rib
    url = 'http://127.0.0.1:8000/controller/rib'
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查响应
        data = response.json()['data']
    except requests.RequestException as e:
        return f"Request Fail: {e}"

    # 分析下一跳
    connections = []
    for entry in data.values():
        for route in entry:
            if all(is_valid_ip(route[field]) for field in ['srcIP', 'nextHop', 'dstIP']):
                interface = f"In:{route['inInterfaceId']} Out:{route['outInterfaceId']}"
                #connections.append((route['srcIP'], route['nextHop'], interface))
                connections.append((route['srcIP'], route['dstIP'], route['nextHop'], interface))
            else:
                print(f"Invalid IP format found and skipped: {route}")

    # 建立连接关系
    G = nx.DiGraph()
    for srcIP,  dstIP, next_hop, interface in connections:
        G.add_edge(srcIP, next_hop, label=interface) #用下一跳去建立连接关系

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    # plt.show()

    return connections

#根据拓扑信息随机选择相邻的三个节点，
def fetch_and_select_nodes():
    # 获取拓扑信息
    url = 'http://127.0.0.1:8000/controller/genTopo'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()['data']
        node_keys = list(data.keys())
        if len(node_keys) < 3:
            return "Not enough nodes to select three adjacent.", None
        # 随机选择三个相邻节点
        # random_start = random.randint(0, len(node_keys) - 3)
        # selected_nodes = node_keys[random_start:random_start + 3]
        # 改成头三个节点，确保每次选择的节点一样
        selected_nodes = node_keys[:3]
        return data, selected_nodes
    except requests.RequestException as e:
        return f"Request Fail: {str(e)}", None

# 转发表（目的ip/mask，出端口），转发表格式为{deviceId:[{dstIP,mask,outInterfaceId}]}
def analyze_fib():
    data, selected_nodes = fetch_and_select_nodes()
    fib = {}

    for node in selected_nodes:
        entries = data[node]
        fib[node] = [{'dstIP': entry['dstIP'].split('/')[0] +  '/' + entry['dstIP'].split('/')[1],
                      'outInterfaceId': entry['interface'].split('Out:')[1]} for entry in entries]
    return fib

#生成验证表, 验证表格式为 {deviceId:[{srcIP,mask,inInterfaceId}]}
def analyze_vt():
    data, selected_nodes = fetch_and_select_nodes()
    vt = {}
    for node in selected_nodes:
        entries = data[node]
        vt[node] = [{'srcIP': node.split('/')[0] +  '/' + node.split('/')[1],
                     'inInterfaceId': entry['interface'].split('In:')[1].split(' ')[0]} for entry in entries]
    return vt

#动态模拟每条链路的时延、丢包率、带宽
def analyze_link_performance():
    connections = analyze_routing_topology()
    link_performance = {}
    for connection in connections:
        delay = random.randint(1, 100)  # 延迟
        packet_loss = random.uniform(0, 0.05)  # 丢包
        bandwidth = random.randint(10, 1000)  # 带宽
        link_performance[connection] = {'延时': f"{delay}ms", '丢包率': f"{packet_loss * 100:.2f}%",
                                        '带宽': f"{bandwidth}Mbps"}
    return link_performance

#动态模拟各个节点的CPU利用率、内存利用率、温度
def analyze_node_performance():
    _, selected_nodes = fetch_and_select_nodes()  # Assume this function returns nodes
    node_performance = {}
    for node in selected_nodes:
        cpu_utilization = random.uniform(0, 1)
        memory_utilization = random.uniform(0, 1)
        temperature = random.randint(20, 90)
        node_performance[node] = {'cpu': f"{cpu_utilization * 100:.2f}%",
                                  '内存': f"{memory_utilization * 100:.2f}%",
                                  '温度': f"{temperature}°C"}
    return node_performance

if __name__ == '__main__':
   performance = analyze_node_performance()
   print(performance)