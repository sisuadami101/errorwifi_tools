import os
import subprocess
import json
import qrcode
from cryptography.fernet import Fernet
from speedtest import Speedtest
import tkinter as tk
import speech_recognition as sr

# ========== ফাংশনসমূহ ========== #

def fetch_wifi_info():
    """WiFi তথ্য সংগ্রহ"""
    try:
        result = subprocess.check_output(['termux-wifi-connectioninfo']).decode('utf-8')
        with open("wifi_info.txt", "w") as file:
            file.write(result)
        print("WiFi তথ্য সংরক্ষণ করা হয়েছে।")
    except Exception as e:
        print(f"WiFi তথ্য সংগ্রহে সমস্যা: {e}")

def monitor_signal():
    """লাইভ সিগনাল মনিটর"""
    try:
        while True:
            result = subprocess.check_output(['termux-wifi-connectioninfo']).decode('utf-8')
            signal_strength = json.loads(result).get('rssi', 'N/A')
            print(f"সিগনাল শক্তি: {signal_strength} dBm")
    except KeyboardInterrupt:
        print("মনিটর বন্ধ করা হয়েছে।")

def check_connected_devices():
    """সংযুক্ত ডিভাইস চেকার"""
    try:
        result = subprocess.check_output(['nmap', '-sn', '192.168.1.0/24']).decode('utf-8')
        with open("connected_devices.txt", "w") as file:
            file.write(result)
        print("সংযুক্ত ডিভাইসের তালিকা তৈরি হয়েছে।")
    except Exception as e:
        print(f"সংযুক্ত ডিভাইস চেক করতে সমস্যা: {e}")

def create_hotspot():
    """WiFi হটস্পট তৈরি"""
    try:
        ssid = input("হটস্পটের নাম দিন: ")
        password = input("পাসওয়ার্ড দিন: ")
        os.system(f"termux-wifi-enable true; termux-wifi-setconfig {ssid} {password}")
        print("হটস্পট সফলভাবে তৈরি হয়েছে।")
    except Exception as e:
        print(f"হটস্পট তৈরি করতে সমস্যা: {e}")

def speed_test():
    """স্পিড টেস্ট"""
    try:
        st = Speedtest()
        download_speed = st.download() / 1_000_000
        upload_speed = st.upload() / 1_000_000
        print(f"ডাউনলোড স্পিড: {download_speed:.2f} Mbps")
        print(f"আপলোড স্পিড: {upload_speed:.2f} Mbps")
    except Exception as e:
        print(f"স্পিড টেস্টে সমস্যা: {e}")

def voice_command():
    """ভয়েস কন্ট্রোল"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("আপনার কমান্ড বলুন...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio, language="bn-BD")
            print(f"আপনার কমান্ড: {command}")
            return command
        except Exception as e:
            print(f"ভয়েস কমান্ড নিতে সমস্যা: {e}")

def firewall_block(mac_address):
    """ফায়ারওয়াল ব্লক"""
    try:
        os.system(f"iptables -A INPUT -m mac --mac-source {mac_address} -j DROP")
        print(f"{mac_address} ব্লক করা হয়েছে।")
    except Exception as e:
        print(f"ব্লক করতে সমস্যা: {e}")

def graphical_interface():
    """GUI চালু করুন"""
    root = tk.Tk()
    root.title("WiFi টুল")
    tk.Label(root, text="WiFi টুল").pack()
    tk.Button(root, text="WiFi তথ্য সংগ্রহ", command=fetch_wifi_info).pack()
    tk.Button(root, text="প্রস্থান", command=root.quit).pack()
    root.mainloop()

def jam_wifi():
    """WiFi জ্যামিং (শিক্ষার উদ্দেশ্যে)"""
    try:
        target = input("টার্গেট SSID দিন: ")
        os.system(f"mdk4 wlan0 d -t {target}")
        print("WiFi জ্যামিং শুরু হয়েছে।")
    except Exception as e:
        print(f"WiFi জ্যামিং করতে সমস্যা: {e}")

def custom_script():
    """কাস্টম স্ক্রিপ্ট রান"""
    try:
        command = input("কমান্ড লিখুন: ")
        os.system(command)
    except Exception as e:
        print(f"কাস্টম স্ক্রিপ্টে সমস্যা: {e}")

# ========== মেনু ========== #
def main_menu():
    while True:
        print("\nওয়াইফাই টুল মেনু")
        print("১। WiFi তথ্য সংগ্রহ")
        print("২। লাইভ সিগনাল মনিটর")
        print("৩। সংযুক্ত ডিভাইস চেকার")
        print("৪। হটস্পট তৈরি")
        print("৫। স্পিড টেস্ট")
        print("৬। GUI চালু")
        print("৭। ভয়েস কন্ট্রোল")
        print("৮। ফায়ারওয়াল ব্লক")
        print("৯। WiFi জ্যামিং")
        print("১০। কাস্টম স্ক্রিপ্ট")
        print("১১। প্রস্থান")
        
        choice = input("আপনার পছন্দ দিন: ")
        
        if choice == "১":
            fetch_wifi_info()
        elif choice == "২":
            monitor_signal()
        elif choice == "৩":
            check_connected_devices()
        elif choice == "৪":
            create_hotspot()
        elif choice == "৫":
            speed_test()
        elif choice == "৬":
            graphical_interface()
        elif choice == "৭":
            voice_command()
        elif choice == "৮":
            mac_address = input("MAC অ্যাড্রেস দিন: ")
            firewall_block(mac_address)
        elif choice == "৯":
            jam_wifi()
        elif choice == "১০":
            custom_script()
        elif choice == "১১":
            print("ধন্যবাদ! প্রস্থান করা হচ্ছে...")
            break
        else:
            print("সঠিক অপশন নির্বাচন করুন।")

# ========== প্রোগ্রাম শুরু ========== #
if __name__ == "__main__":
    main_menu()
