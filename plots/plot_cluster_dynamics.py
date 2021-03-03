import config as cf
import numpy as np
import pandas as pd
import os
import random 
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
from models import sis_replicator
from models.get_clusters import get_partition, cluster_dynamics
assert cf

import argparse 

parser = argparse.ArgumentParser(description='Network simulations.')

parser.add_argument('--network_type', type=str, default='scale_free',
                    help='Network type for storing...')
parser.add_argument('--network_name', type=str, default='new_scale_free_5000',
                    help='Network type for storing...')
parser.add_argument('--iterations', type=str, default='10',
                    help='Selected iterations for plotting...')
parser.add_argument('--n_clusters', type=str, default='3',
                    help='Selected iterations for plotting...')
parser.add_argument('--beta_select', type=str, default='0.6',
                    help='Selected beta for plotting...')
parser.add_argument('--sigma_select', type=str, default='1.0',
                    help='Selected beta for plotting...')
parser.add_argument('--type_sim', default='global',type=str, 
                    help='For running local or global simulation')

args = parser.parse_args()

# sigma_search = pd.read_csv(args.awareness_path, dtype={'key':str, 'value':float})
# beta_search  = pd.read_csv(args.infection_prob_path, dtype={'key':str, 'value':float})


config_data = pd.read_csv('config.csv', sep=',', header=None, index_col=0)

networks_path = config_data.loc['networks_dir'][1]
results_path  = config_data.loc['results_dir'][1]
figures_path  = config_data.loc['figures_dir'][1]
num_nodes     = int(config_data.loc['num_nodes'][1])
if args.network_name == 'new_scale_free_5000':
    num_nodes = 5000

# Path to checkpoints
game_checkpoint_path_global = os.path.join(results_path, num_nodes, 'global', args.network_type,'checkpoints')
disease_checkpoint_path_global = os.path.join(results_path, num_nodes, 'global', args.network_type,'checkpoints')

game_checkpoint_path_local = os.path.join(results_path, num_nodes, 'local', args.network_type,'checkpoints')
disease_checkpoint_path_local = os.path.join(results_path, num_nodes, 'local', args.network_type,'checkpoints')

# Load network
G = nx.read_gpickle( os.path.join(networks_path, args.network_name) )


# Get communities
from get_clusters import get_partition

partition, n_cluster, cluster_nodes, top_clusters, top_cluster_nodes = get_partition(G, n_biggest=args.n_clusters) #n_biggest=3)


# Get cluster dynamics
from get_clusters import cluster_dynamics

df_cluster_dyncs_global = top_cluster_dynamics(top_cluster_nodes, disease_checkpoint_path_global, game_checkpoint_path_global, beta=args.beta_select, sigma=args.sigma_select)
df_cluster_dyncs_local = top_cluster_dynamics(top_cluster_nodes, disease_checkpoint_path_local, game_checkpoint_path_local, beta=args.beta_select, sigma=args.sigma_select)


## Plot results

colors_plt = [ 'tab:green', 'tab:red', 'tab:blue'] #, 'tab:purple', 'tab:cyan', 'tab:orange'  ]

n_top_clusters = list(top_cluster_nodes.keys())
n_top_clusters = n_top_clusters[:3]                 # Get biggest 3

fig, ax = plt.subplots(1,2,figsize=(20, 7))
ax = ax.flatten()

for idx, clust in tqdm(enumerate(n_top_clusters), total=len(n_top_clusters)):

    # Get cluster data
    clust_mask_global = df_cluster_dyncs_global['cluster'] == clust
    clust_mask_local = df_cluster_dyncs_local['cluster'] == clust

    # For global
    df_clust_i_glob = pd.DataFrame(df_cluster_dyncs_global[clust_mask_global])
    df_clust_i_glob['type'] = ['Local'] * len(df_clust_i_glob)
    df_clust_i_loc  = pd.DataFrame(df_cluster_dyncs_local[clust_mask_local])
    df_clust_i_loc['type'] = ['Global'] * len(df_clust_i_loc)

    df_res = [df_clust_i_loc, df_clust_i_glob]
    df_res_c = pd.concat(df_res)


    # Plot global
    sns.lineplot( ax = ax[0],
                  data = df_res_c,
                  x = 'time', y = 'I',
                  label = r'Cluster {}: {} individuals'.format(clust, top_clusters[clust]),
                  style='type',
                  color=colors_plt[idx],
                  alpha=0.5)
    ax[0].get_legend().remove()
    #ax[0].lines[0].set_linestyle("--")
    ax[0].set_title(r'Clustered disease dynamics $R_0=4.2$ $\sigma={}$ '.format(sigma),fontsize=22)
    ax[0].set_xlabel(r'Days',fontsize=21)
    ax[0].xaxis.set_tick_params(labelsize=20)
    ax[0].yaxis.set_tick_params(labelsize=20)
    ax[0].set_xlim([-0.1,151])
    ax[0].set_ylabel(r'Cluster Inf. Fraction $I$',fontsize=21)
    ax[0].set_ylim([-0.1,1.1])

    sns.lineplot( ax = ax[1],
                  data = df_res_c,
                  x = 'time', y = 'C',
                  style='type',
                  color=colors_plt[idx],
                  alpha = 0.5)
    ax[1].get_legend().remove()
    #ax[0].lines[0].set_linestyle("--")
    ax[1].set_title(r'Clustered behavioral dynamics $R_0=4.2$ $\sigma={}$ '.format(sigma),fontsize=22)
    ax[1].set_xlabel(r'Days',fontsize=21)
    ax[1].xaxis.set_tick_params(labelsize=20)
    ax[1].yaxis.set_tick_params(labelsize=20)
    ax[1].set_xlim([-0.1,151])
    ax[1].set_ylabel(r'Cluster Coop. Fraction $c$',fontsize=21)
    ax[1].set_ylim([-0.1,1.1])
    plt.tight_layout()

