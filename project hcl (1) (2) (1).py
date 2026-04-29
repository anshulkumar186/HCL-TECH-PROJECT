# ============================================================
#  Club & Event Discovery Platform  ★  Version 2.0
#  Group 12 | B.Tech 2nd Semester | Design Thinking & Algorithms
#  Members: Saket Narayanan, Sakshi Kumari, Dipanshu Kumar Singh,
#            Anshul, Manthan Rohilla
# ============================================================

import os
import time
import json
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)

# ── COLOUR SHORTCUTS ────────────────────────────────────────
def bold(t):    return Style.BRIGHT + t + Style.RESET_ALL
def blue(t):    return Fore.CYAN + t + Style.RESET_ALL
def green(t):   return Fore.GREEN + t + Style.RESET_ALL
def yellow(t):  return Fore.YELLOW + t + Style.RESET_ALL
def red(t):     return Fore.RED + t + Style.RESET_ALL
def magenta(t): return Fore.MAGENTA + t + Style.RESET_ALL
def white(t):   return Fore.WHITE + Style.BRIGHT + t + Style.RESET_ALL
def gray(t):    return Fore.WHITE + t + Style.RESET_ALL
def header_bg(t): return Back.BLUE + Fore.WHITE + Style.BRIGHT + t + Style.RESET_ALL
def success_bg(t): return Back.GREEN + Fore.WHITE + Style.BRIGHT + t + Style.RESET_ALL
def warn_bg(t):    return Back.YELLOW + Fore.BLACK + Style.BRIGHT + t + Style.RESET_ALL
def err_bg(t):     return Back.RED + Fore.WHITE + Style.BRIGHT + t + Style.RESET_ALL

# ── CATEGORY ICONS & COLOURS ────────────────────────────────
CAT_STYLE = {
    "technology": (Fore.CYAN,    "💻"),
    "arts":       (Fore.MAGENTA, "🎨"),
    "sports":     (Fore.GREEN,   "⚽"),
    "creative":   (Fore.YELLOW,  "📸"),
    "business":   (Fore.BLUE,    "💼"),
    "academic":   (Fore.WHITE,   "📚"),
    "social":     (Fore.GREEN,   "🌱"),
}

def cat_label(cat):
    color, icon = CAT_STYLE.get(cat, (Fore.WHITE, "•"))
    return color + Style.BRIGHT + f"{icon} {cat.upper()}" + Style.RESET_ALL

# ── DATABASE ────────────────────────────────────────────────
CLUBS = [
    {"id": 1,  "name": "Coding Club",          "category": "technology", "rating": 4.8, "members": 120,
     "description": "Competitive programming, hackathons, and DSA practice.",
     "contact": "coding@college.edu",  "meet": "Every Saturday 10 AM",  "room": "Lab 3B"},
    {"id": 2,  "name": "Robotics Club",         "category": "technology", "rating": 4.5, "members": 85,
     "description": "Build and program robots; IoT and embedded systems.",
     "contact": "robotics@college.edu", "meet": "Every Sunday 11 AM",   "room": "Lab 2A"},
    {"id": 3,  "name": "Music Club",            "category": "arts",       "rating": 4.7, "members": 95,
     "description": "Vocal and instrumental performances, jam sessions.",
     "contact": "music@college.edu",   "meet": "Mon & Wed 5 PM",        "room": "Auditorium Hall"},
    {"id": 4,  "name": "Dance Club",            "category": "arts",       "rating": 4.6, "members": 110,
     "description": "Classical, western, and fusion dance workshops.",
     "contact": "dance@college.edu",   "meet": "Tue & Thu 5 PM",        "room": "Activity Room"},
    {"id": 5,  "name": "Cricket Club",          "category": "sports",     "rating": 4.4, "members": 70,
     "description": "Inter-college cricket tournaments and practice sessions.",
     "contact": "cricket@college.edu", "meet": "Daily 6 AM",            "room": "Main Ground"},
    {"id": 6,  "name": "Basketball Club",       "category": "sports",     "rating": 4.3, "members": 60,
     "description": "Training camps and league matches.",
     "contact": "bball@college.edu",   "meet": "Daily 6 PM",            "room": "Basketball Court"},
    {"id": 7,  "name": "Photography Club",      "category": "creative",   "rating": 4.6, "members": 75,
     "description": "Photography walks, editing workshops, and exhibitions.",
     "contact": "photo@college.edu",   "meet": "Every Friday 4 PM",     "room": "Media Lab"},
    {"id": 8,  "name": "Entrepreneurship Cell", "category": "business",   "rating": 4.9, "members": 130,
     "description": "Startup pitches, mentorship, and networking events.",
     "contact": "ecell@college.edu",   "meet": "Every Saturday 2 PM",   "room": "Conference Room"},
    {"id": 9,  "name": "Literary Club",         "category": "academic",   "rating": 4.5, "members": 88,
     "description": "Debates, quizzes, creative writing, and book clubs.",
     "contact": "literary@college.edu","meet": "Every Wednesday 4 PM",  "room": "Seminar Hall"},
    {"id": 10, "name": "Environmental Club",    "category": "social",     "rating": 4.7, "members": 105,
     "description": "Tree plantation drives, awareness campaigns.",
     "contact": "enviro@college.edu",  "meet": "Every Sunday 9 AM",     "room": "Garden Area"},
]

