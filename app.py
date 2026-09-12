import threading
import webbrowser
from bs4 import BeautifulSoup
import customtkinter as ctk
from curl_cffi import requests as cffi_requests

# Letterboxd Color Palette
COLOR_BG = "#14181c"
COLOR_CARD = "#1f252b"
COLOR_GREEN = "#00e054"
COLOR_HOVER = "#00b044"
COLOR_TEXT = "#9ab"
COLOR_WHITE = "#ffffff"
COLOR_BORDER = "#2c3440"
COLOR_ORANGE = "#ff8000"

class LetterboxdTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Letterboxd Non-Followers Tracker")
        self.geometry("780x680")
        self.minsize(650, 550)
        self.configure(fg_color=COLOR_BG)
        ctk.set_appearance_mode("dark")

        self._build_ui()

    def _build_ui(self):
        # Header Section
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(pady=(25, 15), padx=20, fill="x")

        title = ctk.CTkLabel(
            header,
            text="● Letterboxd Tracker",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLOR_GREEN
        )
        title.pack()

        subtitle = ctk.CTkLabel(
            header,
            text="Discover who isn't following you back on Letterboxd",
            font=ctk.CTkFont(size=13),
            text_color=COLOR_TEXT
        )
        subtitle.pack(pady=(2, 0))

        # Input Card
        input_card = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        input_card.pack(padx=30, pady=10, fill="x")

        self.entry_username = ctk.CTkEntry(
            input_card,
            placeholder_text="Enter Letterboxd username...",
            height=42,
            fg_color=COLOR_BG,
            border_color=COLOR_BORDER,
            text_color=COLOR_WHITE,
            font=ctk.CTkFont(size=14)
        )
        self.entry_username.pack(side="left", padx=(15, 10), pady=12, fill="x", expand=True)
        self.entry_username.bind("<Return>", lambda e: self.start_analysis())

        self.btn_search = ctk.CTkButton(
            input_card,
            text="Analyze",
            height=42,
            fg_color=COLOR_GREEN,
            hover_color=COLOR_HOVER,
            text_color="#000000",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.start_analysis
        )
        self.btn_search.pack(side="right", padx=(0, 15), pady=12)

        # Stat Cards
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(padx=30, pady=5, fill="x")

        self.card_following = self._create_stat_card(self.stats_frame, "Following", "-", COLOR_WHITE)
        self.card_followers = self._create_stat_card(self.stats_frame, "Followers", "-", COLOR_WHITE)
        self.card_not_following = self._create_stat_card(self.stats_frame, "Not Following Back", "-", COLOR_ORANGE)

        # Status Label
        self.lbl_status = ctk.CTkLabel(
            self,
            text="Enter a username and click 'Analyze' to begin.",
            font=ctk.CTkFont(size=12),
            text_color=COLOR_TEXT
        )
        self.lbl_status.pack(pady=(8, 4))

        # Scrollable Result List
        self.scroll_list = ctk.CTkScrollableFrame(
            self,
            fg_color=COLOR_CARD,
            corner_radius=10,
            border_width=1,
            border_color=COLOR_BORDER
        )
        self.scroll_list.pack(padx=30, pady=(5, 20), fill="both", expand=True)

    def _create_stat_card(self, parent, title, initial_val, value_color):
        card = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        card.pack(side="left", fill="x", expand=True, padx=4)

        lbl_t = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=11), text_color=COLOR_TEXT)
        lbl_t.pack(pady=(8, 0))

        lbl_v = ctk.CTkLabel(card, text=initial_val, font=ctk.CTkFont(size=18, weight="bold"), text_color=value_color)
        lbl_v.pack(pady=(0, 8))
        return lbl_v

    def start_analysis(self):
        username = self.entry_username.get().strip()
        if not username:
            self.lbl_status.configure(text="Please enter a valid username!", text_color=COLOR_ORANGE)
            return

        self.btn_search.configure(state="disabled")
        self.lbl_status.configure(text=f"Scanning @{username}'s network... Please wait.", text_color=COLOR_WHITE)

        threading.Thread(target=self._run_scrape, args=(username,), daemon=True).start()

    def _fetch_users(self, session, username, endpoint):
        users = {}
        page = 1
        ignore_slugs = {
            "following", "followers", "members", "films", "reviews", "lists", 
            "likes", "watchlist", "activity", "tags", "stats", "rss", "search"
        }

        while True:
            url = f"https://letterboxd.com/{username}/{endpoint}/page/{page}/"
            try:
                res = session.get(url)
                if res.status_code != 200:
                    break
                
                soup = BeautifulSoup(res.content, "html.parser")
                
                person_elements = soup.select("td.table-person, tr.person-summary, div.person-summary, table.person-table tr")
                if not person_elements:
                    person_elements = soup.select("a.avatar, a.name, h3.title-3 a")

                if not person_elements:
                    break

                found_in_page = False
                for el in person_elements:
                    links = [el] if el.name == "a" else el.find_all("a")
                    for a in links:
                        href = a.get("href", "").strip("/")
                        if not href:
                            continue
                        
                        parts = href.split("/")
                        if len(parts) == 1:
                            handle = parts[0].lower()
                            if handle not in ignore_slugs and handle != username.lower():
                                display = a.get_text(strip=True) or handle
                                if handle not in users or users[handle] == handle:
                                    users[handle] = display
                                found_in_page = True

                if not found_in_page:
                    break

                if not soup.select_one("a.next, a.paginate-next"):
                    break

                page += 1
            except Exception:
                break

        return users

    def _run_scrape(self, username):
        session = cffi_requests.Session(impersonate="chrome")
        
        following = self._fetch_users(session, username, "following")
        followers = self._fetch_users(session, username, "followers")

        not_following_handles = set(following.keys()) - set(followers.keys())
        not_following_list = [(h, following[h]) for h in not_following_handles]
        not_following_list.sort(key=lambda x: x[1].lower())

        self.after(0, lambda: self._update_ui_results(following, followers, not_following_list))

    def _update_ui_results(self, following, followers, not_following_list):
        self.btn_search.configure(state="normal")
        
        self.card_following.configure(text=str(len(following)))
        self.card_followers.configure(text=str(len(followers)))
        self.card_not_following.configure(text=str(len(not_following_list)))

        for child in self.scroll_list.winfo_children():
            child.destroy()

        if len(following) == 0 and len(followers) == 0:
            self.lbl_status.configure(text="User not found or profile is private!", text_color=COLOR_ORANGE)
            return

        self.lbl_status.configure(text="Analysis completed successfully.", text_color=COLOR_GREEN)

        if not not_following_list:
            lbl_empty = ctk.CTkLabel(
                self.scroll_list,
                text="Awesome! Everyone you follow is following you back.",
                font=ctk.CTkFont(size=13),
                text_color=COLOR_TEXT
            )
            lbl_empty.pack(pady=30)
            return

        for handle, display_name in not_following_list:
            row = ctk.CTkFrame(self.scroll_list, fg_color=COLOR_BG, corner_radius=6, border_width=1, border_color=COLOR_BORDER)
            row.pack(fill="x", padx=5, pady=4)

            name_box = ctk.CTkFrame(row, fg_color="transparent")
            name_box.pack(side="left", padx=12, pady=8)

            lbl_name = ctk.CTkLabel(
                name_box,
                text=display_name,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=COLOR_WHITE,
                anchor="w"
            )
            lbl_name.pack(anchor="w")

            lbl_handle = ctk.CTkLabel(
                name_box,
                text=f"@{handle}",
                font=ctk.CTkFont(size=11),
                text_color=COLOR_TEXT,
                anchor="w"
            )
            lbl_handle.pack(anchor="w")

            btn_link = ctk.CTkButton(
                row,
                text="View Profile ↗",
                width=90,
                height=28,
                fg_color=COLOR_CARD,
                hover_color=COLOR_BORDER,
                text_color=COLOR_WHITE,
                font=ctk.CTkFont(size=11),
                command=lambda h=handle: webbrowser.open(f"https://letterboxd.com/{h}/")
            )
            btn_link.pack(side="right", padx=12, pady=8)

if __name__ == "__main__":
    app = LetterboxdTrackerApp()
    app.mainloop()