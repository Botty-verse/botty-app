"""
Botty voor Badger2040 — NOLAI offline Tamagotchi
Bewaar als botty.py in de examples/ map op je Badger.
Knoppen: A=data  B=beweeg  C=dilemma/genees  UP=stats  DOWN=terug
"""

import badger2040
import badger_os
import time
import random

display = badger2040.Badger2040()
display.set_update_speed(badger2040.UPDATE_FAST)
BREEDTE, HOOGTE = 296, 128

# ── state ─────────────────────────────────────────────────────────────────────
DEFAULT = {
    "naam": "Botty", "stadium": 1,
    "energie": 80, "data": 75, "fit": 70, "stemming": 65,
    "ziek": False, "leeftijd": 0,
}
state = {}
badger_os.state_load("botty", state)
if "naam" not in state:
    state.update(DEFAULT)
    badger_os.state_save("botty", state)

SCHERM = 0
bericht = ""
bericht_t = 0
last_tick = time.time()

# ── game logic ────────────────────────────────────────────────────────────────
def clamp(v): return max(0.0, min(100.0, float(v)))

def tick():
    state["energie"]  = clamp(state["energie"]  - 1.5)
    state["data"]     = clamp(state["data"]      - 1.0)
    state["fit"]      = clamp(state["fit"]       - 0.8)
    state["stemming"] = clamp(state["stemming"]  - 0.6)
    state["leeftijd"] += 1
    for i, d in enumerate([0, 50, 150, 350, 700]):
        if state["leeftijd"] >= d:
            state["stadium"] = i + 1
    if not state["ziek"] and random.random() < 0.02:
        state["ziek"] = True
    badger_os.state_save("botty", state)

def avg_mood():
    return (state["energie"] + state["data"] + state["fit"] + state["stemming"]) / 4

def flash(msg):
    global bericht, bericht_t
    bericht = msg
    bericht_t = time.time()

def act_data():
    state["energie"]  = clamp(state["energie"]  + 20)
    state["data"]     = clamp(state["data"]      + 24)
    state["stemming"] = clamp(state["stemming"]  + 8)
    badger_os.state_save("botty", state)
    flash("Data gevoed!")

def act_beweeg():
    state["fit"]      = clamp(state["fit"]      + 22)
    state["stemming"] = clamp(state["stemming"] + 8)
    badger_os.state_save("botty", state)
    flash("Bewogen!")

def act_dilemma():
    if state["ziek"]:
        state["ziek"] = False
        state["stemming"] = clamp(state["stemming"] + 20)
        flash("Beter!")
    else:
        state["stemming"] = clamp(state["stemming"] + 12)
        flash("Dilemma opgelost!")
    badger_os.state_save("botty", state)

def stadium_naam():
    return ["","Baby","Peuter","Kind","Tiener","Volwassen"][min(state["stadium"],5)]

def mood_label():
    m = avg_mood()
    if state["ziek"]: return "Ziek"
    if m >= 80: return "Blij"
    if m >= 60: return "Oke"
    if m >= 40: return "Moe"
    return "Slecht"

# ── Tekenhulpen ───────────────────────────────────────────────────────────────
def blk(): display.set_pen(0)
def wht(): display.set_pen(15)

def rrect(x, y, w, h, r):
    """Afgeronde rechthoek: zwarte outline met witte vulling."""
    blk()
    display.rectangle(x + r, y, w - 2 * r, h)
    display.rectangle(x, y + r, w, h - 2 * r)
    display.circle(x + r,         y + r,         r)
    display.circle(x + w - r - 1, y + r,         r)
    display.circle(x + r,         y + h - r - 1, r)
    display.circle(x + w - r - 1, y + h - r - 1, r)
    wht()
    display.rectangle(x + r + 1,     y + 1,     w - 2 * r - 2, h - 2)
    display.rectangle(x + 1,         y + r + 1, w - 2,         h - 2 * r - 2)
    display.circle(x + r + 1,         y + r + 1,         max(0, r - 1))
    display.circle(x + w - r - 2,     y + r + 1,         max(0, r - 1))
    display.circle(x + r + 1,         y + h - r - 2,     max(0, r - 1))
    display.circle(x + w - r - 2,     y + h - r - 2,     max(0, r - 1))

def rrect_fill(x, y, w, h, r):
    """Afgeronde rechthoek: volledig zwart gevuld."""
    blk()
    display.rectangle(x + r, y, w - 2 * r, h)
    display.rectangle(x, y + r, w, h - 2 * r)
    display.circle(x + r,         y + r,         r)
    display.circle(x + w - r - 1, y + r,         r)
    display.circle(x + r,         y + h - r - 1, r)
    display.circle(x + w - r - 1, y + h - r - 1, r)