EVENTS = [
    {"id": 1,  "name": "Hackathon 2026",            "category": "technology", "date": "30 April 2026",
     "club": "Coding Club",          "seats": 200, "registered": 143, "prize": "₹50,000",
     "description": "24-hour coding challenge with prizes worth ₹50,000.",
     "venue": "Main Auditorium", "time": "9:00 AM"},
    {"id": 2,  "name": "Tech Fest Workshop",         "category": "technology", "date": "5 May 2026",
     "club": "Robotics Club",         "seats": 60,  "registered": 41,  "prize": "Certificate",
     "description": "Hands-on Arduino and Raspberry Pi workshop.",
     "venue": "Lab 2A", "time": "10:00 AM"},
    {"id": 3,  "name": "Melody Night",               "category": "arts",       "date": "2 May 2026",
     "club": "Music Club",            "seats": 300, "registered": 210, "prize": "Trophy",
     "description": "Annual cultural music concert open to all students.",
     "venue": "Open Air Theatre", "time": "6:00 PM"},
    {"id": 4,  "name": "Dance Fiesta",               "category": "arts",       "date": "8 May 2026",
     "club": "Dance Club",            "seats": 150, "registered": 98,  "prize": "₹20,000",
     "description": "Inter-college dance competition with celebrity judge.",
     "venue": "Main Auditorium", "time": "5:00 PM"},
    {"id": 5,  "name": "Inter-College Cricket Cup",  "category": "sports",     "date": "10 May 2026",
     "club": "Cricket Club",          "seats": 100, "registered": 56,  "prize": "Trophy + Medal",
     "description": "Weekend tournament — register your team now.",
     "venue": "Main Ground", "time": "8:00 AM"},
    {"id": 6,  "name": "3x3 Basketball League",      "category": "sports",     "date": "12 May 2026",
     "club": "Basketball Club",       "seats": 80,  "registered": 44,  "prize": "Medal",
     "description": "Fast-paced 3-on-3 format open to all years.",
     "venue": "Basketball Court", "time": "4:00 PM"},
    {"id": 7,  "name": "Campus Photo Walk",          "category": "creative",   "date": "3 May 2026",
     "club": "Photography Club",      "seats": 40,  "registered": 32,  "prize": "Exhibition Feature",
     "description": "Guided photography walk with editing masterclass.",
     "venue": "Campus Garden", "time": "7:00 AM"},
    {"id": 8,  "name": "Startup Pitch Day",          "category": "business",   "date": "15 May 2026",
     "club": "Entrepreneurship Cell", "seats": 50,  "registered": 35,  "prize": "Seed Funding",
     "description": "Pitch your idea to investors and win seed funding.",
     "venue": "Conference Room", "time": "11:00 AM"},
    {"id": 9,  "name": "Annual Debate Championship", "category": "academic",   "date": "7 May 2026",
     "club": "Literary Club",         "seats": 120, "registered": 78,  "prize": "₹10,000",
     "description": "Open debate on technology and society topics.",
     "venue": "Seminar Hall", "time": "9:00 AM"},
    {"id": 10, "name": "Green Campus Drive",         "category": "social",     "date": "18 May 2026",
     "club": "Environmental Club",    "seats": 200, "registered": 87,  "prize": "Certificate",
     "description": "Plantation drive and sustainability workshop.",
     "venue": "Campus Ground", "time": "8:00 AM"},
]

