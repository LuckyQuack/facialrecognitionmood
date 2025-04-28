import os
import sys
import shutil
import subprocess
import webbrowser
import tkinter as tk
from tkinter import messagebox

def check_python_installed():
    """Check if Python is installed"""
    try:
        # Check Python version
        subprocess.check_output(["python", "--version"])
        return True
    except:
        try:
            # Try python3 command as fallback
            subprocess.check_output(["python3", "--version"])
            return True
        except:
            return False

def install_dependencies():
    """Install required packages"""
    required_packages = [
        "numpy", "opencv-python", "tensorflow", "mediapipe", "PyQt6", "matplotlib"
    ]
    
    try:
        python_cmd = "python" if os.system("python --version") == 0 else "python3"
        for package in required_packages:
            messagebox.showinfo("Installing", f"Installing {package}... Please wait.")
            subprocess.check_call([python_cmd, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_camera():
    """Check if camera is available"""
    try:
        # Use subprocess to run a small Python script to check camera
        check_script = "import cv2; cap=cv2.VideoCapture(0); print(cap.isOpened()); cap.release()"
        python_cmd = "python" if os.system("python --version") == 0 else "python3"
        result = subprocess.check_output([python_cmd, "-c", check_script], universal_newlines=True)
        return "True" in result
    except:
        return False

def run_app():
    """Run the main application"""
    try:
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_script = os.path.join(script_dir, "main.py")
        
        # Run the main script
        python_cmd = shutil.which("python") or shutil.which("python3")
        subprocess.Popen([python_cmd, main_script])
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")
        return False

def main():
    # Create a simple GUI window
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Check if Python is installed
    if not check_python_installed():
        messagebox.showerror("Error", "Python is not installed. Please install Python 3.8 or newer.")
        webbrowser.open("start https://www.python.org/downloads/")
        return
    
    # Check for dependencies and install if needed
    messagebox.showinfo("Setup", "Checking required packages...")
    if not install_dependencies():
        messagebox.showerror("Error", "Failed to install required packages. Try running as administrator.")
        return
    
    # Check if camera is available
    if not check_camera():
        messagebox.showwarning("Warning", "No camera detected. Please connect a webcam before running the application.")
        return
    
    # Run the application
    messagebox.showinfo("Ready", "Starting Emotion Detection Application...")
    run_app()

if __name__ == "__main__":
    main()