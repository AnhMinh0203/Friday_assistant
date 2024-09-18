import map
import spacy
import neuralcoref

nlp = spacy.load("en_core_web_lg")

# # Add the neuralcoref component to the spaCy pipeline
neuralcoref.add_to_pipe(nlp)

# Define Wh-word labels
wh_labels = {
    "who": "person",
    "what": "thing",
    "where": "place",
    "when": "time",
    "why": "reason",
    "how": "method"
}
#  Quân
def analyze_question(question):
    doc = nlp(question)

    object_in_question = None
    attribute_in_question = None
    action_in_question = None
    wh_label = None

    # Identify WH-words
    for token in doc:
        if token.text.lower() in wh_labels:
            wh_label = wh_labels[token.text.lower()]

    # Check for 'to be' verbs (am, is, are, was, were)
    to_be_verbs = {"am", "is", "are", "was", "were"}
    has_to_be_verb = any(token.lemma_ in to_be_verbs for token in doc)

    # Identify the object (typically noun or noun phrase)
    for ent in doc.ents:
        if ent.text.lower() in doc.text.lower():
            object_in_question = ent.text

    if not object_in_question:
        for chunk in doc.noun_chunks:
            if chunk.root.dep_ in ("nsubj", "dobj", "pobj"):  # Subject or object of the sentence
                object_in_question = chunk.text

    # Determine if there is a main verb or attribute based on the type of question
    if has_to_be_verb:
        for token in doc:
            if token.dep_ in ("attr", "amod"):
                attribute_in_question = token.text
                break
            if token.dep_ == "nsubj":
                attribute_in_question = token.text
                break
    else:
        action_verbs = {"do", "does", "did"}
        if any(token.text.lower() in action_verbs for token in doc):
            for token in doc:
                if token.pos_ == "VERB":
                    action_in_question = token.text
                    break
        else:
            for token in doc:
                if token.pos_ == "VERB":
                    action_in_question = token.text
                    break
                if token.pos_ == "ADJ" or token.pos_ == "NOUN":
                    attribute_in_question = token.text
                    break

    return {
        'Object': object_in_question,
        'Attribute': attribute_in_question,
        'Action': action_in_question,
        'WH Label': wh_label
    }

# Minh
def process_text(text):
    doc = nlp(text)
    return {
        'Sentences': [sent.text for sent in doc.sents],
        'Tokens': [token.text for token in doc],
        'POS Tags': [(token.text, token.pos_) for token in doc],
        'Lemmas': [(token.text, token.lemma_) for token in doc],
        'Stop Words': [(token.text, token.is_stop) for token in doc],
        'Dependencies': [(token.text, token.dep_, token.head.text) for token in doc],
        'Noun Phrases': [chunk.text for chunk in doc.noun_chunks],
        'Named Entities': [(ent.text, ent.label_) for ent in doc.ents],
        'Coreferences': [(coref.mentions[0], [mention.text for mention in coref.mentions]) for coref in doc._.coref_clusters]
    }
# Hiếu
def find_answer(question, text):
    question_info = analyze_question(question)
    object_in_question = question_info['Object']
    attribute_in_question = question_info['Attribute']
    action_in_question = question_info['Action']
    wh_label = question_info['WH Label']

    text_info = process_text(text)
    sentences = text_info['Sentences']
    entities = text_info['Named Entities']

    # Tìm câu trả lời dựa trên WH-words
    if wh_label:
        if wh_label == 'place':
            for sentence in sentences:
                if any(ent[1] == 'GPE' for ent in text_info['Named Entities']):
                    if any(ent[0].lower() in sentence.lower() for ent in text_info['Named Entities']):
                        return sentence
            # Nếu không tìm thấy thông tin về địa điểm, có thể cần thêm xử lý.
        elif wh_label == 'time':
            for sentence in sentences:
                if any(ent[1] == 'DATE' for ent in text_info['Named Entities']):
                    if any(ent[0].lower() in sentence.lower() for ent in text_info['Named Entities']):
                        return sentence
        elif wh_label == 'person':
            for sentence in sentences:
                if any(ent[1] == 'PERSON' for ent in text_info['Named Entities']):
                    if any(ent[0].lower() in sentence.lower() for ent in text_info['Named Entities']):
                        return sentence
        elif wh_label == 'reason':
            for sentence in sentences:
                if 'why' in sentence.lower():
                    return sentence
        elif wh_label == 'method':
            for sentence in sentences:
                if 'how' in sentence.lower():
                    return sentence
        elif wh_label == 'thing':
            for sentence in sentences:
                if object_in_question and object_in_question.lower() in sentence.lower():
                    return sentence
    return "No answer found"

def print_question_analysis(question_info):
    print("Question Analysis:")
    for key, value in question_info.items():
        print(f"{key}: {value}")
def print_text_info(text_info):
    print("Text Information:")
    print("Sentences:")
    for sentence in text_info['Sentences']:
        print(f" - {sentence}")

    print("Tokens:")
    for token in text_info['Tokens']:
        print(f" - {token}")

    print("POS Tags:")
    for tag in text_info['POS Tags']:
        print(f" - {tag[0]}: {tag[1]}")

    print("Lemmas:")
    for lemma in text_info['Lemmas']:
        print(f" - {lemma[0]}: {lemma[1]}")

    print("Stop Words:")
    for stop_word in text_info['Stop Words']:
        print(f" - {stop_word[0]}: {'Stop Word' if stop_word[1] else 'Not Stop Word'}")

    print("Dependencies:")
    for dep in text_info['Dependencies']:
        print(f" - {dep[0]}: {dep[1]} (Head: {dep[2]})")

    print("Noun Phrases:")
    for phrase in text_info['Noun Phrases']:
        print(f" - {phrase}")

    print("Named Entities:")
    for ent in text_info['Named Entities']:
        print(f" - {ent[0]}: {ent[1]}")

    print("Coreferences:")
    for coref in text_info['Coreferences']:
        print(f" - {coref[0]}: {', '.join(coref[1])}")
# Ví dụ sử dụng

text = "Billy was born in 2000. He is very handsome. He lives in Japan. "
question = "When was Billy born ?"
def response(question,text):
    question_info = analyze_question(question)
    print_question_analysis(question_info)
    text_infor = process_text(text)
    print_text_info(text_infor)
    map.answer_question(question, text)

#
# print("Bert:")
# response(question,text)
# print("Minh:")
# find_answer(question,text)