CATEGORIES = ["technology", "arts", "sports", "creative", "business", "academic", "social"]

# ── SESSION STATE ────────────────────────────────────────────
session = {
    "user_name": "",
    "interests": [],
    "rsvp_events": [],      # list of event IDs
    "fav_clubs": [],        # list of club IDs
    "search_history": [],
}

# ── DISPLAY HELPERS ─────────────────────────────────────────
W = 64  # box width

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def line(char="─", w=W, color=Fore.BLUE):
    print(color + char * w + Style.RESET_ALL)

def dline(color=Fore.BLUE):
    print(color + "═" * W + Style.RESET_ALL)

def box_title(text, color=Back.BLUE):
    pad = (W - len(text) - 2) // 2
    print(color + Fore.WHITE + Style.BRIGHT +
          " " * pad + " " + text + " " + " " * pad + Style.RESET_ALL)

def stars(rating):
    full = int(rating)
    half = 1 if (rating - full) >= 0.5 else 0
    empty = 5 - full - half
    return yellow("★" * full) + yellow("½" * half) + gray("☆" * empty) + f" {rating}"

def seat_bar(registered, total, width=20):
    pct = registered / total
    filled = int(pct * width)
    bar = green("█" * filled) + gray("░" * (width - filled))
    status = red(" ALMOST FULL") if pct > 0.85 else (yellow(" FILLING UP") if pct > 0.6 else green(" OPEN"))
    return f"[{bar}] {registered}/{total}{status}"

def type_print(text, delay=0.012):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def loading(msg="Loading", steps=12):
    print(blue(msg) + " ", end="", flush=True)
    for _ in range(steps):
        time.sleep(0.04)
        print(blue("▓"), end="", flush=True)
    print(" " + green("Done!"))
    time.sleep(0.2)

def prompt(msg):
    return input(yellow("  ▶ ") + white(msg) + " ").strip()

# ── BANNER ──────────────────────────────────────────────────
def show_banner():
    clear()
    dline(Fore.CYAN)
    print(Fore.CYAN + Style.BRIGHT + """
   ██████╗██╗     ██╗   ██╗██████╗     ██████╗ ██╗███████╗
  ██╔════╝██║     ██║   ██║██╔══██╗    ██╔══██╗██║██╔════╝
  ██║     ██║     ██║   ██║██████╔╝    ██║  ██║██║███████╗
  ██║     ██║     ██║   ██║██╔══██╗    ██║  ██║██║╚════██║
  ╚██████╗███████╗╚██████╔╝██████╔╝    ██████╔╝██║███████║
   ╚═════╝╚══════╝ ╚═════╝ ╚═════╝     ╚═════╝ ╚═╝╚══════╝
    """ + Style.RESET_ALL)
    print(Fore.WHITE + Style.BRIGHT +
          "        ✦  EVENT & CLUB DISCOVERY PLATFORM  ✦".center(W))
    print(gray("         B.Tech 2nd Sem | Group 12 | Design Thinking".center(W)))
    dline(Fore.CYAN)

# ── LOGIN ────────────────────────────────────────────────────
def login():
    show_banner()
    print()
    type_print(blue("  Welcome! Let's get you set up."))
    print()
    name = prompt("Enter your name:")
    if not name:
        name = "Student"
    session["user_name"] = name
    loading(f"  Setting up your profile, {name}")
    print()
    print(success_bg(f"  Hello, {name}! Your session is ready.  "))
    time.sleep(0.8)

