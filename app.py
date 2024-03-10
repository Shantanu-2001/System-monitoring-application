import psutil
from flask import Flask, render_template

app = Flask(__name__)

def get_processes_info():
    # List to hold information about all processes
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent'])
            # Append dict to list
            processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # Sort processes by CPU usage
    processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)
    return processes

@app.route("/")
def index():
    cpu_metric = psutil.cpu_percent()
    mem_metric = psutil.virtual_memory().percent
    disk_metric = psutil.disk_usage('/').percent
    battery = psutil.sensors_battery()
    battery_metric = battery.percent if battery is not None else None
    processes_info = get_processes_info()  # Get list of processes

    Message = None
    if cpu_metric > 80 or mem_metric > 80 or disk_metric > 80:
        Message = "High CPU, Memory, or Disk Usage Detected, scale up!!!"
    
    return render_template("index.html", cpu_metric=cpu_metric, mem_metric=mem_metric, disk_metric=disk_metric, battery_metric=battery_metric, processes_info=processes_info, message=Message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

