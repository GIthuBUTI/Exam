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
        # Inizializzo una lista vuota per salvare i valori
        values = []
        # Apro e leggo il file, linea per linea
        try:
            my_file = open(self.name, 'r')

        except FileNotFoundError:

            raise ExamException("Nome del file errato")
        last_epoch=-1
        for line in my_file:
            # Faccio lo split di ogni riga sulla virgola
            elements = line.split(',')
            # Se NON sto processando l’intestazione...
            if len(elements) >= 2:
                # Setto la data e il valore
                try:
                    elements[0] = int(elements[0])
                except ValueError:
                    continue

                try:
                    elements[1] = float(elements[1])
                except ValueError:
                    continue
                if last_epoch > elements[0]:
                    raise ExamException("ci sono valori non ordinati ")
                if last_epoch == elements[0]:
                    raise ExamException("ci sono valori duplicati ")
                # Aggiungo alla lista dei valori questo valore
                values.append(elements)
                last_epoch=elements[0]

        my_file.close()
        if len(values)==0:
            raise ExamException("Tutti i valori non sono formattati correttamente o file vuoto")
        return values

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
print(compute_daily_max_difference(time_series))