# ── MAIN MENU ────────────────────────────────────────────────
def show_menu():
    clear()
    dline()
    box_title(f"  CLUB & EVENT DISCOVERY  —  Hi, {session['user_name']}!  ")
    dline()

    now = datetime.now().strftime("%d %b %Y  %I:%M %p")
    fav_count  = len(session["fav_clubs"])
    rsvp_count = len(session["rsvp_events"])
    interests  = ", ".join(i.capitalize() for i in session["interests"]) or "Not set"

    print(gray(f"  📅 {now}".ljust(W)))
    print(gray(f"  🎯 Interests : ") + yellow(interests))
    print(gray(f"  ❤️  Favourites: ") + magenta(f"{fav_count} clubs") +
          gray("  |  ") + green(f"🎟  {rsvp_count} RSVPs"))
    line()

    menu_items = [
        ("1", "🎯", "Set / Update My Interests"),
        ("2", "⭐", "Get Personalized Recommendations"),
        ("3", "🏛 ", "Browse All Clubs"),
        ("4", "📅", "Browse All Upcoming Events"),
        ("5", "🔍", "Search by Keyword"),
        ("6", "❤️ ", "My Favourites & RSVPs"),
        ("7", "📊", "Platform Statistics"),
        ("8", "🗂 ", "Search History"),
        ("9", "🚪", "Exit"),
    ]
    for key, icon, label in menu_items:
        k_colored = bold(blue(f"  [{key}]"))
        print(f"{k_colored}  {icon}  {white(label)}")

    line()
    return prompt("Enter your choice [1-9]:")

# ── SET INTERESTS ────────────────────────────────────────────
def set_interests():
    clear()
    dline()
    box_title("  SET YOUR INTERESTS  ")
    dline()
    print()
    print(white("  Choose the categories that interest you:"))
    print()
    for i, cat in enumerate(CATEGORIES, 1):
        color, icon = CAT_STYLE.get(cat, (Fore.WHITE, "•"))
        tick = green(" ✔") if cat in session["interests"] else gray("  ")
        print(f"  {bold(blue(str(i)))}. {color}{icon}  {cat.capitalize():<14}{Style.RESET_ALL}{tick}")
    print()
    print(gray("  Enter numbers separated by commas (e.g. 1,3,5)"))
    print(gray("  Press ENTER to keep current interests"))
    raw = prompt("Your choice:")

    if not raw:
        print(yellow("\n  Interests unchanged."))
        time.sleep(0.8)
        return

    chosen = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit():
            idx = int(part) - 1
            if 0 <= idx < len(CATEGORIES):
                chosen.append(CATEGORIES[idx])

    chosen = list(set(chosen))
    if chosen:
        session["interests"] = chosen
        print()
        print(success_bg("  Interests saved!  "))
        print()
        for c in chosen:
            color, icon = CAT_STYLE.get(c, (Fore.WHITE, "•"))
            print(f"    {color}{icon}  {c.capitalize()}{Style.RESET_ALL}")
    else:
        print(err_bg("  No valid selection. Please try again.  "))
    time.sleep(1.2)

# ── CLUB CARD ────────────────────────────────────────────────
def print_club_card(c, detailed=False):
    fav = " ❤️" if c["id"] in session["fav_clubs"] else ""
    line("─", W, Fore.BLUE)
    print(f"  {bold(white(c['name']))}{yellow(fav)}  {cat_label(c['category'])}")
    print(f"  {stars(c['rating'])}   👥 {c['members']} members")
    print(f"  {gray(c['description'])}")
    if detailed:
        print(f"  {blue('📍')} {c['room']}   {blue('⏰')} {c['meet']}")
        print(f"  {blue('📧')} {c['contact']}")

