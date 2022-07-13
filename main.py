class ExamException(Exception):
    pass

    
def compute_daily_max_difference(time_series):
    
    list_t = []
    max_difference = []
    day_start = []
    day_end = []
    n = 0 # variabile iteratore
    
    for item in time_series:
        
        start = item[0] - item[0] % 86400  # inizio giorno        
        end = start + 86400  # fine giorno
        
        if start not in day_start: # lista inizio giorni
            day_start.append(start)
            
        if end not in day_end: # lista fine giorni
            day_end.append(end)
        
        if item[0] < day_end[n]: # lista temperature in una giornata 
            list_t.append(item[1])
            
        else:
            max_difference.append(round((max(list_t) - min(list_t)),1)) 
            n = n + 1
            list_t =[]
    
    return max_difference


class CSVTimeSeriesFile:
    
    def __init__(self, name):
        
        self.name = name
      
    def get_data(self):
        
        try:
            my_file = open(self.name, 'r')

        except:
            raise ExamException("Errore durante l'apertura del file")

        obs = []
        
        pv_epoch = -1
        
        for line in my_file:
            
            items = line.split(',')
            
            if len(items) >= 2:
                
                try:
                    items[0] = int(items[0])
                    
                except ValueError:
                    continue

                try:
                    items[1] = float(items[1])
                    
                except ValueError:
                    continue
                    
                if pv_epoch > items[0]:
                    raise ExamException("\nvalori non ordinati\n")
             
                if pv_epoch == items[0]:
                    raise ExamException("\nvalore duplicato\n")
                
                obs.append(items)
                
                pv_epoch = items[0]

        my_file.close()
        
        if len(obs)==0:
            raise ExamException("\nTutti i valori non sono formattati correttamente o file vuoto\n")
            
        return obs

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()

print(compute_daily_max_difference(time_series))