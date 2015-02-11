#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2015/02/11

@author: spiralray
'''


import numpy as np
import math

class Shuttle:
    resist_coeff = 0.001075
    gravity = 9.812
    mass = 0.00467
    
    def __init__(self, mu):
        self.mu = mu
        
        self.Sigma = np.zeros((9,9))
        
        self.B = np.mat([
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,-self.gravity,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,-self.gravity] ])
        
        self.Q = np.eye(9)
        self.R = np.eye(3)

    def getA(self, mu, period):   #Observation matrix
        airR = -self.resist_coeff * math.sqrt(mu[3,0]**2 + mu[4,0]**2 + mu[5,0]**2 ) / self.mass
        
        return np.mat([
            [1,0,0,period,0,0,0,0,0],
            [0,1,0,0,period,0,0,0,0],
            [0,0,1,0,0,period,0,0,0],
            [0,0,0,1,0,0,period,0,0],
            [0,0,0,0,1,0,0,period,0],
            [0,0,0,0,0,1,0,0,period],
            [0,0,0,airR,0,0,0,0,0],
            [0,0,0,0,airR,0,0,0,0],
            [0,0,0,0,0,airR,0,0,0]
        ])
    
    def Jh(self, mu):   #Observation matrix
        return np.mat([
            [1,0,0,0,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,0]
        ])
        
    def predict(self,period):
        
        self.A = self.getA(self.mu,period)
        self.u = np.mat([[0],[0],[0],[0],[0],[period],[0],[0],[1]])
        # prediction
        self.mu = self.A * self.mu + self.B * self.u
        self.Sigma_ = self.Q + self.A * self.Sigma * self.A.T
        
    def update(self, Y):    #Y Observation value
        self.C = self.Jh(self.mu)
        self.yi = Y - self.C * self.mu
        self.S = self.C * self.Sigma_ * self.C.T + self.R
        self.K = self.Sigma_ * self.C.T * self.S.I
        self.mu = self.mu + self.K * self.yi
        self.Sigma = self.Sigma_ - self.K * self.C * self.Sigma
        
    def getState(self):
        return self.mu