# ── EVENT CARD ───────────────────────────────────────────────
def print_event_card(e, detailed=False):
    rsvp = " 🎟 RSVP'd" if e["id"] in session["rsvp_events"] else ""
    seats_left = e["seats"] - e["registered"]
    line("─", W, Fore.CYAN)
    print(f"  {bold(white(e['name']))}{green(rsvp)}")
    print(f"  {cat_label(e['category'])}   📅 {yellow(e['date'])}   ⏰ {e['time']}")
    print(f"  🏛  {e['club']}   📍 {e['venue']}")
    print(f"  🏆 Prize: {green(e['prize'])}")
    print(f"  Seats: {seat_bar(e['registered'], e['seats'])}")
    print(f"  {gray(e['description'])}")
    if detailed:
        print(f"  {yellow(f'Seats Remaining: {seats_left}')}")

# ── RECOMMENDATIONS ──────────────────────────────────────────
def show_recommendations():
    if not session["interests"]:
        print(err_bg("  Please set your interests first! (Option 1)  "))
        time.sleep(1.2)
        return

    clubs  = [c for c in CLUBS  if c["category"] in session["interests"]]
    events = [e for e in EVENTS if e["category"] in session["interests"]]

    # sort: clubs by rating desc, events by seats remaining asc (urgent first)
    clubs  = sorted(clubs,  key=lambda x: -x["rating"])
    events = sorted(events, key=lambda x: x["seats"] - x["registered"])

    clear()
    dline()
    box_title("  ⭐  PERSONALIZED RECOMMENDATIONS  ⭐  ")
    dline()
    int_str = ", ".join(i.capitalize() for i in session["interests"])
    print(f"  Based on your interests: {yellow(int_str)}")
    print()

    if not clubs and not events:
        print(red("  No matches found for your interests."))
    else:
        print(bold(white(f"  🏛  CLUBS FOR YOU  ({len(clubs)} found)")))
        for c in clubs:
            print_club_card(c)
        line()
        print(bold(white(f"\n  📅  EVENTS FOR YOU  ({len(events)} found)")))
        for e in events:
            print_event_card(e)
        line()

    print()
    post_rec_actions(clubs, events)

def post_rec_actions(clubs, events):
    print(white("  What would you like to do?"))
    print(f"  {bold(blue('[F]'))}  Add a club to Favourites")
    print(f"  {bold(blue('[R]'))}  RSVP to an Event")
    print(f"  {bold(blue('[B]'))}  Back to Menu")
    act = prompt("Choice:").upper()
    if act == "F":
        add_favourite(clubs)
    elif act == "R":
        rsvp_event(events)

# ── ALL CLUBS ────────────────────────────────────────────────
def browse_clubs():
    clear()
    dline()
    box_title("  🏛   ALL CLUBS  ")
    dline()
    sort_choice = prompt("Sort by: [1] Rating  [2] Name  [3] Members  (default 1):") or "1"
    if sort_choice == "2":
        clubs = sorted(CLUBS, key=lambda x: x["name"])
    elif sort_choice == "3":
        clubs = sorted(CLUBS, key=lambda x: -x["members"])
    else:
        clubs = sorted(CLUBS, key=lambda x: -x["rating"])

    for c in clubs:
        print_club_card(c)
    line()

    ans = prompt("Enter club ID for details, [F] to favourite, or ENTER to go back:").upper()
    if ans == "F":
        add_favourite(clubs)
    elif ans.isdigit():
        view_club_detail(int(ans))

def view_club_detail(cid):
    club = next((c for c in CLUBS if c["id"] == cid), None)
    if not club:
        print(red("  Club not found."))
        time.sleep(1)
        return
    clear()
    dline()
    box_title(f"  {club['name'].upper()}  ")
    dline()
    print_club_card(club, detailed=True)
    line()
    ans = prompt("[F] Add to Favourites  |  ENTER to go back:").upper()
    if ans == "F":
        add_favourite([club])

