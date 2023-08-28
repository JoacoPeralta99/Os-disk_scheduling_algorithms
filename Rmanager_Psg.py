import PySimpleGUI as sg
from adm_methods import *    # importo los metodos de administracion y sus respectivas cargas al azar utilizando random
from random import randint
import operator

sg.theme('Dark Green 2') # estilo de la ventana

sg.popup_quick_message('espere un momento esto, tomará un poco de tiempo para crear....', auto_close=True, non_blocking=True) # mensaje de espera

MAX_ROWS, MAX_COLS, COL_HEADINGS = 1, 6, ('N°0', 'N°1', 'N°2', 'N°3', 'N°4', 'N°5',)   # aqui se puede modificar para que el input sea en multiples columnas y filas

# Nota: el " + \ " al final de las lineas se realiza debido a que manejamos listas de listas 

layout = [[sg.Text('Data entry in the sector:', font='Default 16')]] + \
         [[sg.Text(' ' * 15)] + [sg.Text(s, key=s, enable_events=True, font='Courier 14', size=(8, 1)) for i, s in enumerate(COL_HEADINGS)]] + \
         [[sg.T(r, size=(4, 1))] + [sg.Input(randint(0, 1000), justification='r', key=(r, c)) for c in range(MAX_COLS)] for r in range(MAX_ROWS)] + \
         [[sg.Text('Administration Methods:', font='Default 16')]] + \
         [[sg.Button('First Come First Served'), sg.Button('Shortest Seek Time First')]] + \
         [[sg.Button('Scan'), sg.Button('C-Scan'), sg.Button('Stacked Requests'), sg.Button('Exit')]]

# creacion de la ventana 
window = sg.Window('Request-Manager_HDD', layout, default_element_size=(12, 1), element_padding=(1, 1), return_keyboard_events=True)

current_cell = (0, 0)
while True:  # bucle
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):     # si el usuario cierra la ventana
        break
    elem = window.find_element_with_focus()
    current_cell = elem.Key if elem and type(elem.Key) is tuple else (0, 0)
    r, c = current_cell

    if event.startswith('Down'):
        r = r + 1 * (r < MAX_ROWS - 1)
    elif event.startswith('Left'):
        c = c - 1 * (c > 0)
    elif event.startswith('Right'):
        c = c + 1 * (c < MAX_COLS - 1)
    elif event.startswith('Up'):
        r = r - 1 * (r > 0)
    elif event in COL_HEADINGS:         
        col_clicked = COL_HEADINGS.index(event)
        try:
            table = [[int(values[(row, col)]) for col in range(MAX_COLS)] for row in range(MAX_ROWS)]
            new_table = sorted(table, key=operator.itemgetter(col_clicked))
        except ValueError:  # validacion de enteros 
            sg.popup_error('Error in table', 'Your table must contain only integers')
        else:
            for i in range(MAX_ROWS):
                for j in range(MAX_COLS):
                    window[(i, j)].update(new_table[i][j])
            [window[c].update(font='Any 14') for c in COL_HEADINGS]     
            window[event].update(font='Any 14 bold')                    
    # si cambia la celda actual que establezca foto en la nueva celda 
    if current_cell != (r, c):
        current_cell = r, c
        window[current_cell].set_focus()          # se establece enfoque para resaltar datos 
        window[current_cell].update(select=True)  # se utiliza para sobreescribir y generar cambios


    table = [[values[(row, col)] for col in range(MAX_COLS)] for row in range(MAX_ROWS)]
    try:
        valores = [int(num) for sublist in table for num in sublist] # transformamos la lista de lista por comprension en numeros enteros para poder manipular los datos ingresados en la interfaz grafica por el usuario
    except ValueError:  # validacion de enteros 
        sg.popup_error('Error in table', 'Your table must contain only integers')
        continue  # Salta al siguiente ciclo si la validación falla

    if event.startswith('First Come First Served'): # estos datos se traen de un random atravez de importacion de adm_methods
        table2 = fcfs(valores)  # modificacion para que tome los valores de la ventana , para tomar los valores importados de un random cambiar nombre a procesos
        sg.popup_scrolled('Requests:', '\n'.join(str(num) for num in table2), title='FCFS', font='fixedsys', keep_on_top=True)
        
    elif event.startswith('Shortest Seek Time First'): 
        table3 = sstf(valores, ultima_ubicacion)
        process_str = ', '.join(str(num) for num in table)  # Convierte la lista de procesos en una cadena
        sg.popup_scrolled('processes:',process_str, '\n'.join(str(num) for num in table3), title='SSTF', font='fixedsys', keep_on_top=True)

    elif event.startswith('Scan'):
        table4 = scan(ultima_ubicacion, valores)
        sg.popup_scrolled('\n'.join(str(num) for num in table4), title='SCAN', font='fixedsys', keep_on_top=True)

    elif event.startswith('C-Scan'): 
        table5 = c_scan(ultima_ubicacion, valores)
        sg.popup_scrolled('\n'.join(str(num) for num in table5), title='C-SCAN', font='fixedsys', keep_on_top=True)

    elif event.startswith('Stacked Requests'):
        table6 = pila(valores)
        sg.popup_scrolled('Requests:', '\n'.join(str(num) for num in table6), title='STACK', font='fixedsys', keep_on_top=True)
