# Exponential
python run/run_sims.py --network_type scale_free --network_name scale_free_2000 --num_nodes 2000 --type_sim local --beta_function exponential
python run/run_sims.py --network_type scale_free --network_name scale_free_2000 --num_nodes 2000 --type_sim global --beta_function exponential

# Linear
python run/run_sims.py --network_type scale_free --network_name scale_free_2000 --num_nodes 2000 --type_sim local --beta_function linear
python run/run_sims.py --network_type scale_free --network_name scale_free_2000 --num_nodes 2000 --type_sim global --beta_function linear

# Concave
python run/run_sims.py --network_type scale_free --network_name scale_free_2000 --num_nodes 2000 --type_sim local --beta_function concave
python run/run_sims.py --network_type scale_free --network_name scale_free_2000 --num_nodes 2000 --type_sim global --beta_function concave

# Convex
python run/run_sims.py --network_type scale_free --network_name scale_free_2000 --num_nodes 2000 --type_sim local --beta_function convex
python run/run_sims.py --network_type scale_free --network_name scale_free_2000 --num_nodes 2000 --type_sim global --beta_function convex

# S-shape
python run/run_sims.py --network_type scale_free --network_name scale_free_2000 --num_nodes 2000 --type_sim local --beta_function s-shape
python run/run_sims.py --network_type scale_free --network_name scale_free_2000 --num_nodes 2000 --type_sim global --beta_function s-shape

