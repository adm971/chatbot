
# V 1.0.0
# 05/06/2026
# commit 


from load import INTENTS

from modules import build_vocab

from model import ChatNet

from model import train_model

from gui import ChatbotApp

def main():
    print("build_vocab()…")
    vocab = build_vocab(INTENTS)
    print(f"   {len(vocab)} mots dans le vocabulaire")

    print("train_model()…")
    model, intent_names = train_model(INTENTS, vocab, epochs=600)
    print(f"   Modèle entraîné sur {len(intent_names)} intents")

    print("lancement du chatbot\n")
    app = ChatbotApp(model, vocab, intent_names, INTENTS)
    app.mainloop()


if __name__ == "__main__":
    main()
