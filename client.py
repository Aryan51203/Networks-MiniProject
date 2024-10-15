import socket
import time
import os
import tkinter as tk
from tkinter import filedialog, messagebox


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
    root.title("File Transfer System")

    # Server address (localhost for simplicity)
    ipv4_server = "127.0.0.1"
    ipv6_server = "::1"
    port = 12345

    # File path input
    tk.Label(root, text="File Path:").grid(row=0, column=0, padx=10, pady=10)
    file_path_entry = tk.Entry(root, width=40)
    file_path_entry.grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=lambda: browse_file(file_path_entry)).grid(
        row=0, column=2, padx=10, pady=10
    )

    # IP version selection
    tk.Label(root, text="IP Version:").grid(row=1, column=0, padx=10, pady=10)
    ip_version_var = tk.StringVar(value="IPv4")
    tk.Radiobutton(root, text="IPv4", variable=ip_version_var, value="IPv4").grid(
        row=1, column=1, padx=10, pady=10, sticky="w"
    )
    tk.Radiobutton(root, text="IPv6", variable=ip_version_var, value="IPv6").grid(
        row=1, column=2, padx=10, pady=10, sticky="w"
    )

    # Results label
    results_label = tk.Label(root, text="", fg="green", justify="left")
    results_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    # Run test button
    tk.Button(
        root,
        text="Send File",
        command=lambda: run_client(
            ip_version_var.get(),
            ipv4_server if ip_version_var.get() == "IPv4" else ipv6_server,
            port,
            file_path_entry,
            results_label,
        ),
    ).grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    root.mainloop()


# Run the GUI
create_gui()
