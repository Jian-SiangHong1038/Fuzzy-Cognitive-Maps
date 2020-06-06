import time, math, sys
from Simulation import * 
import ppft as pp
import FCM
import dispy
'''
    parallelizeS
    Parameters:
    fcm: An fcm already created
    stabilizers: Concepts to stabilize on and their stabilization threshold.
    Returns: The new concept values acquired from running simulation.
    Description: Creates a parallelized simulation process to be ran on the server.
'''

def parallelizeS(fcm, stabilizers):
    sim = FCM.simulation(fcm)
    
    for key in stabilizers:
        sim.stabilize(key,stabilizers[key])
    
    #simulate until 10000 steps or stability reached
    sim.steps(10000)
    sim.changeTransferFunction(lambda x: 1/(1+math.exp(-x)))
    values = sim.run()
    return values
    
'''
    parallelizeT
    Parameters: None.
    Returns: The transfer function.
    Description: Used to provide the parallelT function with the logic of the transfer function.
'''
    
def parallelizeT():
    ans = lambda x: 1/(1+math.exp(-x))
    return ans

'''
    parallelS
    Parameters:
    FCMs: A dictionary containing the FCMs to be parallelized along with the stabilizers to run simulation.
    Returns: Statistics of the execution of the jobs.
    Description: Takes multiple FCMs and parallelizes its simulation on a server. Module used for Parallel Python (pp): https://pypi.python.org/pypi/ppft
'''

def parallelS(FCMs):
    counter = 0
    print ("Number of FCMs to parallelize: ", len(FCMs))
    ppservers = ()
    
    job_server = pp.Server(ppservers=ppservers) # creates the job server
    
    print ("Starting pp with", job_server.get_ncpus(), "workers") # number of local processors
    
    start_time = time.time() # begin time

#    job1 = job_server.submit(parallelizeS, args=(fcm, FCMs[fcm],))
    # Retrieves the result calculated by job1
    # The value of job1() is the same as sum_primes(100)
    # If the job has not been finished yet, execution will wait here until result is available
#    result = job1() 
#    print ("Fuck is\n\n\n", result)
#    cluster = dispy.JobCluster(parallelizeS)
#    jobs = [(fcm, cluster.submit(fcm, FCMs[fcm])) for fcm in FCMs]
    # jobs - the tasks passed to the parallelize function
    jobs = [(fcm, job_server.submit(func=(parallelizeS), \
				    args=(fcm, FCMs[fcm],), \
#		     	depfuncs=(simulation.stabilize, simulation.steps, simulation.changeTransferFunction, simulation.run,), \
				    modules=("sys","FCM","Simulation",))) for fcm in FCMs]    

#    jobs = [(fcm, job_server.submit(parallelizeS, args=(fcm, FCMs[fcm],) )) for fcm in FCMs]
    for fcm, job in jobs:
        counter += 1
        print ("Simulation on FCM #", counter, "is\n\n", job()) # the output of simulation
    
    print ("\nTime elapsed: ", time.time() - start_time, "s\n\n") # end time
    return job_server.print_stats()

'''
    parallelT
    Parameters:
    job_count: An integer representing the number of times to parallilize the transfer function.
    Returns: Statistics of the execution of the jobs.
    Description: Parallelizes the transfer function by pushing it on a server. Module used for Parallel Python (pp): https://pypi.python.org/pypi/ppft
'''

def parallelT(job_count):
    ppservers = ()
    
    job_server = pp.Server(ppservers=ppservers) # creates the job server
# job_server.get_ncpus()
    print ("Starting pp with", job_server.get_ncpus(), "workers") # number of local processors
    
    start_time = time.time() # begin time
    
    # jobs - the tasks passed to the parallelize function
    jobs = [(i, job_server.submit(func=(parallelizeT),
				  args=(), 
           			  modules=("math",))) for i in range(job_count)]
    for i, job in jobs:
                
         print ("Transfer function #", i, "is", job()) # the lambda transfer function


    print ("\nTime elapsed: ", time.time() - start_time, "s\n\n")
    return job_server.print_stats()
