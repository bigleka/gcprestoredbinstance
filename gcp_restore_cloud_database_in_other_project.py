import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# instalar dependencias pelo pip
# pip install google-auth google-auth-oauthlib
# pip install --upgrade google-api-python-client

# Variável global para armazenar as credenciais
# Para gerar as credencias executar o comando
# gcloud auth application-default login
# executar a autenticação do browser e voltar ao prompt
# copiar o arquivo ou o caminho do arquivo que será criado em
# C:\Users\????\AppData\Roaming\gcloud\application_default_credentials.json
# Onde ???? é o seu usuário



# Autenticação e obtenção dos dados do GCP
creds = None

def authenticate_with_gcp(cred_file):
    creds = Credentials.from_authorized_user_file(cred_file)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
    return creds

def get_projects():
    headers = {"Authorization": f"Bearer {creds.token}"}
    url = "https://cloudresourcemanager.googleapis.com/v1/projects"
    response = requests.get(url, headers=headers)
    return [project['projectId'] for project in response.json().get('projects', [])]

def get_instances(project_id):
    headers = {"Authorization": f"Bearer {creds.token}"}
    url = f"https://sqladmin.googleapis.com/v1/projects/{project_id}/instances"
    response = requests.get(url, headers=headers)
    return [instance['name'] for instance in response.json().get('items', [])]

def load_credentials():
    global creds
    filepath = filedialog.askopenfilename()
    if filepath:
        creds = authenticate_with_gcp(filepath)
        projects = get_projects()
        left_project_dropdown['values'] = projects
        left_project_dropdown['state'] = 'readonly'
        right_project_dropdown['values'] = projects
        right_project_dropdown['state'] = 'readonly'

def update_left_instances_dropdown(event):
    instances = get_instances(left_project_dropdown.get())
    left_instance_dropdown['values'] = instances
    left_instance_dropdown['state'] = 'readonly'

def update_right_instances_dropdown(event):
    instances = get_instances(right_project_dropdown.get())
    right_instance_dropdown['values'] = instances
    right_instance_dropdown['state'] = 'readonly'

def load_backups():
    backup_listbox.delete(0, tk.END)
    project_id = left_project_dropdown.get()
    instance_id = left_instance_dropdown.get()
    headers = {"Authorization": f"Bearer {creds.token}"}
    url = f"https://sqladmin.googleapis.com/v1/projects/{project_id}/instances/{instance_id}/backupRuns"
    response = requests.get(url, headers=headers)
    for backup in response.json().get('items', []):
        backup_listbox.insert(tk.END, f"ID: {backup['id']} | StartTime: {backup['startTime']}")

def restore_backup():
    if not backup_listbox.curselection():
        messagebox.showwarning("Selection Required", "Please select at least one backup item from the list.")
        return
    
    confirm = messagebox.askyesno("Confirmation", "Do you really want to proceed? This will overwrite the target instance.")
    if not confirm:
        return
    
    selected_backup = backup_listbox.get(backup_listbox.curselection())
    backup_id = selected_backup.split("|")[0].split(":")[1].strip()
    source_project = left_project_dropdown.get()
    source_instance = left_instance_dropdown.get()
    target_project = right_project_dropdown.get()
    target_instance = right_instance_dropdown.get()

    data = {
        "restoreBackupContext": {
            "backupRunId": backup_id,
            "project": source_project,
            "instanceId": source_instance
        }
    }

    headers = {"Authorization": f"Bearer {creds.token}", "Content-Type": "application/json"}
    url = f"https://sqladmin.googleapis.com/v1/projects/{target_project}/instances/{target_instance}/restoreBackup"
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        messagebox.showinfo("Success", "Restore request submitted successfully!")
    else:
        messagebox.showerror("Error", f"Error submitting restore request: {response.json()}")


# GUI
app = tk.Tk()
app.title("GCP Backup Restore Utility")

frame = ttk.Frame(app, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Carregar credenciais
credential_button = ttk.Button(frame, text="Load GCP Credentials", command=load_credentials)
credential_button.grid(row=0, column=0, sticky=tk.W, pady=(0, 20), columnspan=2)

# Drop-downs da esquerda
left_project_dropdown = ttk.Combobox(frame, state='disabled')
left_project_dropdown.grid(row=1, column=0, sticky=tk.W, pady=5)
left_project_dropdown.bind("<<ComboboxSelected>>", update_left_instances_dropdown)

left_instance_dropdown = ttk.Combobox(frame, state='disabled')
left_instance_dropdown.grid(row=2, column=0, sticky=tk.W, pady=5)

load_backups_button = ttk.Button(frame, text="Load Backups", command=load_backups)
load_backups_button.grid(row=3, column=0, sticky=tk.W, pady=10)

# Drop-downs da direita
right_project_dropdown = ttk.Combobox(frame, state='disabled')
right_project_dropdown.grid(row=1, column=1, sticky=tk.W, pady=5)
right_project_dropdown.bind("<<ComboboxSelected>>", update_right_instances_dropdown)

right_instance_dropdown = ttk.Combobox(frame, state='disabled')
right_instance_dropdown.grid(row=2, column=1, sticky=tk.W, pady=5)

restore_button = ttk.Button(frame, text="Restore", command=restore_backup)
restore_button.grid(row=3, column=1, sticky=tk.W, pady=10)

# Listbox para backups
backup_listbox = tk.Listbox(frame, width=60)
backup_listbox.grid(row=4, column=0, columnspan=2, pady=10)


app.mainloop()
