import requests
import networkx as nx
import matplotlib.pyplot as plt
import ipaddress
import random
def is_valid_ip(ip_with_mask):
    try:
        if not ip_with_mask or ip_with_mask == '""':  #检查空的
            return True
        if '/' in ip_with_mask:
            ip, mask = ip_with_mask.split('/')
            ipaddress.ip_address(ip)  #验证IP 格式
            if not 0 <= int(mask) <= 32:  # 掩码范围
                return False

        else:
            ipaddress.ip_address(ip_with_mask)  #ip没有掩码格式
        return True
    except ValueError:
        return False

#建立拓扑
def analyze_routing_topology():
    # 获取路由表信息 http://127.0.0.1:8000/controller/rib
    url = 'http://127.0.0.1:8000/controller/rib'
    try:
        response = requests.get(url)
        # response.raise_for_status()  # 检查响应
        data = response.json()['data']
    except requests.RequestException as e:
        return f"Request Fail: {e}"

    # 分析下一跳
    connections = []
    for device_id, entries in data.items():
        for route in entries:
            if all(is_valid_ip(route[field]) for field in ['srcIP', 'dstIP', 'nextHop']):
                connection = (device_id, route['srcIP'], route['dstIP'], route['nextHop'], route['inInterfaceId'], route['outInterfaceId'], route['controller_ip'])
                connections.append(connection)
            else:
                print(f"Invalid IP format found and skipped: {route}")

    # 建立每个设备端口到端口的连接
    G = nx.DiGraph()
    for deviceID, srcIP, dstIP, next_hop, inInterface, outInterface,controlloer_ip in connections:
        src_label = f"{srcIP} {outInterface}" #源是出接口
        dst_label = f"{next_hop} {inInterface}" #目的是入接口
        if next_hop and next_hop != '""':
            # 使用出端口和入端口作为边的标签
            edge_label = f"{outInterface} -> {inInterface}"
            G.add_edge(src_label, dst_label, label=edge_label)

    # 布局
    pos = nx.spring_layout(G)

    # 绘图
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
        if len(data) < 3:
            return data
        else:
            selected_nodes = data[:3]
            return selected_nodes
        # 先选择头三个节点，后面改成随机的
    except requests.RequestException as e:
        return f"Request Fail: {str(e)}", None

# 转发表（目的ip/mask，出端口），转发表格式为{deviceId:[{dstIP,mask,outInterfaceId}]}
def analyze_fib():
    selected_nodes = fetch_and_select_nodes()
    fib = {}
    for node in selected_nodes:
        fib[node['deviceId']] = [{'dstIP': node['dstIP'].split('/')[0] +  '/' + node['dstIP'].split('/')[1],
                      'outInterface': node['outInterface']}]
    return fib

#生成验证表, 验证表格式为 {deviceId:[{srcIP,mask,inInterfaceId}]}
def analyze_vt():
    selected_nodes = fetch_and_select_nodes()
    vt = {}
    for node in selected_nodes:
        vt[node['deviceId']] = [{'srcIP': node['srcIP'].split('/')[0] +  '/' + node['srcIP'].split('/')[1],
                                'inInterface': node['inInterface']}]
        # entries = data[node]
        # vt[node] = [{'srcIP': node.split('/')[0] +  '/' + node.split('/')[1],
        #              'inInterfaceId': entry['interface'].split('In:')[1].split(' ')[0]} for entry in entries]
    return vt

#动态模拟每条链路的时延、丢包率、带宽
def analyze_link_performance():
    connections = analyze_routing_topology()
    link_performance = {}
    for connection in connections:
        delay = random.randint(1, 100)  # 延迟
        packet_loss = random.uniform(0, 0.05)  # 丢包
        bandwidth = random.randint(10, 1000)  # 带宽
        key = connection[0]
        link_performance[key] = {'延时': f"{delay}ms", '丢包': f"{packet_loss * 100:.2f}%",
                                        '带宽': f"{bandwidth}Mbps"}
    return link_performance

#动态模拟所有节点的CPU利用率、内存利用率、温度
def analyze_node_performance():
    selected_nodes = fetch_and_select_nodes()
    if not selected_nodes:
        return "Failed to fetch nodes or not enough nodes."

    node_performance = {}
    for node in selected_nodes:
        cpu_utilization = random.uniform(0, 75)
        memory_utilization = random.uniform(0, 65)
        temperature = random.randint(20, 90)
        node_performance[node['deviceId']] = {
            'cpu': f"{cpu_utilization:.2f}%",
            '内存': f"{memory_utilization:.2f}%",
            '温度': f"{temperature}°C"
        }
    return node_performance


if __name__ == '__main__':
    print(analyze_fib())