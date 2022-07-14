'''
Funzione che prende in input una serie temporale di epoch e temperature
convertita in lista di liste di valori numerici (int/float),
e ritorna una lista di valori di tipo float che indicano l'escursione termica giornaliera.
'''

def compute_daily_max_difference(time_series):

    '''
    Creo:
    1) una lista 't_list' per salvare le temperature misurate in una giornata; 
    2) una lista 'day_start_l' per salvare gli epoch che scandiscono la mezzanotte di una giornata;
    3) una lista 'max_difference' per immagazzinare le escursioni termiche giornaliere;
    4) una variabile 'n' per iterare le giornate osservate. 
    '''
    
    t_list = [] 
    day_start_l = [] 
    max_difference = [] 
    n = 0 
    
    '''
    Itero gli elementi della serie temporale per ricavarne le escursioni termiche giornaliere
    '''
    for item in time_series:

        
        day = 86400 # salvo in day la durata di un giorno in secondi

        '''
        Calcolo l'inizio del giorno sottraendo all'epoch che sto iterando
        il modulo dell'epoch diviso per i secondi in un giorno.
        '''
        
        day_start = item[0] - item[0] % day         

        '''
        Verifico che l'inizio del giorno 
        non sia già nella 'lista day_start_l' e,
        se non è presente, lo aggiungo.
        In questo modo non ho valori ripetuti della lista.
        '''
        
        if day_start not in day_start_l: 
            day_start_l.append(day_start)
            
        '''
        Se l'epoch è minore dell'inizio del giorno successivo,
        aggiungo la rispettiva temperatura a 't_list'.
        Ho così una lista di temperature misurate in una giornata.
        '''
        
        if item[0] < day_start_l[n] + day: 
            t_list.append(item[1])

            '''
            Se abbiamo raggiunto la fine della time_series, 
            verifico che la lista di temperature contenga almeno due valori: 
            
                1) Se ne ha solo uno, aggiungo un valore nullo a 'max_difference';
                2) Se ne ha almeno due, aggiungo l'escursione termica dell'ultima giornata a 'max_difference'.
            
            L'escursione termica giornaliera la trovo sottraendo la minima temperatura
            alla massima temperatura misurate in quel giorno.
            Arrotondo il risultato a due cifre decimali.
            '''
            
            if item == time_series[-1]:
                if len(t_list) > 1:
                    max_difference.append(round(max(t_list) - min(t_list),2))
                    
                else:
                    max_difference.append(None)

            '''
            Se l'epoch è uguale all'inizio del' giorno successivo, 
            come ho fatto in precedenza, verifico la lunghezza di 't_list'
            e di conseguenza aggiungo il valore dell'escursione termica giornaliera.
            '''
        
        else:
            if len(t_list) > 1:
                max_difference.append(round(max(t_list) - min(t_list),2))
            
            else:
                max_difference.append(None)
                
            '''
            Incremento la variabile 'n' per aggiornare 'day_start'
            e svuoto la lista di temperature giornaliere.
            Così facendo, posso ricominciare a iterare sul giorno successivo.            
            '''
            n = n + 1
            t_list =[]

    '''
    Ritorno la lista delle escurioni termiche giornaliere.
    '''
    return max_difference

'''
Classe di eccezioni.
'''
class ExamException(Exception):
    pass

'''
Classe che prende in input una serie temporale in formato file.csv
e torna, tramite il metodo get_data(), una lista di liste di valori numerici
'''

class CSVTimeSeriesFile():

    '''
    Istanzio la classe sul nome del file in input
    tramite la variabile 'name'.
    '''
    
    def __init__(self, name):  
        
        self.name = name

    '''
    Metodo che ritorna una lista di liste di valori numerici,
    dove il primo elemento delle liste annidate è l’epoch e il secondo la temperatura.
    '''
    def get_data(self):

        '''
        Verifico che il nome del file sia corretto e che esista.
        In caso contrario, stampo l'errore generato
        '''
        
        try:
            my_file = open(self.name, 'r')
        
            
        except Exception as e:
            print(f'Errore generato da: {e}.')
                    
        '''
        Creo una lista vuota 'obs' per immagazzinare
        i dati del file, dopo aver verificato 
        che siano formattati correttamente,
        e una variabile 'pv_epoch' per verificare
        che gli epoch siano ordinati cronologicamente 
        e non vi siano valori doppi.        
        '''
        
        obs = []
        pv_epoch = -1

        '''
        Itero la serie temporale per ricavare i dati 
        e inserirli nella lista di liste 'obs'.
        '''
        
        for line in my_file:
            
            '''
            Suddivido la riga del file che sto iterando
            tra epoch e temperatura e li inserisco nella lista 'items'.
            '''
            
            items = line.split(',')

            '''
            Prendo in considerazione la lista 'items'
            solo se contiene almeno due elementi.
            '''
            
            if len(items) >= 2:

                '''
                Verifico che il primo elemento di 'items', l'epoch,
                sia convertibile a intero,
                il secondo elemento di 'items', la temperatura,
                sia convertibile a floating point.
                In caso contrario gestisco l'errore e continuo.
                '''
                try:
                    items[0] = int(items[0])
                    
                except ValueError as e:
                    print(f"Errore nel convertire l'epoch in intero: {e}")
                    continue

                try:
                    items[1] = float(items[1])
                    
                except ValueError as e:
                    print(f"Errore nel convertire la temperatura in floating point: {e}")
                    continue

                '''
                Verifico che gli epoch siano ordinati cronologicamente
                e che non vi siano valori doppi.
                In caso contrario, alzo un eccezione.
                '''
                
                if pv_epoch > items[0]:
                    raise ExamException("\nEpoch non ordinati cronologicamente.\n")
                    
                if pv_epoch == items[0]:
                    raise ExamException("\nEpoch duplicati.\n")

                '''
                Se la lista 'items' rispetta tutti i parametri,
                la aggiungo alla lista 'obs'.
                '''
                obs.append(items)

                ''' 
                Aggiorno la variabile 'pv_epoch'
                per continuare a verificare l'ordine degli epoch.
                '''
                
                pv_epoch = items[0]

        '''
        Chiudo il file dopo aver concluso la lista 'obs'.
        '''
        
        my_file.close()

        '''
        Se la lista 'obs' non contiene elementi,
        alzo l'eccezione.
        '''
        
        if obs == []:
            raise ExamException("\nIl file è vuoto o i dati sono scritti in modo errato.\n")
         
        return obs


time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()

print(compute_daily_max_difference(time_series))