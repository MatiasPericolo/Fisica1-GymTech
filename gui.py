import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import prueba

class VideoPlayerApp:

    frameNumber = 0
    frames = 0

    def __init__(self, master):
        self.master = master
        self.master.title("Reproductor de Video")
        
        self.video_path = None
        self.video_cap = None
        self.is_playing = False
        
        self.create_widgets()

    def create_widgets(self):
        # Frame principal para el reproductor de video
        self.video_frame = tk.Frame(self.master)
        self.video_frame.pack(padx=10, pady=10)

        self.btn_open = tk.Button(self.video_frame, text="Seleccionar Video", command=self.open_video)
        self.btn_open.grid(column=0,row=0)

        self.btn_play = tk.Button(self.video_frame, text="\u23F5", command=self.play_video, state=tk.DISABLED)
        self.btn_play.grid(column=1,row=0)

        self.btn_stop = tk.Button(self.video_frame, text="\u23F8", command=self.stop_video, state=tk.DISABLED)
        self.btn_stop.grid(column=2,row=0)

        self.video_label = tk.Label(self.video_frame)
        self.video_label.grid(column=1,row=1)

        # Frame para la imagen adicional a la derecha
        self.image_frame = tk.Frame(self.master)
        self.image_frame.pack(padx=10, pady=10)

        # Crear un label para la imagen
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        # Cargar y mostrar la imagen en el frame
        self.load_image()
        self.show_image()

        

    def update_slider_position(self,val):
        # Actualizar la posición del slider
        self.slider.set(val)

    def open_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Archivos de Video", "*.mp4;*.avi;*.mkv")])
        if self.video_path:
            
            # Llama a la funcion track_pose de prueba.py
            prueba.video_ready_callback = self.video_ready_callback
            prueba.track_pose(self.video_path)

            # Abre el video generado
            self.video_cap = cv2.VideoCapture('resultados\\video\\tracked_video.mp4')

            # Consigue los frames totales para generar el slider con ese numero maximo
            self.frames = int(self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.slider = tk.Scale(from_=0, to=self.frames, orient=tk.HORIZONTAL, command=self.on_slider_changed)
            self.slider.pack(fill=tk.X)

            self.btn_play.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.NORMAL)

    # Actualizar el fotograma actual del video según el valor del slider SOLO si el video esta pausado
    def on_slider_changed(self, val):
        if not self.is_playing:
            self.frameNumber = int(val)
            self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, self.frameNumber)
            self.show_frame()

    # Funcion auxiliar para que compruebe que se genero el video 
    def video_ready_callback(self):
        self.btn_play.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.NORMAL)

    def play_video(self):
        if self.video_cap:
            self.is_playing = True
            self.btn_play.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            self.show_frame()

    def stop_video(self):
        if self.video_cap:
            self.is_playing = False
            self.btn_play.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)

    def show_frame(self):
        ret, frame = self.video_cap.read()
        if ret:
            # Redimensionar el fotograma
            frame_resized = cv2.resize(frame, (600, 450))
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)
            self.video_label.img_tk = img_tk
            self.video_label.config(image=img_tk)
            if self.is_playing:
                self.video_label.after(30, self.show_frame)
            self.update_slider_position(self.frameNumber)
            self.frameNumber += 1
        else:
            self.stop_video()        

    def load_image(self):
        # Cargar una imagen desde el archivo
        self.image_path = "plot.png"  # aca va la ruta de los graficos
        self.image = Image.open(self.image_path)

    def show_image(self):
        # Mostrar la imagen en el frame
        image_width, image_height = self.image.size
        resized_image = self.image.resize((int(image_width / 2), int(image_height / 2)))  # Ajustar el tamaño de la imagen
        self.img_tk = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=self.img_tk)
        self.image_label.image = self.img_tk

def main():
    root = tk.Tk()
    app = VideoPlayerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
