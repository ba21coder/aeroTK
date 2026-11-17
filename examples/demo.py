import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import aerotk as atk

app = atk.AeroApp(title="AeroTk v0.1.0 Showcase", size=(500, 420), theme="dark")

card = atk.AeroFrame(app, width=380, height=320, radius=16)
card.place(relx=0.5, rely=0.5, anchor="center")

title = atk.AeroLabel(card, text="AeroTk Login", size=18, weight="bold")
title.place(x=30, y=25)

sub = atk.AeroLabel(card, text="Zero dependencies. Pure speed.", size=10, muted=True)
sub.place(x=30, y=58)

user_input = atk.AeroEntry(card, placeholder="Username...", width=320, height=40)
user_input.place(x=30, y=100)

pass_input = atk.AeroEntry(card, placeholder="Password...", width=320, height=40)
pass_input.place(x=30, y=155)

def toggle_theme(is_light):
    app.set_theme("light" if is_light else "dark")

theme_lbl = atk.AeroLabel(card, text="Light Mode", size=10, muted=True)
theme_lbl.place(x=30, y=215)

theme_sw = atk.AeroSwitch(card, command=toggle_theme)
theme_sw.place(x=115, y=212)

def submit():
    print(f"Login attempt -> User: {user_input.get()} | Pass: {pass_input.get()}")

login_btn = atk.AeroButton(card, text="Sign In", command=submit, width=320, height=42)
login_btn.place(x=30, y=255)

app.run()
