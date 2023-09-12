import tkinter as tk
from tkinter import messagebox
import datetime, os, subprocess, sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

pcleavedetectors_folder = "pcleavedetectors"
def schedule(start_datetime, interval_seconds, text):
    newfile = pcleavedetectors_folder + "\\" + str(len(os.listdir(pcleavedetectors_folder))) + ".pyw"
    with open(newfile, "w") as f:
        f.write(open(pcleavedetectors_folder + "\\template.py", "r").read().replace("timenasd", str(interval_seconds)).replace("textenasd", str(text)))

    formatted_time = start_datetime.strftime('%H:%M')
    formatted_date = start_datetime.strftime('%d/%m/%Y')

    if start_datetime < datetime.datetime.now():
        subprocess.Popen(['python', newfile], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
        messagebox.showinfo("Success", "The python script is running.")
    else:
        code = os.system(fr'schtasks /create /tn "{"pcleavedetectorTask" + str(len(os.listdir(pcleavedetectors_folder)))}" /tr "{newfile}" /sc once /sd {formatted_date} /st {formatted_time}')

        if code != 0:
            messagebox.showinfo("Error", str(code))
        else:
            messagebox.showinfo("Scheduled", "The python script has been scheduled.")

def on_schedule_click():
    try:
        text = text_input.get("1.0", tk.END).strip()
        date_input_str = date_input.get().strip()
        start_time = start_time_input.get().strip()
        end_time = end_time_input.get().strip()

        if text == "":
            messagebox.showerror("Missing text", "Please provide text in the text input field")
            return

        if not start_time:
            messagebox.showerror("Error", "Please enter a valid start time.")
            return

        try:
            start_datetime = datetime.datetime.strptime(date_input_str + ' ' + start_time, '%Y-%m-%d %H:%M')
            if end_time:
                end_datetime = datetime.datetime.strptime(date_input_str + ' ' + end_time, '%Y-%m-%d %H:%M')
                interval_seconds = (end_datetime - start_datetime).seconds
            else:
                interval_seconds = 4 * 60 * 60
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Please use 'HH:MM' format.")
            return

        schedule(start_datetime, interval_seconds, text)
    except Exception as e:
        messagebox.showerror("Critical Error", str(e))
        return

root = tk.Tk()
root.title("PC leave detector scheduler")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

text_input = tk.Text(frame, wrap=tk.WORD, width=50, height=10)
text_input.pack()

date_input_label = tk.Label(frame, text="Date (YYYY-MM-DD):")
date_input_label.pack()
current_date = datetime.datetime.now().strftime('%Y-%m-%d')
date_input = tk.Entry(frame, width=20)
date_input.insert(0, current_date)
date_input.pack()

time_frame = tk.Frame(frame)
time_frame.pack(pady=10)

current_time = datetime.datetime.now().strftime('%H:%M')
start_time_input = tk.Entry(time_frame, width=10)
start_time_input.insert(0, current_time)
start_time_input.pack(side=tk.LEFT, padx=(0, 10))

end_time_input = tk.Entry(time_frame, width=10)
end_time_input.pack(side=tk.LEFT)

schedule_button = tk.Button(frame, text="Schedule", command=on_schedule_click)
schedule_button.pack()

root.mainloop()
