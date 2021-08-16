import warnings
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import plot, draw, show
from pandas import DataFrame, Series
import pims
import trackpy as tp
import time
import threading
import multiprocessing
import concurrent.futures

global mm
global ps 
global sep
global frames
global totalThreads
threadFlags = []
global size
totalThreads = 5
mm = 2000               #minmass
ps = 17                     #particles size
sep = 12                   #particle separation for detecting sticking particles

def thread0(threadnumber, numframes):
    f = tp.batch(frames[int(threadnumber*numframes):int((threadnumber+1)*numframes)], ps, minmass=mm, separation = sep);
    #dataFrame1[i] = f
    #print(dataFrame1[i])
    #print("Thread %d completed"%i)
    return f

if __name__ == "__main__":
   
    start_time = time.time()
    print("Starting the multiprocessing programm")

    warnings.simplefilter("ignore", RuntimeWarning)

    mpl.rc('figure',  figsize=(10, 5))
    mpl.rc('image', cmap='gray')
    
    global dataFrame1
    dataFrame1 = []
    
    global frames
    frames = pims.open('/home/sagar/Documents/codes/python/threading/data/*.tif')
    threadframes = len(frames) / totalThreads
    
    finaldataframe = []
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(thread0, i, threadframes) for i in range(0,totalThreads)]
    
        for i in concurrent.futures.as_completed(results):
            df = i.result()
            finaldataframe.append(df)
    
    print(finaldataframe)
      
    print("Time taken by the program = ", time.time()-start_time)
