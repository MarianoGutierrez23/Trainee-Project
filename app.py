from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from tkinter.ttk import Treeview
from tkcalendar import DateEntry
from sqlite3 import connect
from os import path, getlogin
from datetime import datetime

DATABASE = "BD_recepcion.db" # Para uso personal

""" Parámetros """

days_of_the_week = [
    'Lunes',
    'Martes',
    'Miércoles',
    'Jueves',
    'Viernes',
    'Sábado',
    'Domingo'
]

# Eventos para ambos elevadores
elev3_events = [
    'Balanza Tapada',
    'Camión Roto',
    'Carro Descarrilado',
    'Corte De Energía',
    'Falla De Sistema - Scada',
    'Falla De Sistema - Programas',
    'No Arranca La Cinta',
    'No Arranca Noria',
    'No Funciona Giratorio',
    'No Levanta Barrera',
    'No Mueve El Carro',
    'Otro',
    'Problema de Aspiración',
    'Problema De Calidad',
    'Problema Eléctrico',
    'Problema Gremial',
    'Problema Mecánico',
    'Problema Operativo',
    'Se Detuvo La Cinta',
    'Se Detuvo La Noria',
    'Tolva Tapada'
]

# Equipos Elevador 3
elev3_eq = [
    'A1',
    'A2',
    'A3',
    'A4',
    'A5',
    'A6',
    'AA1',
    'AA2',
    'Balanza Bruto',
    'Balanza Tara',
    'B4',
    'B5',
    'B6',
    'BB1',
    'BB2',
    'C4',
    'C5',
    'C6',
    'D1',
    'D2',
    'D3',
    'E1',
    'E2',
    'E3',
    'E4',
    'E5',
    'E6',
    'Giratorio 1',
    'Giratorio 2',
    'Giratorio 3',
    'Giratorio 4',
    'Giratorio 5',
    'Giratorio 6',
    'F1',
    'F2',
    'F3',
    'F4',
    'F5',
    'F6',
    'FF1',
    'FF2',
    'FF3',
    'FF4',
    'FF5',
    'FF6',
    'FM',
    'Otro',
    'Plat. 1',
    'Plat. 2',
    'Vía 1',
    'Vía 2',
    'Vía 3',
    'Vía 4',
    'Vía 5',
    'Vía 6'
]

# Eventos que involucran equipos
events_that_involve_eq = [
    'Balanza Tapada',
    'Carro Descarrilado',
    'Falla De Sistema - Scada',
    'No Arranca La Cinta',
    'No Arranca Noria',
    'No Funciona Giratorio',
    'No Levanta Barrera',
    'No Mueve El Carro',
    'Problema de Aspiración',
    'Problema Eléctrico',
    'Problema Mecánico',
    'Problema Operativo',
    'Se Detuvo La Cinta',
    'Se Detuvo La Noria',
    'Tolva Tapada'

]

# Equipos Elevador 5
elev5_eq = [
    'Balanza Bruto',
    'Balanza Tara',
    'CT',
    'FM',
    'FP5',
    'FP6',
    'Giratorio NE4',
    'Giratorio NR3',
    'Giratorio T11',
    'Giratorio T12',
    'NE4',
    'NR3',
    'Otro',
    'Plat. 3',
    'Plat. 4',
    'R4',
    'T11',
    'T12'    
]

""" Comienza Aplicación """

# Crear ventana

root = Tk()
root.title("Registro de demoras - Elevadores")
root.iconbitmap('Images/favicon.ico')
root.geometry("848x400")
root.maxsize(width=848, height=400)

# Crear marco izquierdo y derecho
left = Frame(root, bg='white', height=400, width=200)
left.grid(row=0,column=0)
left.grid_propagate(False)

right = Frame(root, height=400, width=648) # Usar Proporción Aurea (1,618)
right.grid(row=0,column=1)
right.grid_propagate(False)

# Logos
image1 = PhotoImage(file='Images/logo_bunge.png')
logo1 = Label(left,image=image1,bg='white',width=200).place(y=100)

image2 = PhotoImage(file='Images/Logo_tbb_azul.png')
logo2 = Label(left,image=image2, bg='white', width=200).place(y=290)

# Fuente 'negrita'
font1 = Font(weight='bold', size=9)
font2 = Font(underline=True,size=9,weight='bold')
font3 = Font(weight='bold',size=10)


def alert(title,message):
      return messagebox.showerror(title, message)


