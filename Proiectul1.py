import cmath
import math
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image, ImageTk

def ComplexToString(z):
    x = round(z.real, 3)
    y = round(z.imag, 3)
    if y == 0:
        return f"{x:g}"
    if x == 0:
        return f"{y:g}j"
    return f"{x:g}{y:+g}j"

def Radix3(w):
    rho, theta = cmath.polar(w)
    return [cmath.rect(math.pow(rho, 1 / 3), (theta + 2 * k * math.pi) / 3) for k in range(3)]

def RezolvareEcuatie(a, b, c, d):
    assert a != 0, "Coeficientul a nu trebuie să fie zero"

    p = c / a - b * b / (3.0 * a * a)
    q = 2.0 * b ** 3 / (27.0 * a ** 3) - b * c / (3.0 * a * a) + d / a
    Delta = q * q + 4.0 * p ** 3 / 27.0

    w = (-q + cmath.sqrt(Delta)) / 2

    radacini = []
    for u in Radix3(w):
        z = u - p / (3 * u)
        z -= b / (3.0 * a)
        radacini.append(ComplexToString(z))

    return radacini

def plot_function(a_b_c_d_list, ax, xlim=None, ylim=None):
    ax.clear()
    if xlim is None:
        xlim = (-10, 10)
    if ylim is None:
        ylim = (-100, 100)

    x = [i / 100.0 for i in range(int(xlim[0] * 100), int(xlim[1] * 100))]

    for a, b, c, d in a_b_c_d_list:
        y = [a * xi ** 3 + b * xi ** 2 + c * xi + d for xi in x]
        ax.plot(x, y, label=f'{a}x^3 + {b}x^2 + {c}x + {d}')

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    ax.legend()
    ax.figure.canvas.draw()

def update_plot(*args):
    try:
        a = complex(entry_a.get())
        b = complex(entry_b.get())
        c = complex(entry_c.get())
        d = complex(entry_d.get())
        plot_function([(a, b, c, d)], ax)

        try:
            radacini = RezolvareEcuatie(a, b, c, d)
            label_roots.config(text=f'Rădăcinile sunt: {", ".join(radacini)}', style='Success.TLabel')
        except AssertionError as e:
            label_roots.config(text=str(e), style='Error.TLabel')
        except Exception as e:
            label_roots.config(text=f"Eroare la rezolvarea ecuației: {str(e)}", style='Error.TLabel')
    except ValueError:
        label_roots.config(text="Coeficienții trebuie să fie numere complexe valide.", style='Error.TLabel')
    except Exception as e:
        label_roots.config(text=f"Eroare: {str(e)}", style='Error.TLabel')

def save_to_history(a, b, c, d):
    config = f'a={a}, b={b}, c={c}, d={d}'
    if config not in history_list:
        history_list.append(config)
        history_listbox.insert(tk.END, config)
        saved_graphs.append((a, b, c, d))

def add_current_to_history():
    try:
        a = complex(entry_a.get())
        b = complex(entry_b.get())
        c = complex(entry_c.get())
        d = complex(entry_d.get())
        save_to_history(a, b, c, d)
    except ValueError:
        label_roots.config(text="Coeficienții trebuie să fie numere complexe valide.", style='Error.TLabel')
    except Exception as e:
        label_roots.config(text=f"Eroare: {str(e)}", style='Error.TLabel')

def load_from_history(event):
    selected_indices = history_listbox.curselection()
    selected_configs = [saved_graphs[i] for i in selected_indices]
    plot_function(selected_configs, ax)

def delete_selected_from_history():
    selected_indices = history_listbox.curselection()
    for i in reversed(selected_indices):
        history_listbox.delete(i)
        history_list.pop(i)
        saved_graphs.pop(i)
    refresh_plot()

def clear_history():
    history_listbox.delete(0, tk.END)
    history_list.clear()
    saved_graphs.clear()
    refresh_plot()

def refresh_plot():
    selected_indices = history_listbox.curselection()
    selected_configs = [saved_graphs[i] for i in selected_indices]
    plot_function(selected_configs, ax)

def zoom(event):
    base_scale = 1.1
    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()

    xdata = event.xdata
    ydata = event.ydata

    if event.button == 'up':
        scale_factor = 1 / base_scale
    elif event.button == 'down':
        scale_factor = base_scale
    else:
        return

    new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
    new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

    relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
    rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

    ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
    ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])

    ax.figure.canvas.draw_idle()

root = tk.Tk()
root.title("Rezolvare Ecuație De Gradul 3")
root.iconbitmap('.idea/Judge-Iphone-Graph.ico')

# Personalizarea culorilor
bg_color = '#f0f0f0'
fg_color = '#333'
entry_bg = '#fff'
entry_fg = '#000'
frame_bg = '#e0e0f0'
button_bg = '#007acc'
button_fg = '#000'

# Încărcare imagine de fundal
background_image_path = '.idea/pngtree-colorful-graphic-education-math-formula-background-on-blackboard-picture-image_1457817.jpg'
background_image = Image.open(background_image_path)
background_image = background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

