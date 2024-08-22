import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import git
import sqlite3
import datetime
import threading
import time

class MotoresApp:
    db_name = 'databasemotors.db'  # Change this for each section

    def __init__(self, window):
        # Creating a Frame Container
        self.frame = tk.LabelFrame(window, text='Registrar nuevo anuncio')
        self.frame.grid(row=1, column=0, columnspan=3, pady=30)

        # Fecha de publicación Input
        tk.Label(self.frame, text='Fecha de Publicación* (YYYY-MM-DD)*: ').grid(row=1, column=0)
        self.fechainicio = tk.Entry(self.frame)
        self.fechainicio.focus()
        self.fechainicio.grid(row=1, column=1)

        # Fecha de conclusión Input
        tk.Label(self.frame, text='Fecha de Conclución* (YYYY-MM-DD)*: ').grid(row=2, column=0)
        self.fechaconclution = tk.Entry(self.frame)
        self.fechaconclution.grid(row=2, column=1)

        # Tipo de anuncio Input
        tk.Label(self.frame, text='Tipo de anuncio*: ').grid(row=3, column=0)
        self.tipo = ttk.Combobox(self.frame, values=[], state="readonly")
        self.tipo.grid(row=3, column=1)
        self.tipo.bind("<<ComboboxSelected>>", self.on_type_selected)

        # Cargar tipos de anuncios desde la base de datos
        self.load_ad_types()

        # Título del anuncio Input
        tk.Label(self.frame, text='Título del anuncio: ').grid(row=4, column=0)
        self.titulo = tk.Entry(self.frame)
        self.titulo.grid(row=4, column=1)

        # Anuncio Input
        tk.Label(self.frame, text='Descripción*: ').grid(row=5, column=0)
        self.anuncio = tk.Entry(self.frame)
        self.anuncio.grid(row=5, column=1)

        # Detalles Input
        tk.Label(self.frame, text='Enlace de Detalles: ').grid(row=6, column=0)
        self.detalles = tk.Entry(self.frame)
        self.detalles.grid(row=6, column=1)

        # Button Add Product
        ttk.Button(self.frame, text='Guardar Anuncio', command=self.add_product).grid(row=7, columnspan=2, sticky=tk.W + tk.E)

        # Output Messages
        self.message = tk.Label(self.frame, text='', fg='red')
        self.message.grid(row=8, column=0, columnspan=2, sticky=tk.W + tk.E)

        # Table
        self.tree = ttk.Treeview(self.frame, height=10, columns=('col1', 'col2', 'col3'))
        self.tree.grid(row=9, column=0, columnspan=2)
        self.tree.heading('#0', text='Fecha de publicación', anchor=tk.CENTER)
        self.tree.heading('#1', text='Fecha de conclusión', anchor=tk.CENTER)
        self.tree.heading('#2', text='Tipo de anuncio', anchor=tk.CENTER)
        self.tree.heading('#3', text='Título del anuncio', anchor=tk.CENTER)

        # Buttons
        ttk.Button(self.frame, text='Eliminar', command=self.delete_product).grid(row=10, column=0, sticky=tk.W + tk.E)
        ttk.Button(self.frame, text='Actualizar anuncios', command=self.update_html_file).grid(row=10, column=1, sticky=tk.W + tk.E)

        # Filling the Rows
        self.get_products()

        # Start cleanup thread
        cleanup_thread = threading.Thread(target=self.schedule_cleanup)
        cleanup_thread.daemon = True
        cleanup_thread.start()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def load_ad_types(self):
        query = "SELECT DISTINCT tipo FROM product ORDER BY tipo ASC"
        db_rows = self.run_query(query)
        ad_types = [row[0] for row in db_rows]
        ad_types.append("Agregar tipo...")  # Mantener la opción de agregar un nuevo tipo
        self.tipo['values'] = ad_types

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

    def on_type_selected(self, event):
        if self.tipo.get() == "Agregar tipo...":
            new_type = tk.simpledialog.askstring("Nuevo tipo de anuncio", "Ingrese el nuevo tipo de anuncio:")
            if new_type:
                new_type = new_type.replace(" ", "_")
                self.tipo['values'] = list(self.tipo['values'])[:-1] + [new_type, "Agregar tipo..."]
                self.tipo.set(new_type)

    def validate_date_format(self, date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

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
            self.tipo.set("")
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

    def clean_expired_ads(self):
        query = "DELETE FROM product WHERE date(fechaconclution) < date('now')"
        self.run_query(query)

    def schedule_cleanup(self):
        while True:
            self.clean_expired_ads()
            time.sleep(3600)  # Espera 1 hora

    def update_html_file(self):
        # Limpieza de anuncios expirados antes de actualizar el HTML
        self.clean_expired_ads()

        # Selecciona solo los anuncios cuya fecha de publicación es hoy o anterior
        query = "SELECT fechainicio, fechainicio, tipo, titulo, anuncio, detalles FROM product WHERE date(fechainicio) <= date('now')"
        db_rows = self.run_query(query)

        # Crear el contenido de los anuncios y los tipos
        ads_content = ""
        job_types = {}
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
            job_type = row[2]
            if job_type in job_types:
                job_types[job_type] += 1
            else:
                job_types[job_type] = 1

        # Sobrescribir la sección de anuncios en el archivo HTML
        HTML_FILE_PATH = "/home/gunnar/Documents/Tienda/tiendaivirgarzama/todoloquebuscas/motores/motors.html"
        with open(HTML_FILE_PATH, "r") as file:
            content = file.read()

        # Actualizar los filtros en el HTML
        start_filters = "<!-- inicio de filtros -->"
        end_filters = "<!-- fin de filtros -->"
        filters_content = "<li><a href=\"#\" onclick=\"filterJobs('all')\">Todos <span id=\"all-count\"></span></a></li>\n"
        for job_type, count in job_types.items():
            filters_content += f"<li><a href=\"#\" onclick=\"filterJobs('{job_type}')\">{job_type.replace('_', ' ')} <span id=\"{job_type}-count\"></span></a></li>\n"
        # Reemplazar la sección de filtros
        before_filters = content.split(start_filters)[0]
        after_filters = content.split(end_filters)[1]
        new_content = f"{before_filters}{start_filters}\n{filters_content}{end_filters}{after_filters}"

        # Actualizar la sección de anuncios en el HTML
        start_marker = "<!-- aquí deben introducirse los anuncios -->"
        end_marker = "<!-- fin de anuncios -->"
        before_ads = new_content.split(start_marker)[0]
        after_ads = new_content.split(end_marker)[1]
        final_content = f"{before_ads}{start_marker}\n{ads_content}\n{end_marker}{after_ads}"

        # Escribir el nuevo contenido en el archivo HTML
        with open(HTML_FILE_PATH, "w") as file:
            file.write(final_content)

        # Actualizar el JavaScript
        JS_FILE_PATH = "/home/gunnar/Documents/Tienda/tiendaivirgarzama/todoloquebuscas/motores/trab.js"
        with open(JS_FILE_PATH, "r") as file:
            content = file.read()

        # Actualizar las cuentas en el JavaScript
        start_js = "// aquí se agregan los nuevos tipos"
        end_js = "// fin de los nuevos tipos"
        js_content = ""
        for job_type in job_types:
            js_content += f"const {job_type}Jobs = document.querySelectorAll('.job.{job_type}').length;\n"
            js_content += f"document.getElementById('{job_type}-count').textContent = `(${{{job_type}Jobs}})`;\n"
        # Reemplazar la sección de JavaScript dentro de `updateCounts`
        before_js = content.split(start_js)[0]
        after_js = content.split(end_js)[1]
        new_js_content = f"{before_js}{start_js}\n{js_content}{end_js}{after_js}"

        # Escribir el nuevo contenido en el archivo JavaScript
        with open(JS_FILE_PATH, "w") as file:
            file.write(new_js_content)

        # Automatización de Git
        GIT_REPO_PATH = "/home/gunnar/Documents/Tienda/tiendaivirgarzama"
        GIT_REMOTE_NAME = "origin"
        GIT_BRANCH_NAME = "main"
        repo = git.Repo(GIT_REPO_PATH)
        repo.git.add(HTML_FILE_PATH)
        repo.git.add(JS_FILE_PATH)
        repo.index.commit("Actualización de anuncios y tipos desde la base de datos")
        repo.git.push(GIT_REMOTE_NAME, GIT_BRANCH_NAME)

        messagebox.showinfo("Éxito", "Archivo HTML y JavaScript actualizados exitosamente")