# ── ALL EVENTS ───────────────────────────────────────────────
def browse_events():
    clear()
    dline()
    box_title("  📅   ALL UPCOMING EVENTS  ")
    dline()
    sort_choice = prompt("Sort by: [1] Date  [2] Seats Left  [3] Category  (default 1):") or "1"
    if sort_choice == "2":
        events = sorted(EVENTS, key=lambda x: x["seats"] - x["registered"])
    elif sort_choice == "3":
        events = sorted(EVENTS, key=lambda x: x["category"])
    else:
        events = EVENTS[:]

    for e in events:
        print_event_card(e)
    line()

    ans = prompt("Enter event ID to RSVP, [D] for details, or ENTER to go back:").upper()
    if ans.isdigit():
        rsvp_event([e for e in events if e["id"] == int(ans)])
    elif ans == "D":
        eid = prompt("Enter event ID:")
        if eid.isdigit():
            ev = next((e for e in EVENTS if e["id"] == int(eid)), None)
            if ev:
                clear(); print_event_card(ev, detailed=True)
                input(gray("\n  Press ENTER to go back..."))

# ── KEYWORD SEARCH ───────────────────────────────────────────
def keyword_search():
    clear()
    dline()
    box_title("  🔍   KEYWORD SEARCH  ")
    dline()
    print()
    kw = prompt("Enter keyword:")
    if not kw:
        return
    # save to history
    if kw not in session["search_history"]:
        session["search_history"].append(kw)

    loading(f"  Searching for '{kw}'")

    kw_l = kw.lower()
    c_res = [c for c in CLUBS  if kw_l in c["name"].lower() or kw_l in c["description"].lower() or kw_l in c["category"]]
    e_res = [e for e in EVENTS if kw_l in e["name"].lower() or kw_l in e["description"].lower() or kw_l in e["category"] or kw_l in e["club"].lower()]

    dline()
    print(f"  Results for: {bold(yellow(kw))}  —  {green(str(len(c_res)))} clubs, {green(str(len(e_res)))} events")
    line()

    if c_res:
        print(bold(white(f"  MATCHING CLUBS ({len(c_res)})")))
        for c in c_res:
            print_club_card(c)
    else:
        print(gray("  No matching clubs found."))

    line()

    if e_res:
        print(bold(white(f"  MATCHING EVENTS ({len(e_res)})")))
        for e in e_res:
            print_event_card(e)
    else:
        print(gray("  No matching events found."))

    line()
    ans = prompt("[F] Favourite a club  |  [R] RSVP an event  |  ENTER to go back:").upper()
    if ans == "F":
        add_favourite(c_res)
    elif ans == "R":
        rsvp_event(e_res)

# ── FAVOURITES & RSVP VIEW ───────────────────────────────────
def my_favourites():
    clear()
    dline()
    box_title("  ❤️   MY FAVOURITES & RSVPs  ")
    dline()

    fav_clubs  = [c for c in CLUBS  if c["id"] in session["fav_clubs"]]
    rsvp_events = [e for e in EVENTS if e["id"] in session["rsvp_events"]]

    print(bold(white(f"\n  ❤️  FAVOURITE CLUBS ({len(fav_clubs)})")))
    if fav_clubs:
        for c in fav_clubs:
            print_club_card(c, detailed=True)
    else:
        print(gray("  You haven't favourited any clubs yet."))

    line()
    print(bold(white(f"\n  🎟  RSVP'd EVENTS ({len(rsvp_events)})")))
    if rsvp_events:
        for e in rsvp_events:
            print_event_card(e, detailed=True)
    else:
        print(gray("  You haven't RSVP'd to any events yet."))
    line()

    print(f"  {bold(blue('[R]'))} Remove a club from favourites  |  {bold(blue('[C]'))} Cancel an RSVP  |  ENTER to go back")
    ans = prompt("Choice:").upper()
    if ans == "R" and fav_clubs:
        cid = prompt("Enter Club ID to remove from favourites:")
        if cid.isdigit() and int(cid) in session["fav_clubs"]:
            session["fav_clubs"].remove(int(cid))
            print(success_bg("  Removed from favourites.  "))
            time.sleep(0.8)
    elif ans == "C" and rsvp_events:
        eid = prompt("Enter Event ID to cancel RSVP:")
        if eid.isdigit() and int(eid) in session["rsvp_events"]:
            session["rsvp_events"].remove(int(eid))
            # restore seat
            ev = next((e for e in EVENTS if e["id"] == int(eid)), None)
            if ev: ev["registered"] = max(0, ev["registered"] - 1)
            print(warn_bg("  RSVP cancelled.  "))
            time.sleep(0.8)

