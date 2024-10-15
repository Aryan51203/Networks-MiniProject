import socket
import time
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import matplotlib.pyplot as plt

ipv4_times = []
ipv6_times = []

def send_file(ip_version, server_address, port, file_paths, results_label):
    total_bytes_sent = 0
    total_time = 0
    try:
        family = socket.AF_INET if ip_version == 'IPv4' else socket.AF_INET6
        sock = socket.socket(family, socket.SOCK_STREAM)
        sock.connect((server_address, port))

        for file_path in file_paths:
            file_size = os.path.getsize(file_path)

            with open(file_path, 'rb') as file:
                start_time = time.time()
                bytes_sent = 0
                while True:
                    chunk = file.read(4096)
                    if not chunk:
                        break
                    sock.sendall(chunk)
                    bytes_sent += len(chunk)
                end_time = time.time()
            
            transfer_time = end_time - start_time
            total_bytes_sent += bytes_sent
            total_time += transfer_time

        throughput = total_bytes_sent / total_time

        results_label.config(text=f"Sent {total_bytes_sent} bytes in {total_time:.2f} seconds over {ip_version}.\n"
                                  f"Throughput: {throughput:.2f} bytes/second.")

        if ip_version == 'IPv4':
            ipv4_times.append(total_time)
        else:
            ipv6_times.append(total_time)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to send files: {str(e)}")
    finally:
        sock.close()

def browse_files(file_path_entry):
    file_paths = filedialog.askopenfilenames()
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, "; ".join(file_paths))

def run_client(ip_version, server_address, port, file_path_entry, results_label):
    file_paths = file_path_entry.get().split("; ")
    if not file_paths or not file_paths[0]:
        messagebox.showwarning("No files selected", "Please select files to send.")
        return

    send_file(ip_version, server_address, port, file_paths, results_label)

def plot_times():
    plt.figure(figsize=(10, 5))

    # Plot IPv4 vs IPv6 times
    if ipv4_times and ipv6_times:
        plt.plot(range(len(ipv4_times)), ipv4_times, label="IPv4", marker='o')
        plt.plot(range(len(ipv6_times)), ipv6_times, label="IPv6", marker='o')

        plt.xlabel("Test Number")
        plt.ylabel("Transfer Time (seconds)")
        plt.title("Comparison of Transfer Time: IPv4 vs IPv6")
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        messagebox.showinfo("No Data", "Please run both IPv4 and IPv6 transfers before plotting.")

def create_gui():
    root = tk.Tk()
    root.title("File Transfer System (Multi-File Support)")
    
    background_color = "#f0f4f7"
    button_color = "#5078f0"
    text_color = "#000000"
    root.configure(bg=background_color)

    default_font = ("Helvetica", 11)
    
    frame = tk.Frame(root, bg=background_color, padx=20, pady=20)
    frame.grid(row=0, column=0, padx=10, pady=10)

    title_label = tk.Label(frame, text="File Transfer System", font=("Helvetica", 16, "bold"), bg=background_color, fg=text_color)
    title_label.grid(row=0, column=0, columnspan=3, pady=10)

    tk.Label(frame, text="Files:", font=default_font, bg=background_color, fg=text_color).grid(row=1, column=0, padx=10, pady=10)
    file_path_entry = ttk.Entry(frame, width=40, font=default_font)
    file_path_entry.grid(row=1, column=1, padx=10, pady=10)
    browse_button = tk.Button(frame, text="Browse", command=lambda: browse_files(file_path_entry), bg=button_color, fg="white", font=default_font)
    browse_button.grid(row=1, column=2, padx=10, pady=10)

    tk.Label(frame, text="IP Version:", font=default_font, bg=background_color, fg=text_color).grid(row=2, column=0, padx=10, pady=10)
    ip_version_var = tk.StringVar(value="IPv4")
    ipv4_radio = tk.Radiobutton(frame, text="IPv4", variable=ip_version_var, value="IPv4", font=default_font, bg=background_color, fg=text_color, selectcolor=background_color)
    ipv4_radio.grid(row=2, column=1, padx=10, pady=10, sticky="w")
    ipv6_radio = tk.Radiobutton(frame, text="IPv6", variable=ip_version_var, value="IPv6", font=default_font, bg=background_color, fg=text_color, selectcolor=background_color)
    ipv6_radio.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    results_label = tk.Label(frame, text="", fg="green", justify="left", bg=background_color, font=default_font)
    results_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    send_button = tk.Button(frame, text="Send Files", command=lambda: run_client(ip_version_var.get(),
                                                                                 '127.0.0.1' if ip_version_var.get() == 'IPv4' else '::1',
                                                                                 12345, file_path_entry, results_label),
                            bg=button_color, fg="white", font=default_font)
    send_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    plot_button = tk.Button(frame, text="Plot Results", command=plot_times, bg=button_color, fg="white", font=default_font)
    plot_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    for widget in frame.winfo_children():
        widget.grid_configure(padx=5, pady=5)

    root.mainloop()

# Run the GUI
create_gui()
