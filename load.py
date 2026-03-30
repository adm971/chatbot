import json
from collections import defaultdict
from datasets import load_dataset


# CHARGER INTENTS
def load_intents(filepath="data.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
    
# CHARGER COMMANDES 
def load_commands(filepath="commands.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# Recupérer les patterns et les réponses
def get_patterns_and_responses(intents):
    patterns = []
    responses = []
    for intent, data in intents.items():
        patterns.extend(data["patterns"])
        responses.extend(data["responses"])
    return patterns, responses

# Recupérer les patterns des intents
def get_intents_patterns(intents):
    patterns = []
    for intent, data in intents.items():
        patterns.extend(data["patterns"])
    return patterns



# CHARGER MASSIVE
def load_massive(filepath="fr.jsonl"):
    data = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    return data



# CONVERTIR MASSIVE EN INTENTS
def massive_to_intents(dataset):
    intents = defaultdict(lambda: {"patterns": [], "responses": []})

    for item in dataset:
        intent = item["intent"]   
        text = item["utt"]        

        intents[intent]["patterns"].append(text)

    # réponses par défaut
    for intent in intents:
        intents[intent]["responses"] = [f"[{intent}] → réponse non définie"]

    return dict(intents)

dataset = load_dataset("json", data_files="fr.jsonl")
train_data = dataset["train"]




# -----------------------------CHARGER LES DONNÉES------------------------------ 
# INTENTS = massive_to_intents(train_data)
# INTENTS = load_massive()
INTENTS = load_intents()
COMMANDS = load_commands()
PATTERNS, RESPONSES = get_patterns_and_responses(INTENTS)

salut_intents = INTENTS["salutation"]["patterns"]
aurevoir_intents = INTENTS["aurevoir"]["patterns"]
merci_intents = INTENTS["merci"]["patterns"]
nom_intents = INTENTS["nom"]["patterns"]
humeur_intents = INTENTS["humeur"]["patterns"]
heure_intents = INTENTS["heure"]["patterns"]
blague_intents = INTENTS["blague"]["patterns"]
aide = "Voici les commandes disponibles :\n" + "\n".join(COMMANDS)

all_intents = [salut_intents, aurevoir_intents, merci_intents, nom_intents, humeur_intents, heure_intents, blague_intents, aide]

def get_commands(user_input):
    if user_input in COMMANDS:
        index = COMMANDS.index(user_input)  # faire correspondre user_input à une commande avec recherche par index dans COMMANDS
        return f"Voici une liste de mots dont je peux détecter les intentions et auxquels je peux répondre : {all_intents[index]}"


print(get_commands("/salut"))