# ── Botty pixel-art ───────────────────────────────────────────────────────────
# SVG viewBox 0 0 200 250, scale=0.45, offset dx=28 dy=9
# Visor scanlines (y, x_left, x_right) relatief aan character origin
VISOR = [
    (23,26,38),(24,22,42),(25,20,44),(26,20,44),(27,20,44),
    (28,20,44),(29,20,44),(30,20,44),(31,21,43),(32,21,43),
    (33,22,42),(34,23,41),(35,24,40),(36,24,40),(37,25,39),
    (38,25,39),(39,26,38),(40,27,37),(41,28,36),(42,28,36),
    (43,29,35),(44,29,35),(45,31,33),
]
MOND_BLIJ = [
    (39,29,35),(40,29,35),(41,29,35),(42,29,35),
    (43,30,34),(44,30,34),(45,31,33),
]

def draw_botty(ox, oy):
    mood = avg_mood()
    ziek = state["ziek"]

    def ln(x1, y1, x2, y2): display.line(ox+x1, oy+y1, ox+x2, oy+y2)
    def ci(x, y, r):        display.circle(ox+x, oy+y, r)
    def rc(x, y, w, h):     display.rectangle(ox+x, oy+y, w, h)

    # antenne
    blk()
    ln(32,16, 34,10)
    ln(34,10, 36,4)
    ci(37, 3, 3)
    wht()
    ci(37, 3, 1)

    # oren (eerst, hoofd eroverheen)
    blk(); ci(10,30,5); wht(); ci(10,30,2)
    blk(); ci(54,30,5); wht(); ci(54,30,2)

    # hoofd: afgeronde vierkant (x=10,y=13 w=44 h=43 r=9)
    blk()
    rc(19,13,26,43); rc(10,22,44,25)
    ci(19,22,9); ci(45,22,9); ci(19,47,9); ci(45,47,9)
    wht()
    rc(20,14,24,41); rc(11,23,42,23)
    ci(20,23,8); ci(44,23,8); ci(20,46,8); ci(44,46,8)

    # visor (zwart gevuld)
    blk()
    for vy, vl, vr in VISOR:
        display.line(ox+vl, oy+vy, ox+vr, oy+vy)

    # ogen (wit)
    if ziek:
        blk()
        ln(25,29,29,35); ln(29,29,25,35)
        ln(35,29,39,35); ln(39,29,35,35)
    else:
        wht()
        for dx in range(3):
            ln(27+dx,31, 27+dx,36)
            ln(37+dx,31, 37+dx,36)

    # mond (wit op visor)
    wht()
    if mood >= 60:
        for my, ml, mr in MOND_BLIJ:
            display.line(ox+ml, oy+my, ox+mr, oy+my)
    elif mood >= 35:
        ln(29,42, 35,42)
    else:
        for my, ml, mr in MOND_BLIJ:
            display.line(ox+ml, oy+(45-(my-39)), ox+mr, oy+(45-(my-39)))

    # nek
    blk()
    ln(29,51,35,54); ln(35,54,29,56); ln(29,56,35,58)

    # romp (x=17,y=58 w=30 h=23 r=7)
    blk()
    rc(24,58,16,23); rc(17,65,30,9)
    ci(24,65,7); ci(40,65,7); ci(24,74,7); ci(40,74,7)
    wht()
    rc(25,59,14,21); rc(18,66,28,7)
    ci(25,66,6); ci(39,66,6); ci(25,73,6); ci(39,73,6)

    # borst-paneel (x=25,y=63 w=14 h=9 r=3)
    blk()
    rc(28,63,8,9); rc(25,66,14,3)
    ci(28,66,3); ci(36,66,3); ci(28,69,3); ci(36,69,3)
    wht()
    rc(29,64,6,7); rc(26,67,12,1)
    ci(29,67,2); ci(35,67,2); ci(29,68,2); ci(35,68,2)

    # armen
    blk()
    ln(17,66,3,78);  ci(2,80,3);  wht(); ci(2,80,1)
    blk()
    ln(47,66,61,78); ci(62,80,3); wht(); ci(62,80,1)

    # korte broek (x=18,y=78 w=28 h=13 r=5)
    blk()
    rc(23,78,18,13); rc(18,83,28,3)
    ci(23,83,5); ci(41,83,5); ci(23,86,5); ci(41,86,5)
    wht()
    rc(19,80,12,10)
    rc(33,80,12,10)
    blk()
    ln(32,78,32,91)

    # benen
    blk()
    ln(26,91,23,102)
    ln(38,91,41,102)

    # voeten
    blk()
    rc(19,101,8,4); ci(19,103,2); ci(26,103,2)
    wht(); rc(20,102,6,2)
    blk()
    rc(39,101,8,4); ci(39,103,2); ci(46,103,2)
    wht(); rc(40,102,6,2)