def elev_3():
    """
    Función asociada al botón "Elevador 3" para registrar eventos que suceden
    en ese elevador
    """
    def load_open_delays():

        """Carga eventos no finalizados a la tabla"""

        # https://stackoverflow.com/questions/25336726/why-cant-i-iterate-twice-over-the-same-data

        db = connect(DATABASE)
        db_cursor = db.cursor()

        data = db_cursor.execute(
            """
                SELECT id, Evento, Equipo, Fecha_inicio, Hora_inicio, Minuto_inicio
                FROM events
                WHERE Elevador = 'Elevador 3'
                AND Fecha_fin IS NULL
            """
        )
        
        # IMPORTANTE."data" es un objeto iterable que se consume una única vez
        data_list = list()
        for row in data:
            data_list.append(row)
        
        date_and_time = list()

        for row in data_list:
            date_and_time_info = row[3] + " " + str(row[4]) + " " + str(row[5])
            date_and_time_i = datetime.strptime(date_and_time_info, '%Y-%m-%d %H %M')
            date_and_time.append(date_and_time_i.strftime('%d/%m/%Y %H:%M'))
           
        cols = ('ID','Evento', 'Equipo', 'Fecha y Hora')
        open_delays = Treeview(frame_elev3_child2, columns=cols, show='headings', height=3)
        open_delays.grid(row=0, column=1, pady=34, sticky='w')
        
        open_delays.column(cols[0], width=19)
        open_delays.column(cols[1], width=115)
        open_delays.column(cols[2], width=65)
        open_delays.column(cols[3], width=100)
        
        for i in range(len(cols)):
            open_delays.heading(cols[i], text=cols[i])

        rows = list()
        i = 0
        for item in data_list:
            row = []
            row.append(item[0])
            row.append(item[1])
            row.append(item[2])
            row.append(date_and_time[i])

            rows.append(tuple(row))
            i += 1

        j = 0
        for row in rows:
            open_delays.insert(parent='', index=j, iid=j, text='', values=row)
            j += 1

        # Agregar Scrollbar
        sb = Scrollbar(frame_elev3_child2, orient='vertical')
        sb.grid(row=0,column=0)
        open_delays.config(yscrollcommand=sb.set)
        sb.config(command=open_delays.yview)

        return open_delays

    if not path.exists(DATABASE):
        alert(
            'Error',
            '''No se encuentra la base de datos. Por favor, comunicar este error''')
        
        return root.destroy()

    # Limpiar la ventana
    for widget in right.winfo_children():
        widget.destroy()
    
    button_1.config(state='normal')

    upper_frame = Frame(right, height=200, width=648)
    lower_frame = Frame(right, height=200, width=648)
    frame_elev3_child1 = Frame(upper_frame, height=200, width=324)
    frame_elev3_child2 = Frame(upper_frame, height=200, width=324)
    
    upper_frame.grid(row=0, column=0)
    upper_frame.grid_propagate(False)

    divider = Label(upper_frame,text="""
    ---------------------------------------------------------------------------------------------------------------------------
    """).place(y=120)

    lower_frame.grid(row=1, column=0)
    lower_frame.grid_propagate(False)

    frame_elev3_child1.grid(row=0, column=0)
    frame_elev3_child1.grid_propagate(False)    

    frame_elev3_child2.grid(row=0, column=1)
    frame_elev3_child2.grid_propagate(False)

    elev = Label(frame_elev3_child1,text='Elevador 3 - Plataformas del Anexo y Vías 1-2-3-4',font=font3).place(x=4, y=5)    

    open_delays = Label(frame_elev3_child2,text='Eventos sin finalizar').place(x=112,y=12)

    treeview = load_open_delays()
     
    # Button Functions

    def select_and_finish():

        def register_finish_time(id, start_date):

            data = {}

            data['fecha'] = date.get_date()
            data['hora'] = hour.get()
            data['minuto'] = minute.get()

            # Convertir fehca y hora fin en objeto "datetime"

            finish_datetime_string = str(data['fecha']) + " " + str(data['hora']) + " " + str(data['minuto'])
            finish_datetime_obj = datetime.strptime(finish_datetime_string, '%Y-%m-%d %H %M')

            # Convertir fecha y hora de inicio en objeto "datetime"

            start_datetime_obj = datetime.strptime(start_date, '%d/%m/%Y %H:%M')

            if finish_datetime_obj <= start_datetime_obj:
                return alert('Error', 'La fecha de finalización debe ser mayor a la fecha de inicio.')
            
            # Cálculo de la demora (hs.)
            delay = finish_datetime_obj - start_datetime_obj
            data['delay'] = delay.total_seconds()/3600
            
            db = connect(DATABASE)
            db_cursor = db.cursor()
            
            db_cursor.execute(
                """
                    UPDATE events
                    SET Fecha_fin = ?, Hora_fin = ?, Minuto_fin = ?, Demora = ?
                    Where id = ?
                """, (data['fecha'], data['hora'], data['minuto'], data['delay'], id)
            )

            db.commit()
            db.close()
            return elev_3()

        def activate_btn(button):
                button.config(state='normal' if check_value.get() else 'disable')
       
        def delete_event(id):
            db = connect(DATABASE)
            db_cursor = db.cursor()

            db_cursor.execute("""
                                DELETE FROM events
                                WHERE id = ?
                                
            """, [id])
            db.commit()
            db.close()
        
        if treeview.item(treeview.selection())['values']:

            for widget in lower_frame.winfo_children():
                    widget.destroy()

            # Información del evento
            selection = treeview.item(treeview.selection())['values']
            
            evento_label = Label(lower_frame,text='Evento:').grid(row=1,column=0,sticky='w',padx=[4,0])
            evento = Label(lower_frame, text=selection[1]).grid(row=1,column=1,sticky='w')

            equipo_label = Label(lower_frame, text='Equipo:').grid(row=2,column=0,sticky='w',padx=[4,0])
            equipo = Label(lower_frame,text=selection[2]).grid(row=2,column=1,sticky='w')

            fecha_inicio_label = Label(lower_frame,text='Fecha y Hora de inicio:').grid(row=3,column=0,sticky='w',padx=[4,0])
            fecha_inicio = Label(lower_frame,text=selection[3]).grid(row=3,column=1,sticky='w')

            date_label = Label(lower_frame, text='Fecha y Hora de finalización').grid(row=4,column=0,sticky='ew',pady=[10,0]) 
            
            date = DateEntry(lower_frame,showweeknumbers=False, locale='es_AR')
            date.grid(row=5,column=0, padx=[10,5], sticky='ew')

            time_auxframe1 = Frame(lower_frame)
            time_auxframe1.grid(row=5,column=1,sticky='ew')
            
            now = datetime.now()
            hours = StringVar(time_auxframe1)
            minutes = StringVar(time_auxframe1)
            
            hours.set(now.strftime('%H'))
            minutes.set(now.strftime('%M'))

            hour = Spinbox(time_auxframe1, textvariable=hours, state='readonly', from_=0, to=23, wrap=True, width=3, format="%02.0f")
            hour.grid(row=0,column=0,padx=6,sticky='ew')

            sep = Label(time_auxframe1, text=':').grid(row=0,column=1,sticky='ew',padx=[0,5])

            minute = Spinbox(time_auxframe1, textvariable=minutes, state='readonly', from_=0, to=59, wrap=True, width=3, format="%02.0f")
            minute.grid(row=0,column=2,sticky='ew')

            register_end = Button(lower_frame,text='Finalzar Evento', font=font1,command=lambda:[register_finish_time(selection[0],selection[3])])
            register_end.grid(row=6,column=0,pady=10)

            check_value = IntVar(lower_frame)
            
            checkbox = Checkbutton(lower_frame, variable=check_value, command=lambda:[activate_btn(delete_btn)]).grid(row=6, column=2)

            delete_btn = Button(lower_frame, text='Eliminar', state='disable', command=lambda:[delete_event(selection[0]), elev_3()])
            delete_btn.grid(row=6, column=1)

    def new_delay():

        # Funciones Auxiliares --- Comienzo
        def get_otro(value,var):
            var.set(value)
            if var == event:
                load_equipments(equipment)
            for widget in lower_frame.grid_slaves():
                    if int(widget.grid_info()['row']) == 1:
                        widget.grid_forget()
                        date_label = Label(lower_frame, text='Fecha y Hora').grid(row=1,column=0,sticky='ew')
                        obs_label = Label(lower_frame,text='Observaciones').grid(row=1,column=3)

        def check_otro(value,var):
            if value == 'Otro':
                for widget in lower_frame.grid_slaves():
                    if int(widget.grid_info()['row']) == 1 and int(widget.grid_info()['column']) == 0:
                        widget.grid_forget()

                if var == event:        
                    otro_label = Label(lower_frame, text='Evento:')
                elif var == equipment:
                    otro_label = Label(lower_frame, text='Equipo:')

                otro_label.grid(row=1,column=0)
                otro = Entry(lower_frame)
                otro.grid(row=1,column=1)

                get_otro_btn = Button(lower_frame,text='Ok',command=lambda:get_otro(otro.get(),var))
                get_otro_btn.grid(row=1,column=2,padx=3)
                
            else:
                for widget in lower_frame.grid_slaves():
                    if int(widget.grid_info()['row']) == 1:
                        widget.grid_forget()
                date_label = Label(lower_frame, text='Fecha y Hora').grid(row=1,column=0,sticky='ew') 
                obs_label = Label(lower_frame,text='Observaciones').grid(row=1,column=3)

        def load_equipments(equip_var):
            equip_var.set('Equipo')
            equipment_menu = OptionMenu(lower_frame, equip_var, *elev3_eq,command=lambda _:check_otro(equip_var.get(),equip_var))
            equipment_menu.grid(row=0, column=2, pady=[10, 20], sticky='ew')
    
        def check_for_equipments(event, equip_var):
        
            if event in events_that_involve_eq:
                load_equipments(equip_var)
            else:
                for widget in lower_frame.grid_slaves():
                    if int(widget.grid_info()['row']) == 0 and int(widget.grid_info()['column']) == 2:
                        widget.grid_forget()
       
        def register_delay():
        
            data = {}

            # Chequear información
    
            if event.get() == 'Evento':
                return alert('Error', 'Evento no determinado.')
            
            if event.get() == '':
                return alert('Error', 'Evento no determinado. Seleccionar nuevamente "Otro" y especificar en el espacio correspondiente.')

            if event.get() == 'Otro':
                return alert('Error', 'Por favor, especificar el nuevo evento.')

            if equipment.get() == 'Equipo' and event.get() in events_that_involve_eq:
                return alert('Error', 'Equipo no determinado.')

            if equipment.get() == 'Equipo':
                equipment.set(None)

            if not equipment.get():
                equipment.set(None)

            if equipment.get() == 'Otro':
                return alert('Error', 'Por favor, especificar el nuevo equipo.')

            if product.get() == 'Producto':
                product.set(None)

            if len(obs.get('1.0','end-1c')) < 20:
                return alert('Advertencia','El campo de Observaciones debe contener al menos 20 caracteres.')
            
            # Obtener la inforación
            data['evento'] = event.get()
            data['equipo'] = equipment.get()
            data['producción'] = product.get()
            data['fecha'] = date.get_date()
            data['día'] = days_of_the_week[date.get_date().weekday()]
            data['hora'] = hours.get()
            data['minutos'] = minutes.get()
            if '\n' in obs.get('1.0','end-1c'):
                data['obs'] = obs.get('1.0','end-1c').replace('\n',' ')
            else:
                data['obs'] = obs.get('1.0','end-1c')
            data['user'] = getlogin()
    
            sql_iterable = list()
            sql_iterable.append('Elevador 3')
            for key in data.keys():
                sql_iterable.append(data[key])

            # Cargar a la Base de Datos
            print(sql_iterable)
            db = connect(DATABASE)
            db_cursor = db.cursor()

            db_cursor.execute(
                """
                    INSERT INTO events (
                        Elevador,
                        Evento,
                        Equipo,
                        Producción,
                        Fecha_inicio,
                        Día_inicio,
                        Hora_inicio,
                        Minuto_inicio,
                        Observaciones,
                        Usuario
                    )
                    VALUES (?,?,?,?,?,?,?,?,?,?)

                """,tuple(sql_iterable)
            )

            db.commit()
            db.close()
            return elev_3()

        # Funciones Auxiliares --- Fin

        for widget in lower_frame.winfo_children():
                widget.destroy()
    
        title_new = Label(upper_frame, text='Nuevo Evento', font=font3).place(x=4,y=160)
        subtitle = Label(lower_frame, text='Seleccionar datos:').grid(row=0,column=0)
        
        event = StringVar(lower_frame)
        event.set('Evento')
        event_menu = OptionMenu(
            lower_frame, event,
            *elev3_events,
            command=lambda _:[check_for_equipments(event.get(),equipment),check_otro(event.get(),event)] # '_' para que no calleé 'event' automáticamente 
        )
        event_menu.grid(row=0,column=1,pady=[10,20], padx=[5,10], sticky='ew')

        equipment = StringVar(lower_frame)

        product = StringVar(lower_frame)
        product.set('Producto')
        product_menu = OptionMenu(lower_frame,product,'Cebada','Maíz','Soja','Trigo')
        product_menu.grid(row=0,column=3, pady=[10,20], padx=5, sticky='w')
        
        date_label = Label(lower_frame, text='Fecha y Hora').grid(row=1,column=0,sticky='ew') 
        
        date = DateEntry(lower_frame,locale='es_AR', showweeknumbers=False)
        date.grid(row=2,column=0, padx=[10,5], sticky='ew')

        time_auxframe = Frame(lower_frame)
        time_auxframe.grid(row=2,column=1,sticky='ew')
        
        now = datetime.now()
        hours = StringVar(time_auxframe)
        minutes = StringVar(time_auxframe)
        
        hours.set(now.strftime('%H'))
        minutes.set(now.strftime('%M'))

        hour = Spinbox(time_auxframe, textvariable=hours, state='readonly', from_=0, to=23, wrap=True, width=3, format="%02.0f")
        hour.grid(row=0,column=0,padx=6,sticky='ew')

        sep = Label(time_auxframe, text=':').grid(row=0,column=1,sticky='ew',padx=[0,5])

        minute = Spinbox(time_auxframe, textvariable=minutes, state='readonly', from_=0, to=59, wrap=True, width=3, format="%02.0f")
        minute.grid(row=0,column=2,sticky='ew')

        obs_label = Label(lower_frame,text='Observaciones').grid(row=1,column=3)
        obs = Text(lower_frame,height=4,width=25)
        obs.grid(row=2,column=3)

        add_event = Button(lower_frame,text='Registrar Evento', font=font1,command=register_delay)
        add_event.grid(row=3,column=3,pady=10)

    select_open_delay = Button(frame_elev3_child1, text='Seleccionar',width=18,command=select_and_finish)
    select_open_delay.grid(row=1,column=0,padx=92)
    add_new_delay = Button(frame_elev3_child1, text=' + Nuevo Evento', width=18, font=font1,command=new_delay)
    add_new_delay.grid(row=0,column=0,pady=[45,10])


