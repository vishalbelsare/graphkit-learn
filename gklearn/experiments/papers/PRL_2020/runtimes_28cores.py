#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 10:34:26 2020

@author: ljia
"""
from utils import Graph_Kernel_List, Dataset_List, compute_graph_kernel
from gklearn.utils.graphdataset import load_predefined_dataset
import logging


# def get_graphs(ds_name):
# 	from gklearn.utils.graph_synthesizer import GraphSynthesizer
# 	gsyzer = GraphSynthesizer()
# 	graphs = gsyzer.unified_graphs(num_graphs=100, num_nodes=num_nodes, num_edges=int(num_nodes*2), num_node_labels=0, num_edge_labels=0, seed=None, directed=False)
# 	return graphs


def xp_runtimes_of_all_7cores():
		
	# Run and save.
	import pickle
	import os
	save_dir = 'outputs/runtimes_of_all_7cores/'
	if not os.path.exists(save_dir):
		os.makedirs(save_dir)

	run_times = {}
	
	for kernel_name in Graph_Kernel_List:
		print()
		print('Kernel:', kernel_name)
		
		run_times[kernel_name] = []
		for ds_name in Dataset_List:
			print()
			print('Dataset:', ds_name)
			
			# get graphs.
			graphs, _ = load_predefined_dataset(ds_name)

			# Compute Gram matrix.
			try:
				gram_matrix, run_time = compute_graph_kernel(graphs, kernel_name, n_jobs=28)
				run_times[kernel_name].append(run_time)
			except Exception as exp:
				run_times[kernel_name].append('error')
				print('An exception occured when running this experiment:')
				LOG_FILENAME = save_dir + 'error.txt'
				logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
				logging.exception('')
				print(repr(exp))
			
			pickle.dump(run_time, open(save_dir + 'run_time.' + kernel_name + '.' + ds_name + '.pkl', 'wb'))
		
	# Save all.	
	pickle.dump(run_times, open(save_dir + 'run_times.pkl', 'wb'))	
	
	return


if __name__ == '__main__':
	xp_runtimes_of_all_7cores()