# ── Balk ──────────────────────────────────────────────────────────────────────
PANEL_X = 78
PANEL_W = 210
BAR_H   = 16

def balk(y, label, val):
    blk()
    display.rectangle(PANEL_X, y, PANEL_W, BAR_H)
    wht()
    display.rectangle(PANEL_X + 1, y + 1, PANEL_W - 2, BAR_H - 2)
    fill = max(0, int((PANEL_W - 2) * val / 100))
    if fill > 0:
        blk()
        display.rectangle(PANEL_X + 1, y + 1, fill, BAR_H - 2)
    text_col = 15 if fill > 45 else 0
    display.set_pen(text_col)
    display.text(label, PANEL_X + 4, y + 3, 400, 1)
    val_str = str(int(val))
    val_x = PANEL_X + PANEL_W - len(val_str) * 8 - 4
    text_col2 = 15 if fill > PANEL_W - len(val_str) * 8 - 10 else 0
    display.set_pen(text_col2)
    display.text(val_str, val_x, y + 3, 400, 1)

# ── Hoofd scherm ──────────────────────────────────────────────────────────────
def draw_hoofd():
    wht(); display.clear()
    draw_botty(ox=2, oy=8)

    blk()
    display.line(72, 0, 72, 113)
    display.line(0, 113, BREEDTE, 113)

    naam = state["naam"]
    mood = mood_label()
    blk()
    display.text(naam, PANEL_X, 4, 400, 2)
    mood_x = PANEL_X + PANEL_W - len(mood) * 8
    display.text(mood, mood_x, 8, 400, 1)

    BAR_START = 28
    slot = (113 - BAR_START) // 4
    balk(BAR_START,          "Energie",  state["energie"])
    balk(BAR_START + slot,   "Data",     state["data"])
    balk(BAR_START + slot*2, "Fit",      state["fit"])
    balk(BAR_START + slot*3, "Stemming", state["stemming"])

    blk()
    display.text("A=data  B=beweeg  C=dilemma  UP=meer", 4, 116, 400, 1)

    if bericht and (time.time() - bericht_t) < 3:
        blk()
        display.rectangle(PANEL_X, 100, PANEL_W, 12)
        wht()
        display.text(bericht, PANEL_X + 4, 102, 400, 1)

# ── Stats scherm ──────────────────────────────────────────────────────────────
def draw_stats():
    wht(); display.clear()
    blk()
    display.text(state["naam"], 4, 2, 400, 2)
    display.text(stadium_naam(), 4, 22, 400, 1)
    display.text("Leeftijd: " + str(state["leeftijd"]), 130, 22, 400, 1)
    display.line(0, 32, BREEDTE, 32)

    items = [
        ("Energie",  state["energie"]),
        ("Data",     state["data"]),
        ("Fit",      state["fit"]),
        ("Stemming", state["stemming"]),
    ]
    for i, (lbl, val) in enumerate(items):
        balk(36 + i * 19, lbl, val)

    display.line(0, 114, BREEDTE, 114)
    blk()
    display.text("DOWN = terug", 4, 117, 400, 1)

# ── Hoofd lus ─────────────────────────────────────────────────────────────────
TICK_S = 30

def render():
    if SCHERM == 0:
        draw_hoofd()
    else:
        draw_stats()
    display.update()

render()
changed = False

while True:
    now = time.time()

    if now - last_tick >= TICK_S:
        tick()
        last_tick = now
        changed = True

    if display.pressed(badger2040.BUTTON_A):
        act_data()
        SCHERM = 0
        changed = True
        time.sleep_ms(250)

    if display.pressed(badger2040.BUTTON_B):
        act_beweeg()
        SCHERM = 0
        changed = True
        time.sleep_ms(250)

    if display.pressed(badger2040.BUTTON_C):
        act_dilemma()
        SCHERM = 0
        changed = True
        time.sleep_ms(250)

    if display.pressed(badger2040.BUTTON_UP):
        SCHERM = 1
        changed = True
        time.sleep_ms(250)

    if display.pressed(badger2040.BUTTON_DOWN):
        SCHERM = 0
        changed = True
        time.sleep_ms(250)

    if changed:
        render()
        changed = False

    time.sleep_ms(50)
