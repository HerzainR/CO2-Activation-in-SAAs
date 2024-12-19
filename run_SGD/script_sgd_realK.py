#import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import json

# The three lines below define the number of SGD run to perform (n_runs),
# the number of seeds used in the Monte Carlo study of the SGs (n_seeds_try), 
# and k_means is this number for this parameter. 
n_runs = [1,2]
n_seeds_try = [50000]
k_means = 12

# Utility function definition and dataset file
utility = 'normalized_positive_mean_shift'
data_file = 'co2_activation_on_saa.csv' 

# Initial check of the folder to perform the runs
if not os.path.isdir(utility):
    os.makedirs(utility) 
    os.chdir(utility)

    # Making of the folders were each run is going to take place
    for run in n_runs:
    
        base_runs = 'run_' + str(run)
    
        os.makedirs(base_runs)
        os.chdir(base_runs)
    
        # Making the forlders for each number of seeds
        for seed in n_seeds_try:
    
            seed_folder = str(seed) + '_seeds' 
            os.makedirs(seed_folder)
            os.chdir(seed_folder)
    
            get_data_set = 'cp ../../../' + data_file + ' .'
    
            os.system(get_data_set)
    
            ##########   BEGIN SGD runs  #############

            #get dataset
            df=pd.read_csv(data_file).set_index('Site')
            
            #choose the candidate descriptive parameters within the dataset
            attribute_list=['PE_h',
                            'IP_h',      
                            'EA_h',
                            'rs_h',
                            'rp_h',
                            'rd_h',
                            'rval_h',
                            'PE_sa',
                            'IP_sa',
                            'EA_sa',
                            'rs_sa',
                            'rp_sa',
                            'rd_sa',
                            'rval_sa',
                            'PE_site',
                            'IP_site',
                            'EA_site',
                            'PE_snn',
                            'IP_snn',
                            'EA_snn',
                            'CN',
                            'gen_CN',
                            'site_no',
                            'bulk_nnd',  
                            'max_d_CO']
            
            df_input = df[attribute_list].copy()
            
            # This function will write the input file for realkd
            def write_input(path, df, id_job, n_cutoffs, algo, dev, n_res, n_seeds, target_key):
                """
                creates the two input files necessary to run the algorithm:
                i) a .json file with calculation details, named "id_job.json", and
                ii) a .xarf file with the data set, named "id_job.xarf".
                function arguments: path(str): path to the folder where the files 
                                               will be written
                           df(data frame): data set containing the values for the 
                                           candidate descriptive parameters and for
                                           the target for all adsorption sites
                           id_job(str): job name
                           n_cutoffs(int): number of cutoffs to be used in k-Means
                                           clustering to generate the propositions
                           algo(str): SG search algorithm (PMM_SAMPLER or EMM_SAMPLER)
                                      PMM_SAMPLER uses std(SG)/std(P) as utility function
                                      whereas EMM_SAMPLER uses the function specified in dev
                           dev(str): deviation measure when using EMM_SAMPLER 
                                     (e.g. cumulative_jensen_shannon_divergence)
                           n_res(int): number of results, i.e., number of top-ranked
                                       SGs to display
                           n_seeds(int): number of seeds to use for the SG search
                           target_key(str): label of the variable to be used as target quantity in SGD
                """
                df.to_csv(path+'/'+id_job+'.csv')
                with open(path+'/'+id_job+'.csv', 'r') as file_in:
                    data = file_in.read().splitlines(True)
                    
                file_out = open(path+'/'+id_job+'.xarf', 'w')
                file_out.write('@relation '+id_job+'\n')
                file_out.write('@attribute sites name\n')
                for variable in list(df.columns):
                    file_out.write('@attribute '+variable+' numeric\n')
                file_out.write("@data\n")
                file_out.close()
            
                with open(path+'/'+id_job+'.xarf', 'a') as file_out:
                    file_out.writelines(data[1:])
                    file_out.close()
                
                input_file = {}
                input_file = {"type" : "productWorkScheme",
                              "id" : id_job,
                              "workspaces" : [ {
                                            "type" : "workspaceFromXarf",
                                            "id" : id_job,
                                            "datafile" : id_job+".xarf",
                                            "propScheme": {"type": "standardPropScheme",
                                                            "defaultMetricRule": {"type": "kmeansPropRule",
                                                                                   "numberOfCutoffs": n_cutoffs,
                                                                                   "maxNumberOfIterations": 1000}}} ],
                                "computations" : [ {
                                            "type" : "legacyComputation",
                                            "id" : "subgroup_analysis",
                                            "algorithm" : algo,
                                            "parameters" : {
                                                "dev_measure": dev,
                                                "attr_filter" : "[]",
                                                "cov_weight" : "1.0",
                                                "num_res" : n_res,
                                                "num_seeds" : n_seeds,
                                                "targets" : "["+target_key+"]"
                                                         }
                              }],
                              "computationTimeLimit" : 360000
                                 }
                with open(path+'/'+id_job+'.json','w') as outfile:
                    json.dump(input_file, outfile, indent=4)
            
            id_job_scaling = utility
            write_input('./', df_input, id_job_scaling, k_means, 'EMM_SAMPLER',utility, 1500, seed, 'max_d_CO')  
            
            # The next line will take care to run realkd.
            os.system('java -jar $PATH_to_real_KD/realkd-0.7.1-jar-with-dependencies.jar '+id_job_scaling+'.json')
            
            os.chdir("..")  # Going back from the #_seeds folders
        os.chdir("..")  # Going back from the run_# folders
    
else:
    print('Runs for this utility function: ' + utility)
    print('have already an existing folder ...')

