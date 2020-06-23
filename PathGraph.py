"""
绘制依赖图
"""
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)

# 读取文件数据
flit_path = {}
flit_path['source'] = []
flit_path['purpose'] = []
node = []
filename = "..\Data\data20200611_uniform_vc_4_size_8\pretreatment_flitpath.txt"
path = open(filename, "r")
for pathline in path:
    newline = pathline.split('.')
    router = newline[0].split('=')
    print(router)
    for i in range(len(router)):
        node.append(router[i].split('_')[1])
    print(node)
    for j in range(len(node)-1):
        flit_path['source'].append(node[j])
        flit_path['purpose'].append(node[j + 1])
    node.clear()
df = pd.DataFrame(flit_path)
# 绘制网络图
G = nx.from_pandas_edgelist(df, 'source', 'purpose', create_using=nx.DiGraph())
nx.draw(G, with_labels=True, node_size=150, width=0.5, font_size=5, node_color="skyblue", pos=nx.fruchterman_reingold_layout(G))
plt.show()
