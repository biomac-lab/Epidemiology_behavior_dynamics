import random 
import os
import pandas as pd
import numpy as np

import argparse 

parser = argparse.ArgumentParser(description='Network simulations.')

parser.add_argument('--num_ic', type=int, default=10,
                    help='Number of initial contions to generate')

args = parser.parse_args()

IC = pd.DataFrame(columns =['ic_index', 'I', 'D'])

main_path = os.path.split(os.getcwd())[0]
config_path = os.path.split(os.getcwd())[0]+'/config.csv'
config_data = pd.read_csv(config_path, sep=',', header=None, index_col=0)

N     = int(config_data.loc['num_nodes'][1])


IC['ic_index'] = list(range(args.num_ic))
IC = IC.set_index('ic_index')
for iter_ic in range(args.num_ic):
    I = random.sample(range(N), 1)
    D = random.sample(range(N), int(N/2) )
    D = [str(d) for d in D]
    D = '|'.join(D)

    IC.loc[iter_ic]['I'] = I[0]
    IC.loc[iter_ic]['D'] = D

D = np.fromstring(D, sep='|')

IC.to_csv('init_conditions/initial_conditions.csv')

print('Initial conditions created')