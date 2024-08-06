import tkinter as tk
from tkinter import messagebox
import git
import os

# Configura tu repositorio de Git
GIT_REPO_PATH = "/home/gunnar/Documents/Tienda/tiendaivirgarzama"
HTML_FILE_PATH = os.path.join(GIT_REPO_PATH, "todoloquebuscas/empleos/trab.html")
GIT_REMOTE_NAME = "origin"
GIT_BRANCH_NAME = "main"

def add_advertisement():
    title = entry_title.get()
    date = entry_date.get()
    description = entry_description.get()
    link = entry_link.get()

    if not title or not date or not description:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    # Crear el nuevo anuncio
    new_ad = f"""
    <div class="job albañil">
        <div class="job-header">
            <h4>{title}</h4>
            <span class="job-date">Publicado: {date}</span>
        </div>
        <p>{description}</p>
        <a href="{link}" class="job-details">Ver detalles</a>
    </div>
    """

    # Añadir el anuncio al archivo HTML
    with open(HTML_FILE_PATH, "r+") as file:
        content = file.read()
        file.seek(0)
        file.write(content.replace("<!-- aquí deben introducirse los anuncios -->", f"<!-- aquí deben introducirse los anuncios -->\n{new_ad}"))

    # Automatización de Git
    repo = git.Repo(GIT_REPO_PATH)
    repo.git.add(HTML_FILE_PATH)
    repo.index.commit("Añadido nuevo anuncio")
    repo.git.push(GIT_REMOTE_NAME, GIT_BRANCH_NAME)

    messagebox.showinfo("Éxito", "Anuncio añadido exitosamente")

def create_gui():
    root = tk.Tk()
    root.title("Gestor de Anuncios")

    global entry_title, entry_date, entry_description, entry_link
    entry_title = tk.Entry(root, width=50)
    entry_date = tk.Entry(root, width=50)
    entry_description = tk.Entry(root, width=50)
    entry_link = tk.Entry(root, width=50)

    tk.Label(root, text="Título del Anuncio:").pack()
    entry_title.pack()
    tk.Label(root, text="Fecha de Publicación:").pack()
    entry_date.pack()
    tk.Label(root, text="Descripción:").pack()
    entry_description.pack()
    tk.Label(root, text="Enlace de Detalles:").pack()
    entry_link.pack()

    tk.Button(root, text="Añadir Anuncio", command=add_advertisement).pack()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
