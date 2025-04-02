import psutil
import pandas as pd
import datetime

def check_memory(unit = 'GB', round_to = 3):
    unit = unit.lower()
    print(f'Timestamp: {datetime.datetime.now()}')
    unit_dd = {'bytes': 1, 'mb': 2**20, 'gb': 2**30, 'tb': 2**40}
    divider = unit_dd[unit]
    
    memory_df = pd.DataFrame(
                {
                  'TOTAL (RAM) memory in environment ({u})'.format(u = unit.upper()):round(psutil.virtual_memory()[0]/divider, round_to)
                  , "Memory available to you ({u})".format(u = unit.upper()):round(psutil.virtual_memory()[1]/divider,round_to)
                  , 'Perc memory available'.format(u = unit.upper()): psutil.virtual_memory()[2]
                  , 'Used memory ({u})'.format(u = unit.upper()):round(psutil.virtual_memory()[3]/divider,round_to)
                  , 'FREE memory ({u})'.format(u = unit.upper()):round(psutil.virtual_memory()[4]/divider,round_to)
                  }, index = ['']
                )
    
    return memory_df.T