# Creare label pentru fundal
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Frame pentru inputuri și istoric
frame = ttk.Frame(root, padding="10 10 10 10", style='Custom.TFrame')
frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.N, tk.S))

ttk.Label(frame, text="Coeficient a:", background=frame_bg, foreground=fg_color).grid(row=0, column=0, sticky=tk.W)
entry_a = ttk.Entry(frame)
entry_a.grid(row=0, column=1, sticky=(tk.W, tk.E))
entry_a.bind("<KeyRelease>", update_plot)

ttk.Label(frame, text="Coeficient b:", background=frame_bg, foreground=fg_color).grid(row=1, column=0, sticky=tk.W)
entry_b = ttk.Entry(frame)
entry_b.grid(row=1, column=1, sticky=(tk.W, tk.E))
entry_b.bind("<KeyRelease>", update_plot)

ttk.Label(frame, text="Coeficient c:", background=frame_bg, foreground=fg_color).grid(row=2, column=0, sticky=tk.W)
entry_c = ttk.Entry(frame)
entry_c.grid(row=2, column=1, sticky=(tk.W, tk.E))
entry_c.bind("<KeyRelease>", update_plot)

ttk.Label(frame, text="Coeficient d:", background=frame_bg, foreground=fg_color).grid(row=3, column=0, sticky=tk.W)
entry_d = ttk.Entry(frame)
entry_d.grid(row=3, column=1, sticky=(tk.W, tk.E))
entry_d.bind("<KeyRelease>", update_plot)

label_roots = ttk.Label(frame, text="", background=frame_bg, foreground=fg_color, style='Success.TLabel')
label_roots.grid(row=4, column=0, columnspan=2, pady=(10, 10))

# Frame pentru butoane
buttons_frame = ttk.Frame(frame, padding="5 5 5 5", style='Custom.TFrame')
buttons_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))

# Adaugare buton de salvare
save_button = ttk.Button(buttons_frame, text="Salvează", command=add_current_to_history, style='Save.TButton')
save_button.grid(row=0, column=0, padx=5, pady=(10, 10))

# Adaugare buton de ștergere din istoric
delete_from_history_button = ttk.Button(buttons_frame, text="Șterge", command=delete_selected_from_history,
                                        style='Delete.TButton')
delete_from_history_button.grid(row=0, column=1, padx=5, pady=(10, 10))

# Adaugare buton de curățare a istoricului
clear_history_button = ttk.Button(buttons_frame, text="Curăță", command=clear_history,
                                  style='Clear.TButton')
clear_history_button.grid(row=0, column=2, padx=5, pady=(10, 10))

# Frame pentru istoric în interiorul frame-ului principal
history_frame = ttk.Frame(frame, padding="10 10 10 10", style='Custom.TFrame')
history_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.S))

ttk.Label(history_frame, text="Grafice salvate:", background=frame_bg, foreground=fg_color).grid(row=0, column=0,
                                                                                                 sticky=tk.W)

# Listbox pentru istoric
history_listbox = tk.Listbox(history_frame, height=15, width=50, selectmode=tk.MULTIPLE)
history_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.S))
history_listbox.bind('<<ListboxSelect>>', load_from_history)

# Frame pentru grafic
plot_frame = ttk.Frame(root, padding="10 10 10 10", style='Custom.TFrame')
plot_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.N, tk.E, tk.S, tk.W))

# Creare figură și axă matplotlib
fig = Figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))

canvas.mpl_connect('scroll_event', zoom)

# Adaugare toolbar matplotlib
toolbar_frame = ttk.Frame(plot_frame, style='Custom.TFrame')
toolbar_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()

# Configurare greutăți grid pentru redimensionare
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

plot_frame.columnconfigure(0, weight=1)
plot_frame.rowconfigure(0, weight=1)
plot_frame.rowconfigure(1, weight=0)

# Aplicare stiluri
style = ttk.Style()
style.configure('Custom.TFrame', background=frame_bg)
style.configure('TLabel', background=frame_bg, foreground=fg_color)
style.configure('TEntry', fieldbackground=entry_bg, foreground=entry_fg)
style.configure('Save.TButton', background='green', foreground=button_fg, relief='flat', font=('Helvetica', 10, 'bold'))
style.configure('Delete.TButton', background='red', foreground=button_fg, relief='flat', font=('Helvetica', 10, 'bold'))
style.configure('Clear.TButton', background='blue', foreground=button_fg, relief='flat', font=('Helvetica', 10, 'bold'))
style.configure('Error.TLabel', foreground='red')
style.configure('Success.TLabel', foreground='green')

root.configure(background=bg_color)
frame.configure(style='Custom.TFrame')
plot_frame.configure(style='Custom.TFrame')
toolbar_frame.configure(style='Custom.TFrame')
history_frame.configure(style='Custom.TFrame')
buttons_frame.configure(style='Custom.TFrame')

history_list = []
saved_graphs = []

root.mainloop()
