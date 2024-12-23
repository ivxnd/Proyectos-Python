import json
import os
from Task import Task  # Asumimos que la clase Task está en el archivo Task.py

class TaskManager:
    def __init__(self, fichero_tareas="tareas.json"):
        self.__fichero_tareas = fichero_tareas
        self.__tareas = []
        self.crear_archivo()
        
    #Crea el archivo JSON si no existe
    def crear_archivo(self):
        
        if not os.path.exists(self.__fichero_tareas):
            print(f"El archivo '{self.__fichero_tareas}' no existe. Creándolo...")
            with open(self.__fichero_tareas, 'w') as archivo:
                json.dump([], archivo)  # Inicializar con una lista vacía
            print(f"Archivo '{self.__fichero_tareas}' creado correctamente.")
        
        self.cargar_tareas()  # Cargamos las tareas existentes
        
    #Carga las tareas desde el archivo JSON
    def cargar_tareas(self):
        
        try:
            
            with open(self.__fichero_tareas, "r") as archivo:
                datos_tareas = json.load(archivo)
                self.__tareas = [Task.from_dict(tarea) for tarea in datos_tareas]
                
        except json.JSONDecodeError:
            print("El archivo JSON está vacío o no tiene un formato válido. Iniciando una lista vacía.")
        except Exception as e:
            print(f"Error inesperado al cargar las tareas: {e}")
        
    #Guarda las tareas en el archivo JSON
    def guardar_tareas(self):

        try:
            datos_tareas = [tarea.to_dict() for tarea in self.__tareas]
            with open(self.__fichero_tareas, 'w') as archivo:
                json.dump(datos_tareas, archivo, indent=4)
        except Exception as e:
            print(f"Error al guardar las tareas: {e}")

    def add_tarea(self, descripcion):
        
        #Añade una nueva tarea con la descripción proporcionada.
        try:
            nueva_tarea = Task(descripcion)
            self.__tareas.append(nueva_tarea)
            self.guardar_tareas()
            print(f"Tarea añadida correctamente! (ID: {nueva_tarea.get_id()})")
        except Exception as e:
            print(f"Error al añadir la tarea: {e}")
            
    # Actualizar tarea
    def update_tarea(self, id, nueva_descripcion):
        try:
            
            if not self.comprobar_tareas():
                return
            
            # Buscar la tarea por ID
            tarea = self.comprobar_id(id)
            
            tarea.set_description(nueva_descripcion)
            self.guardar_tareas()
            print(f'Tarea con ID: {id} actualizada correctamente!')
        
        except ValueError as e:
            print(f'Error al actualizar la tarea: {e}')
    
    #Borrar una tarea        
    def borrar_tarea(self, id):
        try:
            
            if not self.comprobar_tareas():
                return
            
            # Buscar la tarea por ID
            tarea = self.comprobar_id(id)
            
            self.__tareas.remove(tarea)
            self.guardar_tareas()
            print(f'Tarea con ID: {id} borrada correctamente!')
            
        except ValueError as e:
            print(f'Error al eliminar la tarea: {e}')
    
    #Actualizar el estado de una tarea por ID        
    def update_status(self, command, id):
        
        try:
            
            if not self.comprobar_tareas():
                return
            
            # Buscar la tarea por ID
            tarea = self.comprobar_id(id)
            
            # Mapear comandos a estados
            if command == 'mark-in-progress':
                tarea.set_status('In Progress')
            elif command == 'mark-todo':
                tarea.set_status('To do')
            elif command == 'mark-done':
                tarea.set_status('Done')
            else:
                print(f"Comando '{command}' incorrecto.")
                return
            
            self.guardar_tareas()
            print(f"El estado de la tarea con ID {id} ha sido actualizado a '{tarea.get_status()}'.")
        
        except ValueError as e:
            print(f'Error al actualizar el status de la tarea: {e}')
    
    #Mostrar todas las tareas        
    def mostrar_tareas(self):
        
        try:
            if not self.comprobar_tareas():
                return
        
            print("Mostrando todas las tareas:")
            
            for t in self.__tareas:
                print(t.__str__())
                
        except Exception as e:
            print(f'Error al mostrar las tareas: {e}')
            
    def mostrar_tareas_byStatus(self, status=None):
        
        try:
            if not self.comprobar_tareas():
                return
            
            # Mapeo de estados aceptados
            estado_mapeo = {
                "todo": "To do",
                "to do": "To do",
                "in-progress": "In progress",
                "in progress": "In progress",
                "done": "Done"
            }

            if status:
                # Normalizar el estado proporcionado
                status_normalizado = estado_mapeo.get(status.lower())
                
                if not status_normalizado:
                    print(f"Estado '{status}' no reconocido. Estados válidos: {', '.join(estado_mapeo.keys())}")
                    return

                print(f"Mostrando tareas con estado '{status_normalizado}':")
                tareas_filtradas = [tarea for tarea in self.__tareas if tarea.get_status() == status_normalizado]
                
                if not tareas_filtradas:
                    print(f"No hay tareas con el estado '{status_normalizado}'.")
                    return

                for tarea in tareas_filtradas:
                    print(tarea.__str__())
                    
            else: 
                self.mostrar_tareas()
                    
        except Exception as e:
            print(f'Error al mostrar las tareas por estado: {e}')
            
    def comprobar_tareas(self):
        
        if not self.__tareas:
            print("No hay tareas disponibles")
            return False
        
        return True
    
    def comprobar_id(self, id):

        # Verifica si una tarea con el ID proporcionado existe en la lista de tareas.
        # Si la encuentra devuelve la tarea, pero si no, devuelve None
        
        tarea = next((tarea for tarea in self.__tareas if tarea.get_id() == id), None)
        if not tarea:
            raise ValueError(f"No se encontró ninguna tarea con el ID: {id}")
        return tarea

        
        

                    