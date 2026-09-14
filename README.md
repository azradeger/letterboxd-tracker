<div align="center">

# 🎬 Letterboxd Tracker
### A clean, modern desktop tool to find who isn't following you back on Letterboxd.

[![Release](https://img.shields.io/badge/Release-v1.1.0-00e054?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/azradeger/letterboxd-tracker/releases)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

<br />

Letterboxd does not provide a direct way to view mutual follows or see who doesn't follow back. **Letterboxd Tracker** is an intuitive, standalone desktop utility that analyzes your network and lists non-followers with zero hassle.

</div>

---

## ✨ Features

* **Zero Installation for Users:** Distributed as a standalone portable `.exe` — no Python setup needed.
* **Circular Avatars:** Displays profile pictures with clean circular cropping right next to usernames.
* **Modern Letterboxd UI:** Built with CustomTkinter following Letterboxd's signature dark theme palette.
* **Anti-Bot Protection Bypass:** Powered by browser-impersonating HTTP requests to handle Cloudflare checks seamlessly.
* **Direct Profile Navigation:** Open any detected profile directly in your default browser with one click.
* **Safe & Private:** Operates entirely locally. No credentials or passwords required.

---

## 🚀 Download & Run (For End Users)

You do not need to install Python or run any commands.

1. Go to the **[Releases](https://github.com/azradeger/letterboxd-tracker/releases/latest)** section.
2. Download the latest **`LetterboxdTracker.exe`**.
3. Double-click the file to open the app.
4. Enter your username and click **Analyze**.

---

## 🛠️ Build from Source (For Developers)

If you prefer to run or build the app from source code:

### 1. Clone the repository
```bash
git clone [https://github.com/azradeger/letterboxd-tracker.git](https://github.com/azradeger/letterboxd-tracker.git)
cd letterboxd-tracker
2. Set up virtual environment
PowerShell
python -m venv venv
.\venv\Scripts\activate
3. Install dependencies
Bash
pip install -r requirements.txt
4. Run the application
Bash
python app.py
5. Build standalone executable
PowerShell
pyinstaller --noconfirm --onefile --windowed --name "LetterboxdTracker" app.py
The compiled executable will be generated inside the dist/ folder.

🧰 Tech Stack
UI: CustomTkinter

Image Processing: Pillow (PIL)

Scraping: BeautifulSoup4

HTTP Engine: curl_cffi

Packaging: PyInstaller

🤖 Development Note (Vibecoding)
This project was built using a "vibecoding" approach. The core logic, UI generation, and Cloudflare bypass integrations were developed collaboratively with AI, allowing for rapid prototyping and deployment of a fully functional desktop application in a fraction of the usual time.

📝 Disclaimer
This tool is an unofficial community project and is not affiliated with, maintained, or endorsed by Letterboxd Limited.

📄 License
Distributed under the MIT License. See LICENSE for more details.