plt.savefig(os.path.join(figures_path,'dynamics', 'new_cluster_dynamics_sigma_{}.png'.format(sigma)), 
                             dpi=400, transparent = False, bbox_inches = 'tight', pad_inches = 0.1)
#plt.show()
import os
os.system('say "your program has finished" ')


plt.show()

### save legends
fig, ax = plt.subplots(2,1,figsize=(9, 8))
coms = [1,2,3]
for idx, clust in tqdm(enumerate(n_top_clusters), total=len(n_top_clusters)):

    # Get cluster data
    clust_mask_global = df_cluster_dyncs_global['cluster'] == clust

    # For global
    df_clust_i_glob = pd.DataFrame(df_cluster_dyncs_global[clust_mask_global])

    sns.lineplot( ax = ax[0],
                  data = df_clust_i_glob, 
                  x = 'time', y = 'I',
                  label = r'Community {}: {} ind.'.format(coms[idx], top_clusters[clust]),
                  color = colors_plt[idx])
    ax[0].get_legend().remove()
    ax[0].set_title(r'Disease dynamics')
    #ax[0].set_xlabel('')
    ax[0].set_xlabel(r'Days',fontsize=21)
    #ax[0].set_xticks(fontsize=20)
    ax[0].set_xticklabels('')
    ax[0].set_xlim([-0.1,151])
    ax[0].set_ylabel(r'Inf. Fraction $\bar{I}$',fontsize=21)
    #ax[0].set_yticks(fontsize=20)
    ax[0].set_ylim([-0.1,1.1])

    plt.figlegend(bbox_to_anchor=(0.9,0.4), fontsize=22)

plt.savefig(os.path.join(figures_path, 'dynamics', 'new_colorlabel_cluster_dynamics.png'), 
                             dpi=400, transparent = False, bbox_inches = 'tight', pad_inches = 0.1)
plt.show()

#### save type
fig, ax = plt.subplots(2,1,figsize=(9, 8))


df_clust_t_loc  = df_cluster_dyncs_local.copy()
df_clust_t_loc['type'] = ['Global'] * len(df_cluster_dyncs_local)
df_clust_t_glob = df_cluster_dyncs_global.copy()
df_clust_t_glob['type'] = ['Local'] * len(df_cluster_dyncs_global)

df_res = [df_clust_t_loc, df_clust_t_glob]
df_res_c = pd.concat(df_res)

sns.lineplot( ax = ax[0],
                data = df_res_c, 
                x = 'time', y = 'I',
                style='type', alpha=0.5)
ax[0].get_legend().remove()
ax[0].set_title(r'Disease dynamics')
#ax[0].set_xlabel('')
ax[0].set_xlabel(r'Days',fontsize=21)
#ax[0].set_xticks(fontsize=20)
ax[0].set_xticklabels('')
ax[0].set_xlim([-0.1,151])
ax[0].set_ylabel(r'Inf. Fraction $\bar{I}$',fontsize=21)
#ax[0].set_yticks(fontsize=20)
ax[0].set_ylim([-0.1,1.1])

plt.figlegend(bbox_to_anchor=(0.7,0.4), fontsize=22)

plt.savefig(os.path.join(figures_path, 'dynamics', 'style_cluster_dynamics.png'), 
                             dpi=400, transparent = False, bbox_inches = 'tight', pad_inches = 0.1)
plt.show()



## Plot graph
from matplotlib import cm
def plot_G(G, communities, not_comms, plot_title, nodecmap,figures_path=figures_path):

    n_comms = max(communities.values())
    pos     = nx.kamada_kawai_layout(G)

    plt.figure(figsize=(12,12))
    #cmap = cm.get_cmap('hsv')#, n_comms+)
    #plt.title(str(plot_title) + ' {} biggest clusters'.format(n_comms), size=15)

    nx.draw(G, pos,
            nodelist    = list(not_comms.keys()),
            node_size   = 12,
            #cmap        = cmap,
            node_color  = 'black',
            edge_color  = 'gray',
            width       = .2,
            with_labels = False
            )

    nx.draw(G, pos,
            nodelist    = list(communities.keys()),
            node_size   = 12,
            #cmap        = cmap,
            node_color  = nodecmap,
            edge_color  = 'gray',
            width       = .2,
            with_labels = False
            )
    plt.savefig(os.path.join(figures_path,'graph_cluster_dynamics_new_6clus.png'), 
                              dpi=400, transparent = True, bbox_inches = 'tight', pad_inches = 0.1)
    plt.show()