# ── STATISTICS ───────────────────────────────────────────────
def show_stats():
    clear()
    dline()
    box_title("  📊   PLATFORM STATISTICS  ")
    dline()

    total_members = sum(c["members"] for c in CLUBS)
    total_registered = sum(e["registered"] for e in EVENTS)
    total_seats = sum(e["seats"] for e in EVENTS)
    avg_rating = sum(c["rating"] for c in CLUBS) / len(CLUBS)
    most_popular_club  = max(CLUBS,  key=lambda x: x["members"])
    most_popular_event = max(EVENTS, key=lambda x: x["registered"])
    hottest_event      = min(EVENTS, key=lambda x: x["seats"] - x["registered"])

    print(f"\n  {bold(white('OVERVIEW'))}")
    line("─", 40)
    print(f"  🏛  Total Clubs      : {yellow(str(len(CLUBS)))}")
    print(f"  📅  Total Events     : {yellow(str(len(EVENTS)))}")
    print(f"  👥  Total Members    : {yellow(str(total_members))}")
    print(f"  🎟  Total RSVPs      : {yellow(str(total_registered))} / {total_seats} seats")
    print(f"  ⭐  Avg Club Rating  : {stars(round(avg_rating, 1))}")

    line("─", 40)
    print(f"\n  {bold(white('HIGHLIGHTS'))}")
    line("─", 40)
    print(f"  🥇 Most Members  : {green(most_popular_club['name'])} ({most_popular_club['members']} members)")
    print(f"  🔥 Hottest Event : {red(hottest_event['name'])}  ", end="")
    left = hottest_event["seats"] - hottest_event["registered"]
    print(red(f"Only {left} seats left!"))
    print(f"  📈 Most RSVP'd   : {green(most_popular_event['name'])} ({most_popular_event['registered']} registrations)")

    line("─", 40)
    print(f"\n  {bold(white('EVENTS BY CATEGORY'))}")
    line("─", 40)
    cat_counts = {}
    for e in EVENTS:
        cat_counts[e["category"]] = cat_counts.get(e["category"], 0) + 1
    for cat, cnt in sorted(cat_counts.items(), key=lambda x: -x[1]):
        bar_len = cnt * 6
        bar = green("█" * bar_len)
        print(f"  {cat_label(cat):<30}  {bar}  {cnt}")

    line("─", 40)
    print(f"\n  {bold(white('YOUR SESSION STATS'))}")
    line("─", 40)
    print(f"  ❤️  Clubs Favourited : {magenta(str(len(session['fav_clubs'])))}")
    print(f"  🎟  Events RSVP'd   : {green(str(len(session['rsvp_events'])))}")
    print(f"  🔍  Searches Done   : {blue(str(len(session['search_history'])))}")
    line()
    input(gray("  Press ENTER to go back..."))

# ── SEARCH HISTORY ───────────────────────────────────────────
def show_history():
    clear()
    dline()
    box_title("  🗂   SEARCH HISTORY  ")
    dline()
    if not session["search_history"]:
        print(gray("  No searches yet this session."))
    else:
        for i, kw in enumerate(session["search_history"], 1):
            print(f"  {blue(str(i)+'.')}  {white(kw)}")
    line()
    ans = prompt("[S] Search again  |  [C] Clear history  |  ENTER to go back:").upper()
    if ans == "S":
        kw_idx = prompt("Enter number to search again:")
        if kw_idx.isdigit():
            idx = int(kw_idx) - 1
            if 0 <= idx < len(session["search_history"]):
                session["search_history"].append(session["search_history"][idx])
                keyword_search()
    elif ans == "C":
        session["search_history"].clear()
        print(success_bg("  History cleared.  "))
        time.sleep(0.8)

