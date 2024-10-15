import socket
import time
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


def send_file(ip_version, server_address, port, file_path, results_label):
    try:
        # Determine IP version
        family = socket.AF_INET if ip_version == "IPv4" else socket.AF_INET6
        sock = socket.socket(family, socket.SOCK_STREAM)
        sock.connect((server_address, port))

        # Get file size
        file_size = os.path.getsize(file_path)

        # Start the transfer
        with open(file_path, "rb") as file:
            start_time = time.time()
            bytes_sent = 0
            while True:
                chunk = file.read(4096)
                if not chunk:
                    break
                sock.sendall(chunk)
                bytes_sent += len(chunk)
            end_time = time.time()

        # Calculate time and throughput
        transfer_time = end_time - start_time
        throughput = bytes_sent / transfer_time

        # Update GUI with results
        results_label.config(
            text=f"Sent {bytes_sent} bytes in {transfer_time:.2f} seconds over {ip_version}.\n"
            f"Throughput: {throughput:.2f} bytes/second."
        )

    except Exception as e:
        messagebox.showerror("Error", f"Failed to send file: {str(e)}")
    finally:
        sock.close()


def browse_file(file_path_entry):
    file_path = filedialog.askopenfilename()
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)


def run_client(ip_version, server_address, port, file_path_entry, results_label):
    file_path = file_path_entry.get()
    if not file_path:
        messagebox.showwarning("No file selected", "Please select a file to send.")
        return

    # Run the file transfer
    send_file(ip_version, server_address, port, file_path, results_label)


def create_gui():
    root = tk.Tk()
    root.title("Dual Stack File Transfer System")

    # Set a consistent color scheme
    background_color = "#f0f4f7"  # Light blue-gray
    button_color = "#5078f0"  # Nice blue for buttons
    text_color = "#000000"  # Black for text
    root.configure(bg=background_color)

    # Set default font style
    default_font = ("Helvetica", 11)

    # Frame to hold everything
    frame = tk.Frame(root, bg=background_color, padx=20, pady=20)
    frame.grid(row=0, column=0, padx=10, pady=10)

    # Title label
    title_label = tk.Label(
        frame,
        text="Dual Stack File Transfer System",
        font=("Helvetica", 16, "bold"),
        bg=background_color,
        fg=text_color,
    )
    title_label.grid(row=0, column=0, columnspan=3, pady=10)

    # File path input
    tk.Label(
        frame, text="File Path:", font=default_font, bg=background_color, fg=text_color
    ).grid(row=1, column=0, padx=10, pady=10)
    file_path_entry = ttk.Entry(frame, width=40, font=default_font)
    file_path_entry.grid(row=1, column=1, padx=10, pady=10)
    browse_button = tk.Button(
        frame,
        text="Browse",
        command=lambda: browse_file(file_path_entry),
        bg=button_color,
        fg="white",
        font=default_font,
    )
    browse_button.grid(row=1, column=2, padx=10, pady=10)

    # IP version selection
    tk.Label(
        frame, text="IP Version:", font=default_font, bg=background_color, fg=text_color
    ).grid(row=2, column=0, padx=10, pady=10)
    ip_version_var = tk.StringVar(value="IPv4")
    ipv4_radio = tk.Radiobutton(
        frame,
        text="IPv4",
        variable=ip_version_var,
        value="IPv4",
        font=default_font,
        bg=background_color,
        fg=text_color,
        selectcolor=background_color,
    )
    ipv4_radio.grid(row=2, column=1, padx=10, pady=10, sticky="w")
    ipv6_radio = tk.Radiobutton(
        frame,
        text="IPv6",
        variable=ip_version_var,
        value="IPv6",
        font=default_font,
        bg=background_color,
        fg=text_color,
        selectcolor=background_color,
    )
    ipv6_radio.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    # Results label
    results_label = tk.Label(
        frame,
        text="",
        fg="green",
        justify="left",
        bg=background_color,
        font=default_font,
    )
    results_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    # Run test button
    send_button = tk.Button(
        frame,
        text="Send File",
        command=lambda: run_client(
            ip_version_var.get(),
            "127.0.0.1" if ip_version_var.get() == "IPv4" else "::1",
            12345,
            file_path_entry,
            results_label,
        ),
        bg=button_color,
        fg="white",
        font=default_font,
    )
    send_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    # Adding padding around all widgets
    for widget in frame.winfo_children():
        widget.grid_configure(padx=5, pady=5)

    # Start the GUI
    root.mainloop()


# Run the GUI
create_gui()
