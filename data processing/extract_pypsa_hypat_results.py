#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 18:24:52 2023

@author: haz43975
"""
import os
import pypsa

countries = ['NA']
scenarios = ['OPTIMISTIC', 'REALISTIC', 'CONSERVATIVE']
#scenarios = ['CONSERVATIVE']
years = ['2030'] #, '2050']

ports = ['NAM12_AC', 'NAM20_AC']


for country in countries:
    for scenario in scenarios:
        for year in years:
            
            for file in os.listdir('results/{0}_{1}_{2}/postnetworks/'.format(country, scenario, year)):
                quantity = file.split('_')[-1].split('export')[0]

                n = pypsa.Network("results/{0}_{1}_{2}/postnetworks/{3}".format(country, scenario, year, file))
                #print(country, scenario, year, file)
                n.buses_t.marginal_price.loc[:,ports].to_csv('HyPAT/{0}/{0}_{1}_{2}_{3}_elec_lmp.csv'.format(country, year, scenario, quantity))
                n.links_t.p0.filter(like='export').loc[:,[port + " H2 export" for port in ports]].to_csv('HyPAT/{0}/{0}_{1}_{2}_{3}_h2_delivery.csv'.format(country, year, scenario, quantity))
                n.links_t.p1.filter(like='lysis').loc[:,[port + " H2 Electrolysis" for port in ports]].to_csv('HyPAT/{0}/{0}_{1}_{2}_{3}_h2_prod.csv'.format(country, year, scenario, quantity))