# G_1000 = nx.read_gpickle( os.path.join(networks_path, 'scale_free_1000') )
# partition_1000, n_cluster_1000, cluster_nodes_other_node_cluster1000, top_clusters_1000, top_cluster_nodes_1000 = get_partition(G_1000, n_biggest=3)




n_top_clusters = list(top_cluster_nodes.keys())
nodes = []
cluster = []
n_nodes = []
n_cluster = []
for idx, clus in enumerate(n_top_clusters):
    for key, value in partition.items():
        if clus == value:
            nodes.append(key)
            cluster.append(value)
        else:
            n_nodes.append(key)
            n_cluster.append(value)

node_cluster = dict(zip(nodes,cluster))
other_node_cluster = dict(zip(n_nodes,n_cluster))
colors_plt = [ 'tab:green', 'tab:red', 'tab:blue', 'tab:purple', 'tab:cyan', 'tab:orange' ]
node_cmap = []
for n, c in node_cluster.items():
    if c == n_top_clusters[0]:
        node_cmap.append(colors_plt[0])
    if c == n_top_clusters[1]:
        node_cmap.append(colors_plt[1])
    if c == n_top_clusters[2]:
        node_cmap.append(colors_plt[2])
    if c == n_top_clusters[3]:
        node_cmap.append(colors_plt[3])
    if c == n_top_clusters[4]:
        node_cmap.append(colors_plt[4])
    if c == n_top_clusters[5]:
        node_cmap.append(colors_plt[5])

plot_G(G, node_cluster, other_node_cluster, 'Clustered graph', node_cmap)

######################### 
# Graph states


def plot_steady(G, states, nodecmap,figures_path=figures_path):

    #n_comms = max(communities.values())
    pos     = nx.kamada_kawai_layout(G)

    plt.figure(figsize=(12,12))

    nx.draw(G, pos,
            nodelist    = list(states.keys()),
            node_size   = 12,
            #cmap        = cmap,
            node_color  = nodecmap,
            edge_color  = 'gray',
            width       = .2,
            with_labels = False
            )
    plt.savefig(os.path.join(figures_path,'graph_states_end.png'), 
                              dpi=400, transparent = True, bbox_inches = 'tight', pad_inches = 0.1)
    plt.show()
# G_1000 = nx.read_gpickle( os.path.join(networks_path, 'scale_free_1000') )
# partition_1000, n_cluster_1000, cluster_nodes_other_node_cluster1000, top_clusters_1000, top_cluster_nodes_1000 = get_partition(G_1000, n_biggest=3)


nodes = [node for node in G.nodes()]
state = graph_end_states.tolist()

node_state = dict(zip(nodes,state))
colors_plt = [ 'palegreen', 'dodgerblue', 'darkorange', 'darkred'] #, 'tab:cyan', 'tab:orange' ]
node_cmap = []
for n, s in node_state.items():
    if s == 0:  # cooperator
        node_cmap.append(colors_plt[0])
    if s == 1:
        node_cmap.append(colors_plt[1])
    if s == 2:
        node_cmap.append(colors_plt[2])
    if s == 3:
        node_cmap.append(colors_plt[3])


plot_steady(G, node_state, node_cmap)



def plot_steady_games(G, states, nodecmap,figures_path=figures_path):

    #n_comms = max(communities.values())
    pos     = nx.kamada_kawai_layout(G)

    plt.figure(figsize=(12,12))

    nx.draw(G, pos,
            nodelist    = list(states.keys()),
            node_size   = 12,
            #cmap        = cmap,
            node_color  = nodecmap,
            edge_color  = 'gray',
            width       = .2,
            with_labels = False
            )
    plt.savefig(os.path.join(figures_path,'graph_game_states_end_t30.png'), 
                              dpi=400, transparent = True, bbox_inches = 'tight', pad_inches = 0.1)
    #plt.show()


nodes = [node for node in G.nodes()]
state = graph_end_states
node_state = dict(zip(nodes,state))
colors_plt = [ 'deepskyblue', 'darkred']
node_cmap = []
for n, s in node_state.items():
    if s == 0:  # cooperator
        node_cmap.append(colors_plt[0])
    if s == 1:  # defector
        node_cmap.append(colors_plt[1])

plot_steady_games(G, node_state, node_cmap)

import os
os.system('say "your program has finished" ')

# %%
def gamma_inference(G):
    # Fit node degree distribution with powerlaw
    # G: undirected scale-free graph
    degree_vals = sorted([d for n,d in G.degree()], reverse=True)
    fit = powerlaw.Fit(degree_vals, xmin=1)
    fig = fit.plot_pdf(color='b', linewidth=2)
    fit.power_law.plot_pdf(color='g', linestyle='--', ax=fig)
    gamma = fit.alpha
    return gamma