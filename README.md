# AutoPick 🎯  

**AutoPick** is an automated pickpocketing script for **Schedule I**, utilizing **image recognition** and **keypress automation** to efficiently loot NPCs. It detects visual cues in the game and presses `SPACE` at the right moment to ensure optimal pickpocketing.  

## ✨ Features  
- 🎯 **Smart visual detection** – Uses OpenCV to identify the green bar and arrow alignment.  
- ⌨️ **Automated keypress** – Presses `SPACE` when conditions are met.  
- 🖥️ **Game window focusing** – Ensures **Schedule I** is the active window.  
- ⚡ **Real-time toggle** – Press `CTRL + ALT` to enable/disable AutoPick.  
- 🖼️ **Debug mode** – View detection in real time.  

## 🛠️ Requirements  
Ensure you have the necessary dependencies installed before running the script:  

```bash
pip install pydirectinput opencv-python numpy keyboard mss pywin32
```

## 🚀 Usage  

1. **Run the script**  
   ```bash
   python autopick.py
   ```  
2. **Ensure the game window is active** (AutoPick will attempt to focus **Schedule I** automatically).  
3. **Press `CTRL + ALT`** to toggle AutoPick on/off.  
4. If debug mode is enabled, a window will show detected regions.  
5. **Press `Q`** in the debug window to exit visual debugging.  

## 🔧 Configuration  
Modify the following settings in the script if needed:  

- **Game window title** (default: `"Schedule I"`)  
- **Region for detection** (`BAR_REGION`)  
- **HSV color ranges** for detecting green and white bars  
- **Toggle debug mode** (`debug_enabled = True/False`)  

## ⚠️ Disclaimer  
This script is for educational purposes only. **Use responsibly** and ensure compliance with **Schedule I**'s terms of service.  
