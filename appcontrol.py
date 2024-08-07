import tkinter as tk
from tkinter import messagebox, ttk
import git
#import os
import sqlite3
import datetime
import threading
import time

class JobApp:
    # Connection dir property
    db_name = 'database.db'

    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.title('Administrador de Anuncios')

        # Creating a Frame Container 
        frame = tk.LabelFrame(self.wind, text='Registrar nuevo anuncio')
        frame.grid(row=0, column=0, columnspan=3, pady=30)

        # Fecha de publicación Input
        tk.Label(frame, text='Fecha de Publicación* (YYYY-MM-DD)*: ').grid(row=1, column=0)
        self.fechainicio = tk.Entry(frame)
        self.fechainicio.focus()
        self.fechainicio.grid(row=1, column=1)

        # Fecha de conclusión Input
        tk.Label(frame, text='Fecha de Conclución* (YYYY-MM-DD)*: ').grid(row=2, column=0)
        self.fechaconclution = tk.Entry(frame)
        self.fechaconclution.grid(row=2, column=1)

        # Tipo de anuncio Input
        tk.Label(frame, text='Tipo de anuncio*: ').grid(row=3, column=0)
        self.tipo = tk.Entry(frame)
        self.tipo.grid(row=3, column=1)

        # Título del anuncio Input
        tk.Label(frame, text='Título del anuncio: ').grid(row=4, column=0)
        self.titulo = tk.Entry(frame)
        self.titulo.grid(row=4, column=1)

        # Anuncio Input
        tk.Label(frame, text='Descripción*: ').grid(row=5, column=0)
        self.anuncio = tk.Entry(frame)
        self.anuncio.grid(row=5, column=1)

        # Detalles Input
        tk.Label(frame, text='Enlace de Detalles: ').grid(row=6, column=0)
        self.detalles = tk.Entry(frame)
        self.detalles.grid(row=6, column=1)

        # Button Add Product 
        ttk.Button(frame, text='Guardar Anuncio', command=self.add_product).grid(row=7, columnspan=2, sticky=tk.W + tk.E)

        # Output Messages 
        self.message = tk.Label(text='', fg='red')
        self.message.grid(row=7, column=0, columnspan=2, sticky=tk.W + tk.E)

        # Table
        self.tree = ttk.Treeview(height=10, columns=('col1', 'col2', 'col3'))
        self.tree.grid(row=8, column=0, columnspan=2)
        self.tree.heading('#0', text='Fecha de publicación', anchor=tk.CENTER)
        self.tree.heading('#1', text='Fecha de conclusión', anchor=tk.CENTER)
        self.tree.heading('#2', text='Tipo de anuncio', anchor=tk.CENTER)
        self.tree.heading('#3', text='Título del anuncio', anchor=tk.CENTER)

        # Buttons
        ttk.Button(text='Eliminar', command=self.delete_product).grid(row=9, column=0, sticky=tk.W + tk.E)
        ttk.Button(text='Actualizar anuncios', command=self.update_html_file).grid(row=9, column=1, sticky=tk.W + tk.E)

        # Filling the Rows
        self.get_products()

    # Function to Execute Database Queries
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get Products from Database
    def get_products(self):
        # cleaning Table 
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM product ORDER BY fechainicio DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=(row[2], row[3], row[4]))

    def validate_date_format(self, date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    # Validación de la entrada del usuario
    def validation(self):
        if not self.validate_date_format(self.fechainicio.get()):
            messagebox.showerror("Error", "La Fecha de Publicación debe estar en el formato YYYY-MM-DD")
            return False
        if not self.validate_date_format(self.fechaconclution.get()):
            messagebox.showerror("Error", "La Fecha de Conclución debe estar en el formato YYYY-MM-DD")
            return False
        if len(self.tipo.get()) == 0 or len(self.anuncio.get()) == 0:
            messagebox.showerror("Error", "Los campos con * son obligatorios")
            return False
        return True

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?, ?, ?, ?, ?)'
            parameters = (self.fechainicio.get(), self.fechaconclution.get(), self.tipo.get(), self.titulo.get(), self.anuncio.get(), self.detalles.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Anuncio {} agregado satisfactoriamente'.format(self.titulo.get())
            self.fechainicio.delete(0, tk.END)
            self.fechaconclution.delete(0, tk.END)
            self.tipo.delete(0, tk.END)
            self.titulo.delete(0, tk.END)
            self.anuncio.delete(0, tk.END)
            self.detalles.delete(0, tk.END)
        else:
            self.message['text'] = 'Los items en * son obligatorios'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
            selected_item = self.tree.selection()[0]
            titulo = self.tree.item(selected_item)['values'][2]
        except IndexError as e:
            self.message['text'] = 'Por favor, seleccione un registro'
            return
        query = 'DELETE FROM product WHERE titulo = ?'
        self.run_query(query, (titulo,))
        self.message['text'] = 'Registro {} fue eliminado'.format(titulo)
        self.get_products()

    # Método para limpiar anuncios expirados de la base de datos
    def clean_expired_ads(self):
        query = "DELETE FROM product WHERE date(fechaconclution) < date('now')"
        self.run_query(query)

    # Método para ejecutar periódicamente la limpieza y actualización
    def schedule_cleanup(self):
        while True:
            self.clean_expired_ads()
            time.sleep(3600) # Espera 1 hora

    # Método para actualizar el archivo HTML basado en la base de datos
    def update_html_file(self):
        # Limpieza de anuncios expirados antes de actualizar el HTML
        self.clean_expired_ads()
        query = "SELECT fechainicio, fechainicio, tipo, titulo, anuncio, detalles FROM product"
        db_rows = self.run_query(query)
        # Crear el contenido de los anuncios
        ads_content = ""
        for row in db_rows:
            ads_content += f"""
            <div class="job {row[2]}">
                <div class="job-header">
                    <h4>{row[3]}</h4>
                    <span class="job-date">Publicado: {row[0]}</span>
                </div>
                <p>{row[4]}</p>
                <a href="{row[5]}" class="job-details">Ver detalles</a>
            </div>
            """

        # Añadir el anuncio al archivo HTML
        HTML_FILE_PATH = "/home/gunnar/Documents/Tienda/tiendaivirgarzama/todoloquebuscas/empleos/trab.html"
        with open(HTML_FILE_PATH, "r+") as file:
            content = file.read()
            file.seek(0)
            updated_content = content.split("<!-- aquí deben introducirse los anuncios -->")
            file.write(f"{updated_content[0]}<!-- aquí deben introducirse los anuncios -->\n{ads_content}\n{updated_content[1]}")
        
        # Automatización de Git
        GIT_REPO_PATH = "/home/gunnar/Documents/Tienda/tiendaivirgarzama"
        GIT_REMOTE_NAME = "origin"
        GIT_BRANCH_NAME = "main"
        repo = git.Repo(GIT_REPO_PATH)
        repo.git.add(HTML_FILE_PATH)
        repo.index.commit("Actualizado el archivo HTML con los anuncios actuales")
        repo.git.push(GIT_REMOTE_NAME, GIT_BRANCH_NAME)

        messagebox.showinfo("Éxito", "Archivo HTML actualizado exitosamente con anuncios actuales")

if __name__ == '__main__':
    # Inicia la limpieza periódica en un hilo separado
    window = tk.Tk()
    application = JobApp(window)
    cleanup_thread = threading.Thread(target=application.schedule_cleanup)
    cleanup_thread.daemon = True
    cleanup_thread.start()

    # Inicializa la interfaz gráfica
    window.mainloop()
