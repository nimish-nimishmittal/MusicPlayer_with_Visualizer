import tkinter as tk
import fnmatch
import os
from pygame import mixer
from tkinter import Scale
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import librosa.display
#updated code...
fig = Figure(figsize=(4, 2), dpi=100)
ax = fig.add_subplot(111)
canvas = tk.Tk()
canvas.title("Music Player")
canvas.geometry("600x800")
canvas.config(bg='black')
#updated code...
canvas_visualizer = FigureCanvasTkAgg(fig, master=canvas)
canvas_visualizer.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
rootpath = "C:\\Users\\Nimesh\\Desktop\\miniplayer\\musics"
pattern = "*.mp3"
mixer.init()
prev_img = tk.PhotoImage(file = "C:\\Users\\Nimesh\\Desktop\\miniplayer\\musicplayer\\prev_img.png")
stop_img = tk.PhotoImage(file = "C:\\Users\\Nimesh\\Desktop\\miniplayer\\musicplayer\\stop_img.png")
power = tk.PhotoImage(file = "C:\\Users\\Nimesh\\Desktop\\miniplayer\\musicplayer\\power.png")
play_img = tk.PhotoImage(file = "C:\\Users\\Nimesh\\Desktop\\miniplayer\\musicplayer\\play_img.png")
pause_img = tk.PhotoImage(file = "C:\\Users\\Nimesh\\Desktop\\miniplayer\\musicplayer\\pause_img.png")
next_img = tk.PhotoImage(file = "C:\\Users\\Nimesh\\Desktop\\miniplayer\\musicplayer\\next_img.png")
def select():
    label.config(text = listBox.get("anchor"))
    mixer.music.load(rootpath + "\\" + listBox.get("anchor"))
    mixer.music.play()
def stop():
    mixer.music.stop()
    listBox.select_clear('active')
def play_next():
    next_song = listBox.curselection()
    next_song = next_song[0] + 1
    next_song_name = listBox.get(next_song)
    label.config(text = next_song_name)
    mixer.music.load(rootpath + "\\" + next_song_name)
    mixer.music.play()
    listBox.select_clear(0, 'end')
    listBox.activate(next_song)
    listBox.select_set(next_song)
def play_prev():
    next_song = listBox.curselection()
    next_song = next_song[0] - 1
    next_song_name = listBox.get(next_song)
    label.config(text = next_song_name)
    mixer.music.load(rootpath + "\\" + next_song_name)
    mixer.music.play()
    listBox.select_clear(0, 'end')
    listBox.activate(next_song)
    listBox.select_set(next_song)
def pause_song():
    mixer.music.pause()
def play_song():
    mixer.music.unpause()
def adjust_volume(volume):
    mixer.music.set_volume(float(volume))
def update_visualizer():
    try:
        if mixer.music.get_busy():
            # Get the current music position in seconds
            current_pos = mixer.music.get_pos() / 1000
            # Load the currently playing audio file
            audio_file = rootpath + "\\" + listBox.get("anchor")
            # Read the audio file and extract the waveform data
            y, sr = librosa.load(audio_file)
            duration = librosa.get_duration(y=y, sr=sr)
            # Calculate the desired plot length in seconds
            plot_length = 1.0  # Adjust this value as needed
            # Calculate the start and end time based on the current position and plot length
            start_time = max(0, current_pos - plot_length)
            end_time = current_pos
            # Convert the start and end time to sample indices
            start_index = int(start_time * sr)
            end_index = int(end_time * sr)
            # Slice the waveform data
            data = y[start_index:end_index]
            # Clear the axis and plot the waveform data
            ax.clear()
            ax.plot(data, color='red')
            # Adjust the width of the plot
            ax.set_xlim(0, len(data))
            ax.set_ylim(-1, 1)
            # Redraw the canvas
            canvas_visualizer.draw()
    except Exception as e:
        print(f"Error updating visualizer: {str(e)}")
    # Schedule the next update
    canvas.after(20, update_visualizer)
listBox = tk.Listbox(canvas, fg = "cyan", bg = "black", width = 100, font = ('ds-digital',14))
listBox.pack(padx = 15,pady = 15)
label = tk.Label(canvas, text = '', bg = 'black', fg = 'yellow', font = ('ds-digital',18))
label.pack(pady = 15)
top = tk.Frame(canvas, bg = 'black')
top.pack(padx = 10, pady = 5, anchor = 'center')
prevButton = tk.Button(canvas, text = "Prev", image = prev_img, bg = 'black', borderwidth = 0, command = play_prev)
prevButton.pack(pady = 15, in_ = top, side = 'left')
stopButton = tk.Button(canvas, text = "Stop", image = stop_img, bg = 'black', borderwidth = 0, command = stop)
stopButton.pack(pady = 15, in_ = top, side = 'left')
powerButton = tk.Button(canvas, text = "Prev", image = power, bg = 'black', borderwidth = 0, command = select)
powerButton.pack(pady = 15, in_ = top, side = 'left')
playButton = tk.Button(canvas, text = "Prev", image = play_img, bg = 'black', borderwidth = 0, command = play_song)
playButton.pack(pady = 15, in_ = top, side = 'left')
pauseButton = tk.Button(canvas, text = "Stop", image = pause_img, bg = 'black', borderwidth = 0, command = pause_song)
pauseButton.pack(pady = 15, in_ = top, side = 'left')
nextButton = tk.Button(canvas, text = "Stop", image = next_img, bg = 'black', borderwidth = 0, command = play_next)
nextButton.pack(pady = 15, in_ = top, side = 'left')
volumeScale = Scale(canvas, from_=0, to=1, resolution=0.1, orient="horizontal", length=200, bg="white", fg="black", troughcolor="gray", sliderrelief="flat", command=adjust_volume)
volumeScale.pack(pady=15, in_=top, side='left')
for root, dirs, files, in os.walk(rootpath):
    for filename in fnmatch.filter(files, pattern):
        listBox.insert('end',filename)

update_visualizer()
canvas.mainloop()
