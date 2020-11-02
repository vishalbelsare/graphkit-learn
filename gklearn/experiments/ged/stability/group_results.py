#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 17:26:43 2020

@author: ljia

This script groups results together into a single file for the sake of faster 
searching and loading.
"""
import os
import pickle
import numpy as np
from shutil import copyfile
from tqdm import tqdm
import sys


def group_trials(dir_folder, name_prefix, override, clear, backup):
	
	# Get group name.
	label_name = name_prefix.split('.')[0]
	if label_name == 'ged_matrix':
		group_label = 'ged_mats'
	elif label_name == 'runtime':
		group_label = 'runtimes'
	else:
		group_label = label_name
	name_suffix = name_prefix[len(label_name):]
	if label_name == 'ged_matrix':
		name_group = dir_folder + 'groups/' + group_label + name_suffix + 'npy'
	else:
		name_group = dir_folder + 'groups/' + group_label + name_suffix + 'pkl'

	if not override and os.path.isfile(name_group):
		# Check if all trial files exist.
		trials_complete = True
		for trial in range(1, 101):
			file_name = dir_folder + name_prefix + 'trial_' + str(trial) + '.pkl'
			if not os.path.isfile(file_name):
				trials_complete = False
				break
	else:
		# Get data.
		data_group = []
		for trial in range(1, 101):
			file_name = dir_folder + name_prefix + 'trial_' + str(trial) + '.pkl'
			if os.path.isfile(file_name):
				with open(file_name, 'rb') as f:
					data = pickle.load(f)
					data_group.append(data)
			else: # Not all trials are completed.
				return
	
		# Write groups.
		if label_name == 'ged_matrix':
			data_group = np.array(data_group)
			with open(name_group, 'wb') as f:
				np.save(f, data_group)
		else:
			with open(name_group, 'wb') as f:
				pickle.dump(data_group, f)
				
		trials_complete = True

	if trials_complete:
		# Backup.
		if backup:
			for trial in range(1, 101):
				src = dir_folder + name_prefix + 'trial_' + str(trial) + '.pkl'
				dst = dir_folder + 'backups/' + name_prefix + 'trial_' + str(trial) + '.pkl'
				copyfile(src, dst)
				
		# Clear.
		if clear:
			for trial in range(1, 101):
				src = dir_folder + name_prefix + 'trial_' + str(trial) + '.pkl'
				os.remove(src)


def group_all_in_folder(dir_folder, override=False, clear=True, backup=True):
	
	# Create folders.
	if not os.path.exists(dir_folder + 'groups/'):
		os.makedirs(dir_folder + 'groups/')
	if backup:
		if not os.path.exists(dir_folder + 'backups'):
			os.makedirs(dir_folder + 'backups')
			
	# Iterate all files.
	cur_file_prefix = ''
	for file in tqdm(sorted(os.listdir(dir_folder)), desc='Grouping', file=sys.stdout):
		if os.path.isfile(os.path.join(dir_folder, file)):
			name_prefix = file.split('trial_')[0]
# 			print(name)
# 			print(name_prefix)
			if name_prefix != cur_file_prefix:
				group_trials(dir_folder, name_prefix, override, clear, backup)
				cur_file_prefix = name_prefix
	
		

if __name__ == '__main__':
 	dir_folder = 'outputs/CRIANN/edit_costs.num_sols.ratios.IPFP/'
 	group_all_in_folder(dir_folder)
	
 	dir_folder = 'outputs/CRIANN/edit_costs.repeats.ratios.IPFP/'
 	group_all_in_folder(dir_folder)