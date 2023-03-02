import pandas as pd
import numpy as np
from graphy import graphy

df = pd.read_csv('../data/spaceship-titanic.csv')
features = ['CryoSleep', 'Age', 'VIP', 'RoomService',
            'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck',
            'Transported']

df = df.loc[:, features]
df = df.dropna(axis=0)
df = df.astype(np.float32)
print('*' * 100)
print(f"N-Size : {df.shape[0]}")
print('*' * 100)

d = graphy.Graphier(df, target='Transported')

d.build_graph(statistics='correlation', method='pearson', corr_threshold=0.15)
d.draw_graph(path_to_save='../sample_img/target.png', node_size=11, font_size=1.1)