# ── FAVOURITE A CLUB ─────────────────────────────────────────
def add_favourite(clubs):
    if not clubs:
        print(gray("  No clubs to favourite."))
        time.sleep(0.8)
        return
    print()
    for c in clubs:
        fav = " ❤️" if c["id"] in session["fav_clubs"] else ""
        print(f"  {bold(blue(str(c['id'])))}.  {c['name']}{fav}")
    cid = prompt("Enter Club ID to add to favourites (ENTER to skip):")
    if cid.isdigit():
        cid = int(cid)
        if any(c["id"] == cid for c in clubs):
            if cid not in session["fav_clubs"]:
                session["fav_clubs"].append(cid)
                club_name = next(c["name"] for c in CLUBS if c["id"] == cid)
                print(success_bg(f"  ❤️  {club_name} added to favourites!  "))
            else:
                print(yellow("  Already in favourites!"))
        else:
            print(red("  Invalid club ID."))
    time.sleep(0.8)

# ── RSVP AN EVENT ────────────────────────────────────────────
def rsvp_event(events):
    if not events:
        print(gray("  No events available."))
        time.sleep(0.8)
        return
    print()
    for e in events:
        rsvp = " 🎟" if e["id"] in session["rsvp_events"] else ""
        seats_left = e["seats"] - e["registered"]
        print(f"  {bold(blue(str(e['id'])))}.  {e['name']}{rsvp}  —  {yellow(e['date'])}  [{seats_left} seats left]")
    eid = prompt("Enter Event ID to RSVP (ENTER to skip):")
    if eid.isdigit():
        eid = int(eid)
        ev = next((e for e in EVENTS if e["id"] == eid), None)
        if ev:
            if eid in session["rsvp_events"]:
                print(yellow("  You already RSVP'd to this event!"))
            elif ev["registered"] >= ev["seats"]:
                print(err_bg("  Sorry! This event is FULL.  "))
            else:
                session["rsvp_events"].append(eid)
                ev["registered"] += 1
                print(success_bg(f"  🎟  RSVP confirmed for: {ev['name']}!  "))
                print(green(f"  📅 {ev['date']}  ⏰ {ev['time']}  📍 {ev['venue']}"))
        else:
            print(red("  Invalid event ID."))
    time.sleep(1.0)

# ── EXIT SCREEN ──────────────────────────────────────────────
def show_exit():
    clear()
    dline(Fore.CYAN)
    print()
    type_print(blue("  Thank you for using Club & Event Discovery Platform!"), 0.02)
    print()
    print(f"  {bold(white('SESSION SUMMARY'))}")
    line("─", 40, Fore.CYAN)
    print(f"  👤  User           : {yellow(session['user_name'])}")
    print(f"  ❤️   Clubs Saved    : {magenta(str(len(session['fav_clubs'])))}")
    print(f"  🎟   Events RSVP'd : {green(str(len(session['rsvp_events'])))}")
    print(f"  🔍  Searches Done  : {blue(str(len(session['search_history'])))}")
    print()
    print(gray("  B.Tech 2nd Semester | Group 12 | Design Thinking & Algorithms"))
    print()
    dline(Fore.CYAN)
    print()

# ── MAIN LOOP ────────────────────────────────────────────────
def main():
    login()

    while True:
        choice = show_menu()

        if   choice == "1": set_interests()
        elif choice == "2": show_recommendations()
        elif choice == "3": browse_clubs()
        elif choice == "4": browse_events()
        elif choice == "5": keyword_search()
        elif choice == "6": my_favourites()
        elif choice == "7": show_stats()
        elif choice == "8": show_history()
        elif choice == "9":
            show_exit()
            break
        else:
            print(err_bg("  Invalid choice. Enter a number between 1 and 9.  "))
            time.sleep(0.8)

if __name__ == "__main__":
    main()