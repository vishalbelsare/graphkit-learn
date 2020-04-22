#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 11:31:26 2020

@author: ljia
"""
import numpy as np

class NodeMap(object):
	
	def __init__(self, num_nodes_g, num_nodes_h):
		self.__forward_map = [np.inf] * num_nodes_g
		self.__backward_map = [np.inf] * num_nodes_h
		self.__induced_cost = np.inf
		
		
	def num_source_nodes(self):
		return len(self.__forward_map)
	
	
	def num_target_nodes(self):
		return len(self.__backward_map)
	
	
	def image(self, node):
		if node < len(self.__forward_map):
			return self.__forward_map[node]
		else:
			raise Exception('The node with ID ', str(node), ' is not contained in the source nodes of the node map.')
		return np.inf
	
	
	def pre_image(self, node):
		if node < len(self.__backward_map):
			return self.__backward_map[node]
		else:
			raise Exception('The node with ID ', str(node), ' is not contained in the target nodes of the node map.')
		return np.inf
	
	
	def get_forward_map(self):
		return self.__forward_map
	
	
	def get_backward_map(self):
		return self.__backward_map
	
	
	def add_assignment(self, i, k):
		if i != np.inf:
			if i < len(self.__forward_map):
				self.__forward_map[i] = k
			else:
				raise Exception('The node with ID ', str(i), ' is not contained in the source nodes of the node map.')
		if k != np.inf:
			if k < len(self.__backward_map):
				self.__backward_map[k] = i
			else:
				raise Exception('The node with ID ', str(k), ' is not contained in the target nodes of the node map.')
	
	
	def set_induced_cost(self, induced_cost):
		self.__induced_cost = induced_cost
		
		
	def induced_cost(self):
		return self.__induced_cost