def elev_5():

    def load_open_delays():

        # https://stackoverflow.com/questions/25336726/why-cant-i-iterate-twice-over-the-same-data

        db = connect(DATABASE)
        db_cursor = db.cursor()

        data = db_cursor.execute(
            """
                SELECT id, Evento, Equipo, Fecha_inicio, Hora_inicio, Minuto_inicio
                FROM events
                WHERE Elevador = 'Elevador 5'
                AND Fecha_fin IS NULL
            """
        )
        
        #IMPORTANTE!!!
        data_list = list()
        for row in data:
            data_list.append(row)
        
        date_and_time = list()

        for row in data_list:
            date_and_time_info = row[3] + " " + str(row[4]) + " " + str(row[5])
            date_and_time_i = datetime.strptime(date_and_time_info, '%Y-%m-%d %H %M')
            date_and_time.append(date_and_time_i.strftime('%d/%m/%Y %H:%M'))
           
        cols = ('ID','Evento', 'Equipo', 'Fecha y Hora')
        open_delays = Treeview(frame_elev3_child2,columns=cols,show='headings',height=3)
        open_delays.grid(row=0,column=1,pady=34,sticky='w')
        
        open_delays.column(cols[0],width=19)
        open_delays.column(cols[1],width=115)
        open_delays.column(cols[2],width=65)
        open_delays.column(cols[3],width=100)
        
        for i in range(len(cols)):
            open_delays.heading(cols[i],text=cols[i])

        rows = list()
        i = 0
        for item in data_list:
            row = []
            row.append(item[0])
            row.append(item[1])
            row.append(item[2])
            row.append(date_and_time[i])

            rows.append(tuple(row))
            i += 1

        j = 0
        for row in rows:
            open_delays.insert(parent='', index=j, iid=j, text='', values=row)
            j += 1

        # Agregar Scrollbar
        sb = Scrollbar(frame_elev3_child2, orient='vertical')
        sb.grid(row=0,column=0)
        open_delays.config(yscrollcommand=sb.set)
        sb.config(command=open_delays.yview)
    
        return open_delays

    if not path.exists(DATABASE):
        alert(
            'Error',
            '''No se encuentra la base de datos. Por favor, comunicar este error.''')   
        return root.destroy()

    # Limpiar la ventana
    for widget in right.winfo_children():
        widget.destroy()
    
    button_1.config(state='normal')

    upper_frame = Frame(right,height=200,width=648)
    lower_frame = Frame(right, height=200, width=648)
    frame_elev3_child1 = Frame(upper_frame, height=200, width=324)
    frame_elev3_child2 = Frame(upper_frame, height=200, width=324)
    
    upper_frame.grid(row=0,column=0)
    upper_frame.grid_propagate(False)

    divider = Label(upper_frame,text="""
    ---------------------------------------------------------------------------------------------------------------------------
    """).place(y=120)

    lower_frame.grid(row=1,column=0)
    lower_frame.grid_propagate(False)

    frame_elev3_child1.grid(row=0,column=0)
    frame_elev3_child1.grid_propagate(False)    

    frame_elev3_child2.grid(row=0,column=1)
    frame_elev3_child2.grid_propagate(False)

    elev = Label(frame_elev3_child1,text='Elevador 5 - Plataformas 3-4',font=font3).place(x=4, y=5)    
    open_delays = Label(frame_elev3_child2,text='Eventos sin finalizar').place(x=112,y=12)

    treeview = load_open_delays()
      
    # Button Functions

    def select_and_finish():

        def register_finish_time(id, start_date):

            data = {}

            data['fecha'] = date.get_date()
            data['hora'] = hour.get()
            data['minuto'] = minute.get()

            # Convertir fehca y hora fin en objeto "datetime"

            finish_datetime_string = str(data['fecha']) + " " + str(data['hora']) + " " + str(data['minuto'])
            finish_datetime_obj = datetime.strptime(finish_datetime_string, '%Y-%m-%d %H %M')

            # Convertir fecha y hora de inicio en objeto "datetime"

            start_datetime_obj = datetime.strptime(start_date, '%d/%m/%Y %H:%M')

            if finish_datetime_obj <= start_datetime_obj:
                return alert('Error', 'La fecha de finalización debe ser mayor a la fecha de inicio.')
            
            # Cálculo de la demora (hs.)
            delay = finish_datetime_obj - start_datetime_obj
            data['delay'] = delay.total_seconds()/3600
            
            db = connect(DATABASE)
            db_cursor = db.cursor()
            
            db_cursor.execute(
                """
                    UPDATE events
                    SET Fecha_fin = ?, Hora_fin = ?, Minuto_fin = ?, Demora = ?
                    Where id = ?
                """,(data['fecha'],data['hora'],data['minuto'],data['delay'],id)
            )

            db.commit()
            db.close()
            return elev_5()

        def activate_btn(button):
                button.config(state='normal' if check_value.get() else 'disable')
       
        def delete_event(id):
            db = connect(DATABASE)
            db_cursor = db.cursor()

            db_cursor.execute("""
                                DELETE FROM events
                                WHERE id = ?
                                
            """,[id]) 
            db.commit()
            db.close()
                    
        if treeview.item(treeview.selection())['values']:

            for widget in lower_frame.winfo_children():
                    widget.destroy()

            # Información del evento
            selection = treeview.item(treeview.selection())['values']
    
            evento_label = Label(lower_frame,text='Evento:').grid(row=1,column=0,sticky='w',padx=[4,0])
            evento = Label(lower_frame, text=selection[1]).grid(row=1,column=1,sticky='w')

            equipo_label = Label(lower_frame, text='Equipo:').grid(row=2,column=0,sticky='w',padx=[4,0])
            equipo = Label(lower_frame,text=selection[2]).grid(row=2,column=1,sticky='w')

            fecha_inicio_label = Label(lower_frame,text='Fecha y Hora de inicio:').grid(row=3,column=0,sticky='w',padx=[4,0])
            fecha_inicio = Label(lower_frame,text=selection[3]).grid(row=3,column=1,sticky='w')

            date_label = Label(lower_frame, text='Fecha y Hora de finalización').grid(row=4,column=0,sticky='ew',pady=[10,0]) 
            
            date = DateEntry(lower_frame,showweeknumbers=False, locale='es_AR')
            date.grid(row=5,column=0, padx=[10,5], sticky='ew')

            time_auxframe1 = Frame(lower_frame)
            time_auxframe1.grid(row=5,column=1,sticky='ew')
            
            now = datetime.now()
            hours = StringVar(time_auxframe1)
            minutes = StringVar(time_auxframe1)
            
            hours.set(now.strftime('%H'))
            minutes.set(now.strftime('%M'))

            hour = Spinbox(time_auxframe1, textvariable=hours, state='readonly', from_=0, to=23, wrap=True, width=3, format="%02.0f")
            hour.grid(row=0,column=0,padx=6,sticky='ew')

            sep = Label(time_auxframe1, text=':').grid(row=0,column=1,sticky='ew',padx=[0,5])

            minute = Spinbox(time_auxframe1, textvariable=minutes, state='readonly', from_=0, to=59, wrap=True, width=3, format="%02.0f")
            minute.grid(row=0,column=2,sticky='ew')

            register_end = Button(lower_frame,text='Finalzar Evento', font=font1,command=lambda:[register_finish_time(selection[0],selection[3])])
            register_end.grid(row=6,column=0,pady=10)

            check_value = IntVar(lower_frame)
            
            checkbox = Checkbutton(lower_frame, variable=check_value, command=lambda:[activate_btn(delete_btn)]).grid(row=6, column=2)
            
            delete_btn = Button(lower_frame, text='Eliminar', state='disable', command=lambda:[delete_event(selection[0]), elev_5()])
            delete_btn.grid(row=6, column=1)

    def new_delay():

        # Funciones Auxiliares --- Comienzo
        
        def get_otro(value,var):
            var.set(value)
            if var == event:
                load_equipments(equipment)
            for widget in lower_frame.grid_slaves():
                    if int(widget.grid_info()['row']) == 1:
                        widget.grid_forget()
                        date_label = Label(lower_frame, text='Fecha y Hora').grid(row=1,column=0,sticky='ew')
                        obs_label = Label(lower_frame,text='Observaciones').grid(row=1,column=3)

        def check_otro(value,var):
            if value == 'Otro':
                for widget in lower_frame.grid_slaves():
                    if int(widget.grid_info()['row']) == 1 and int(widget.grid_info()['column']) == 0:
                        widget.grid_forget()
                
                if var == event:        
                    otro_label = Label(lower_frame, text='Evento:')
                elif var == equipment:
                    otro_label = Label(lower_frame, text='Equipo:')
                otro_label.grid(row=1,column=0)
                otro = Entry(lower_frame)
                otro.grid(row=1,column=1)

                get_otro_btn = Button(lower_frame,text='Ok',command=lambda:get_otro(otro.get(),var))
                get_otro_btn.grid(row=1,column=2,padx=3)
                
            else:
                for widget in lower_frame.grid_slaves():
                    if int(widget.grid_info()['row']) == 1:
                        widget.grid_forget()
                date_label = Label(lower_frame, text='Fecha y Hora').grid(row=1,column=0,sticky='ew')
                obs_label = Label(lower_frame,text='Observaciones').grid(row=1,column=3)         
        
        def load_equipments(equip_var):
            
            equip_var.set('Equipo')
            equipment_menu = OptionMenu(lower_frame, equip_var, *elev5_eq, command=lambda _:check_otro(equip_var.get(),equip_var))
            equipment_menu.grid(row=0,column=2,pady=[10,20],sticky='ew')
    
        def check_for_equipments(event,equip_var):
        
            if event in events_that_involve_eq:
                load_equipments(equip_var)
            else:
                for widget in lower_frame.grid_slaves():
                    if int(widget.grid_info()['row']) == 0 and int(widget.grid_info()['column']) == 2:
                        widget.grid_forget()
       
        def register_delay():
        
            data = {}

            # Chequear información

            if event.get() == 'Evento':
                return alert('Error', 'Evento no determinado.')

            if event.get() == '':
                return alert('Error', 'Evento no determinado. Seleccionar nuevamente "Otro" y especificar en el espacio correspondiente.')
                
            if event.get() == 'Otro':
                return alert('Error', 'Por favor, especificar el nuevo evento.')

            if equipment.get() == 'Equipo' and event.get() in events_that_involve_eq:
                return alert('Error', 'Equipo no determinado.')

            if equipment.get() == 'Equipo':
                equipment.set(None)

            if not equipment.get():
                equipment.set(None)

            if equipment.get() == 'Otro':
                return alert('Error', 'Por favor, especificar el nuevo equipo.')

            if product.get() == 'Producto':
                product.set('None')

            if len(obs.get('1.0','end-1c')) < 20:
                return alert('Advertencia','El campo de Observaciones debe contener al menos 20 caracteres.')

            # Obtener la inforación
            data['evento'] = event.get()
            data['equipo'] = equipment.get()
            data['producción'] = product.get()
            data['fecha'] = date.get_date()
            data['día'] = days_of_the_week[date.get_date().weekday()]
            data['hora'] = hours.get()
            data['minutos'] = minutes.get()
            if '\n' in obs.get('1.0','end-1c'):
                data['obs'] = obs.get('1.0','end-1c').replace('\n',' ')
            else:
                data['obs'] = obs.get('1.0','end-1c')
            data['user'] = getlogin()

            sql_iterable = list()
            sql_iterable.append('Elevador 5')
            for key in data.keys():
                sql_iterable.append(data[key])

            # Cargar a la Base de Datos

            db = connect(DATABASE)
            db_cursor = db.cursor()

            db_cursor.execute(
                """
                    INSERT INTO events (
                        Elevador,
                        Evento,
                        Equipo,
                        Producción,
                        Fecha_inicio,
                        Día_inicio,
                        Hora_inicio,
                        Minuto_inicio,
                        Observaciones,
                        Usuario
                    )
                    VALUES (?,?,?,?,?,?,?,?,?,?)

                """,tuple(sql_iterable)
            )

            db.commit()
            db.close()
            return elev_5()

        # Funciones Auxiliares --- Fin

        for widget in lower_frame.winfo_children():
                widget.destroy()

        title_new = Label(upper_frame, text='Nuevo Evento', font=font3).place(x=4,y=160)

        subtitle = Label(lower_frame, text='Seleccionar datos:').grid(row=0,column=0)

        event = StringVar(lower_frame)
        event.set('Evento')
        event_menu = OptionMenu(
            lower_frame, event,
            *elev3_events,
            command=lambda _:[check_for_equipments(event.get(),equipment),check_otro(event.get(),event)] # '_' para que no calleé 'event' automáticamente 
        )
        event_menu.grid(row=0,column=1,pady=[10,20], padx=[5,10], sticky='ew')

        equipment = StringVar(lower_frame)

        product = StringVar(lower_frame)
        product.set('Producto')
        product_menu = OptionMenu(lower_frame,product,'Cebada','Maíz','Soja','Trigo')
        product_menu.grid(row=0,column=3, pady=[10,20], padx=5, sticky='w')
        
        date_label = Label(lower_frame, text='Fecha y Hora').grid(row=1,column=0,sticky='ew') 
        
        date = DateEntry(lower_frame,locale='es_AR', showweeknumbers=False)
        date.grid(row=2,column=0, padx=[10,5], sticky='ew')

        time_auxframe = Frame(lower_frame)
        time_auxframe.grid(row=2,column=1,sticky='ew')
        
        now = datetime.now()
        hours = StringVar(time_auxframe)
        minutes = StringVar(time_auxframe)
        
        hours.set(now.strftime('%H'))
        minutes.set(now.strftime('%M'))

        hour = Spinbox(time_auxframe, textvariable=hours, state='readonly', from_=0, to=23, wrap=True, width=3, format="%02.0f")
        hour.grid(row=0,column=0,padx=6,sticky='ew')

        sep = Label(time_auxframe, text=':').grid(row=0,column=1,sticky='ew',padx=[0,5])

        minute = Spinbox(time_auxframe, textvariable=minutes, state='readonly', from_=0, to=59, wrap=True, width=3, format="%02.0f")
        minute.grid(row=0,column=2,sticky='ew')

        obs_label = Label(lower_frame,text='Observaciones').grid(row=1,column=3)
        obs = Text(lower_frame,height=4,width=25)
        obs.grid(row=2,column=3)

        add_event = Button(lower_frame,text='Registrar Evento', font=font1,command=register_delay)
        add_event.grid(row=3,column=3,pady=10)
    
    select_open_delay = Button(frame_elev3_child1, text='Seleccionar',width=18,command=select_and_finish)
    select_open_delay.grid(row=1,column=0,padx=92)
    add_new_delay = Button(frame_elev3_child1, text=' + Nuevo Evento', width=18, font=font1,command=new_delay)
    add_new_delay.grid(row=0,column=0,pady=[45,10])

def button_1_onclick():
    # Limpiar la ventana
    for widget in right.winfo_children():
        widget.destroy()

    # Crear el nuevo frame
    frame_1 = Frame(right, height=500, width=809)
    frame_1.grid(row=0, column=0, padx=40)
    frame_1.grid_propagate(False)

    # Etiqueta
    elev_label = Label(frame_1, text='Seleccione un sector.').place(x=0, y=15)
    
    # Elevadores
    elev3_button = Button(frame_1, text='Elevador 3',width=20,command=elev_3).grid(row=0,column=0, pady=[45,10], padx=7 ,sticky='ew')
    elev5_button = Button(frame_1, text='Elevador 5',width=20, command=elev_5).grid(row=1,column=0, padx=7)
    
    # Desactivar el botón para evitar que se refresquen las entries
    button_1.config(state='disable')
        
# Botones principales

button_1 = Button(left, text='Inicio',width=15, command=button_1_onclick)

button_1.grid(row=0, column=0,padx=42,pady=[15,0], sticky="ew")

root.mainloop()