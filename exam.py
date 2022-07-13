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
            if len(list_t) > 1:
                max_difference.append(round((max(list_t) - min(list_t)),1))
            else:
                max_difference.append(None)
            n = n + 1
            list_t =[]
    
    return max_difference
class ExamException(Exception):
    pass
class CSVFile():
    
    def __init__(self, name):  
        self.name = name
                
    def get_data(self):
        #verifico che il file esista
        try:
            my_file = open(self.name, 'r')
        #se il file non esiste stampo l'errore
        except Exception as e:
            print('File inesistente, errore: {}'.format(e))
            exit()
        #creo lista vuota
        list = []
        #apro il file
        my_file = open(self.name, 'r')
        for item in my_file:
            #divido gli elementi della lista
            elements = item.split(',')
            if elements[0] != 'epoch':   #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                #elimino l'elemento \n
                try:
                    elements[0] = int(elements[0])
                    elements[1] = float(elements[1])
                except ValueError as e:
                    print('Errore di valore in get_data() di CVSFile(): {}'.format(e))
                    
                except Exception as e:
                    print('Errore generico in get_data() di CVSFile(): {}'.format(e))
                    
                                        
                #aggiungo l'elememto modificato a list
                list.append(elements) 
        #chiudo il file
        my_file.close()
    
        return list

class CSVTimeSeriesFile(CSVFile):
    def __init__(self, name):  
        self.name = name

    def get_data(self):
        list = super().get_data()
        return list

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()

#print(time_series)
print(compute_daily_max_difference(time_series))