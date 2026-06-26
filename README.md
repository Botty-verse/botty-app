# Botty — NOLAI AI-robot

**Botty** is an educational AI tamagotchi based on the mascot at [NOLAI (Nationaal OnderwijsLab AI)](https://nolai.nl). She lives at [botty.ramonmoorlag.nl](https://botty.ramonmoorlag.nl).

---

## What is Botty?

Botty is a digital robot you take care of — like a tamagotchi, but for AI literacy. You feed her data, make her exercise, and help her solve ethical dilemmas. As you care for her, she grows from a Baby AI to a fully Adult AI.

The goal is simple: make abstract AI concepts tangible and playful for students and the general public. How well can you take care of an AI?

---

## Project scope

This repository hosts the **Botty web app** and all related assets:

| File | Description |
|------|-------------|
| `index.html` | Landing page — hub for all Botty experiences |
| `botty.html` | The main Botty tamagotchi game (browser-based) |
| `kaarten.html` | Collector cards — automation levels and Botty emotions |
| `badger2040/botty.py` | Offline MicroPython app for the Pimoroni Badger2040 e-ink badge |
| `badger2040/botty.png` | BadgerOS launcher icon (86×86px) |
| `CNAME` | Custom domain: `botty.ramonmoorlag.nl` |

---

## Experiences

### 🤖 Botty Tamagotchi (web)
Play at **[botty.ramonmoorlag.nl/botty.html](https://botty.ramonmoorlag.nl/botty.html)**

- Give Botty **data** (feeds her energy and knowledge)
- Make her **move** (keeps her fit)
- Solve **ethical dilemmas** (improves her mood and health)
- Watch her grow through 5 life stages: Baby → Toddler → Child → Teen → Adult
- Available in **Dutch** and **English**

### 🃏 Collector Cards
Browse at **[botty.ramonmoorlag.nl/kaarten.html](https://botty.ramonmoorlag.nl/kaarten.html)**

Cards covering the levels of automation (from manual to fully autonomous) and the emotional states Botty can be in.

### 🌐 The Hive — Singularity
Visit **[hive.ramonmoorlag.nl](https://hive.ramonmoorlag.nl)**

Your Botty is part of a larger ecosystem. The Hive connects all Bottys in the Botty-verse.

### 📟 Badger2040 (offline hardware)
Download `badger2040/botty.py` and copy it to the `examples/` folder on your [Pimoroni Badger2040](https://shop.pimoroni.com/products/badger-2040).

- Runs fully offline on MicroPython + BadgerOS
- 296×128 e-ink display, 5 buttons
- Buttons: **A** = feed data · **B** = exercise · **C** = solve dilemma / heal · **UP** = stats · **DOWN** = back
- State is saved between sessions (Botty remembers her stats)

---

## Intent

Botty was designed **gimmick** for AI literacy education. And the application was vibe coded and should not be taken very seriously. The core pedagogical ideas:

- **AI needs care** — just like living things, AI systems require ongoing input (data), maintenance (training/fitness), and ethical oversight (dilemma resolution)
- **Growth takes time** — Botty evolves through life stages, mirroring how real AI systems mature from narrow prototypes to capable systems
- **Ethics are gameplay** — dilemmas aren't just flavour; they're a primary mechanic, putting ethical decision-making at the centre of the experience
- **Accessible across devices** — from a browser on any phone or laptop to a physical e-ink badge, Botty meets students where they are

---

## Part of NOLAI

This is not directly connected to NOLAI, it's products or it's views. It was developed in my spare time. 

---

*Made with care by Ramon Moorlag / NOLAI*
