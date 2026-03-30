# ui.py
import tkinter as tk
from tkinter import scrolledtext   
from datetime import datetime       
from model import predict_intent, get_response
from load import all_intents, COMMANDS, get_commands



BG_DARK      = "#0d0f14"
BG_PANEL     = "#13161e"
BG_INPUT     = "#1a1e2a"
ACCENT       = "#5b8cff"
ACCENT_GLOW  = "#3a5fc8"
USER_BG      = "#1e2d5a"
BOT_BG       = "#1a1e2a"
TEXT_MAIN    = "#e8ecf5"
TEXT_MUTED   = "#6b7494"
BORDER       = "#232840"
SUCCESS      = "#4ecdc4"
FONT_MAIN    = ("Consolas", 11)
FONT_TITLE   = ("Consolas", 14, "bold")
FONT_SMALL   = ("Consolas", 9)


class ChatbotApp(tk.Tk):
    def __init__(self, model, vocab, intent_names, intents):
        super().__init__()
        self.model = model
        self.vocab = vocab
        self.intent_names = intent_names
        self.intents = intents

        self.title("PyBot — Assistant IA")
        self.geometry("720x620")
        self.minsize(500, 450)
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        self._build_ui()
        self._welcome()

    # GUI

    def _build_ui(self):
        # header
        header = tk.Frame(self, bg=BG_PANEL, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        indicator = tk.Canvas(header, width=10, height=10, bg=BG_PANEL, highlightthickness=0)
        indicator.pack(side="left", padx=(20, 8), pady=24)
        indicator.create_oval(1, 1, 9, 9, fill=SUCCESS, outline="")

        tk.Label(
            header, text="PyBot", font=FONT_TITLE,
            fg=TEXT_MAIN, bg=BG_PANEL
        ).pack(side="left")

        tk.Label(
            header, text="● IA locale · PyTorch",
            font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_PANEL
        ).pack(side="left", padx=10)

        btn_clear = tk.Button(
            header, text="Effacer", font=FONT_SMALL,
            fg=TEXT_MUTED, bg=BG_PANEL, bd=0, cursor="hand2",
            activeforeground=ACCENT, activebackground=BG_PANEL,
            command=self._clear_chat
        )
        btn_clear.pack(side="right", padx=20)

        # Chat
        chat_frame = tk.Frame(self, bg=BG_DARK)
        chat_frame.pack(fill="both", expand=True, padx=12, pady=(8, 0))

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            state="disabled",
            bg=BG_DARK,
            fg=TEXT_MAIN,
            font=FONT_MAIN,
            bd=0,
            padx=10,
            pady=10,
            wrap="word",
            cursor="arrow",
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
        )
        self.chat_display.pack(fill="both", expand=True)

        # Tags de style
        self.chat_display.tag_config("user_label", foreground=ACCENT, font=("Consolas", 9, "bold"))
        self.chat_display.tag_config("user_msg",   foreground=TEXT_MAIN,  font=FONT_MAIN)
        self.chat_display.tag_config("bot_label",  foreground=SUCCESS,    font=("Consolas", 9, "bold"))
        self.chat_display.tag_config("bot_msg",    foreground=TEXT_MAIN,  font=FONT_MAIN)
        self.chat_display.tag_config("muted",      foreground=TEXT_MUTED, font=FONT_SMALL)
        self.chat_display.tag_config("separator",  foreground=BORDER)

        # INPUT
        input_frame = tk.Frame(self, bg=BG_INPUT, highlightthickness=1, highlightbackground=BORDER)
        input_frame.pack(fill="x", padx=12, pady=12)

        self.entry = tk.Entry(
            input_frame,
            font=FONT_MAIN,
            bg=BG_INPUT,
            fg=TEXT_MAIN,
            insertbackground=ACCENT,
            bd=0,
            relief="flat",
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=14, pady=12)
        self.entry.bind("<Return>", self._on_send)
        self.entry.bind("<FocusIn>",  lambda e: input_frame.config(highlightbackground=ACCENT))
        self.entry.bind("<FocusOut>", lambda e: input_frame.config(highlightbackground=BORDER))
        self.entry.focus()

        send_btn = tk.Button(
            input_frame,
            text="Envoyer ↵",
            font=FONT_SMALL,
            fg=BG_DARK,
            bg=ACCENT,
            activebackground=ACCENT_GLOW,
            activeforeground=TEXT_MAIN,
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            relief="flat",
            command=self._on_send,
        )
        send_btn.pack(side="right", padx=(0, 8), pady=6)

        # Status
        self.status_var = tk.StringVar(value="Prêt")
        status_bar = tk.Label(
            self, textvariable=self.status_var,
            font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_DARK, anchor="w"
        )
        status_bar.pack(fill="x", padx=16, pady=(0, 6))

    # LOGIQUE DU CHATBOT

    def _welcome(self):
        # Message de bienvenue avec l'heure de démarrage du programme
        now = datetime.now().strftime("%H:%M")
        self._append("", "", "muted")
        self._append(
            "  PyBot v1.0  ",
            f"  Démarré à {now} — modèle PyTorch chargé\n",
            "muted"
        )
        # premier message du bot
        self._bot_message("Bonjour ! Je suis PyBot, un chatbot expérimental basé sur PyTorch. " \
        "\nFaites la commande /aide pour voir ce que je peux faire !")

    def _on_send(self, event=None):
        # envoyer le message de l'utilisateur
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self._user_message(text)
        self.after(300, lambda: self._respond(text))

    def is_command(self,text: str) -> bool:
        text = text.strip()
        # doit commencer par /
        if not text.startswith("/"):
            return False
        return text in COMMANDS

    def _respond(self, text: str):
        # réponse du bot
        if self.is_command(text):
            response = get_commands(text)
            self._bot_message(response)
            self.status_var.set(f"Commande reconnue : {text}")
            return
        else : 
            self.status_var.set("Réflexion en cours…")
            self.update_idletasks()

            intent, confidence = predict_intent(self.model, text, self.vocab, self.intent_names)
            response = get_response(intent, self.intents)

            self._bot_message(response)
            self.status_var.set(f"Intent: {intent}  |  Confiance: {confidence:.0%}")

    def _user_message(self, text: str):
        # traiter msg utilisateur
        now = datetime.now().strftime("%H:%M")
        self._append(f"\n  Vous  ", f"[{now}]\n", "user_label", "muted")
        self._append(f"  {text}\n", "", "user_msg")

    def _bot_message(self, text: str):
        # traiter msg bot
        now = datetime.now().strftime("%H:%M")
        self._append(f"\n  PyBot  ", f"[{now}]\n", "bot_label", "muted")
        self._append(f"  {text}\n", "", "bot_msg")
        self.chat_display.see("end")

    def _append(self, part1: str, part2: str = "", tag1: str = "bot_msg", tag2: str = "muted"):
        # afficher le texte
        self.chat_display.config(state="normal")
        if part1:
            self.chat_display.insert("end", part1, tag1)
        if part2:
            self.chat_display.insert("end", part2, tag2)
        self.chat_display.config(state="disabled")
        self.chat_display.see("end")

    def _clear_chat(self):
        # nettoyer chat
        self.chat_display.config(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.config(state="disabled")
        self._welcome()
        self.status_var.set("Conversation effacée")