import tkinter as tk
from appempleos import JobApp
from appinmuebles import InmueblesApp
from appmotores import MotoresApp
from appvarios import VariosApp

class MainApp:
    def __init__(self, window):
        self.wind = window
        self.wind.title('Administrador de Anuncios')

        # Create a menu bar with buttons
        menu_frame = tk.Frame(self.wind)
        menu_frame.grid(row=0, column=0, columnspan=4, pady=10)
        
        self.buttons = {
            'Empleos': tk.Button(menu_frame, text='Empleos', command=self.show_empleos),
            'Inmuebles': tk.Button(menu_frame, text='Inmuebles', command=self.show_inmuebles),
            'Motores': tk.Button(menu_frame, text='Motores', command=self.show_motores),
            'Varios': tk.Button(menu_frame, text='Varios', command=self.show_varios),
        }
        
        self.buttons['Empleos'].grid(row=0, column=0)
        self.buttons['Inmuebles'].grid(row=0, column=1)
        self.buttons['Motores'].grid(row=0, column=2)
        self.buttons['Varios'].grid(row=0, column=3)

        # Placeholder for the active section
        self.current_app = None
        self.current_section = None
        self.show_empleos()

    def show_empleos(self):
        self.switch_section('Empleos', JobApp)

    def show_inmuebles(self):
        self.switch_section('Inmuebles', InmueblesApp)

    def show_motores(self):
        self.switch_section('Motores', MotoresApp)

    def show_varios(self):
        self.switch_section('Varios', VariosApp)

    def switch_section(self, section, app_class):
        if self.current_section == section:
            return
        if self.current_app:
            self.current_app.frame.destroy()
        self.current_app = app_class(self.wind)
        self.current_section = section
        
        # Disable the button for the current section and enable others
        for name, button in self.buttons.items():
            if name == section:
                button.config(state=tk.DISABLED)
            else:
                button.config(state=tk.NORMAL)

if __name__ == '__main__':
    window = tk.Tk()
    app = MainApp(window)
    window.mainloop()
