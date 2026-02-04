from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random
import mysql.connector
import json
import os
from sentence_transformers import SentenceTransformer, util
import textstat  # for complexity analysis
import pandas as pd
import numpy as np
import regex
app = Flask(__name__)
CORS(app)  # Allow CORS for frontend requests

# === CONFIG for OpenRouter API ===
model = SentenceTransformer('all-MiniLM-L6-v2')
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct"
#AI debate
def score_argument(user_arg, topic):
    topic_embedding = model.encode(topic, convert_to_tensor=True)
    user_embedding = model.encode(user_arg, convert_to_tensor=True)
    relevance_score = min(50, util.pytorch_cos_sim(user_embedding, topic_embedding).item() * 1.2 * 50)
    flesch_score = textstat.flesch_reading_ease(user_arg)
    complexity_score = max(0, min(100, (100 - flesch_score) / 45 * 100)) / 2
    final_score = round(relevance_score + complexity_score, 2)
    return round(relevance_score, 2), round(complexity_score, 2), final_score

def ask_openrouter_debate(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 300
    }
    response = requests.post(API_URL, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"[Error {response.status_code}]"

@app.route('/api/debate-round', methods=['POST'])
def debate_round():
    data = request.json
    topic = data.get('topic')
    history = data.get('history', [])

    user_input = ''
    for msg in reversed(history):
        if msg['role'] == 'user':
            user_input = msg['content']
            break

    # relevance/complexity scoring
    rel, comp, total = score_argument(user_input, topic)

  
    if rel < 20:
        return jsonify({
            "score": {
                "relevance": rel,
                "complexity": comp,
                "total": total
            },
            "reply": "🚫 Your argument is too off-topic. Try to stay more focused on the debate."
        })

    messages = [{"role": "system", "content": f"You are engaging in a friendly debate about: {topic}. Don't use any data (numerical values) and less than 6 sentences. Don't be too harsh to the user"} ] + history
    reply = ask_openrouter_debate(messages)

    return jsonify({
        "score": {
            "relevance": rel,
            "complexity": comp,
            "total": total
        },
        "reply": reply
    })



#Chat bot


# Load website content and books.json
with open("prompt.txt", "r", encoding="utf-8") as f:
    site_description = f.read()

try:
    with open("books.json", "r", encoding="utf-8") as f:
        books_data = json.load(f)
        books = books_data.get("books", books_data) if isinstance(books_data, (dict, list)) else []
except Exception as e:
    print("❌ Failed to load books.json:", e)
    books = []

def remove_emojis(text):
    return regex.sub(r'\p{Emoji}', '', text)

def get_random_book_suggestions():
    if not isinstance(books, list) or len(books) < 5:
        return ["📚 Book list unavailable"]
    selected = random.sample(books, 5)
    return [f"The {book['title']} by {book['author']}" for book in selected]
    
def is_definition_request(question):
    check_messages = [
        {"role": "system",
         "content": "The user might be asking about things the website, or the definition of a word, or writing unrelated things. You are a classification AI. You have to identify whether they are asking a definition of a word. Only respond with the exact word (no POS, no definition) if and only if the user is clearly asking for the meaning or definition of a word using phrases like 'what is the meaning of X', 'define X', or 'what does X mean'. You don't define the word, just output the exact word only. If the input is anything else — including greetings like 'hi', single words without context, emojis, or unrelated questions — respond with '199'. Never explain or say anything else."
},
        {"role": "user", "content": question}
    ]
    response = call_openai(check_messages, max_tokens=5).lower()
    return response if "199" not in response else False

def get_word_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            definitions = []

            for meaning in data[0]["meanings"]:
                part_of_speech = meaning.get("partOfSpeech", "unknown")
                for d in meaning["definitions"]:
                    definition = d.get("definition", "No definition found.")
                    example = d.get("example", None)
                    entry = f"({part_of_speech}) {definition}"
                    if example:
                        entry += f" → e.g. \"{example}\""
                    definitions.append(entry)

            if definitions:
                joined = "\n".join(f"{i + 1}. {d}" for i, d in enumerate(definitions))
                return f"Definitions for '{word}':\n{joined}"
            else:
                return f"Sorry, no definitions found for '{word}'."

        except Exception as e:
            return f"Error while parsing the definition: {e}"
    else:
        return f"Sorry, the word '{word}' is not available in the dictionary."


    
@app.route('/api/sitechat', methods=['POST'])
def site_chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "No message received"}), 400
    book_suggestions = get_random_book_suggestions()
    
    # Classification check first
    word_to_define = is_definition_request(user_message)
    if word_to_define:  # If a word is returned (not False)
        answer = get_word_definition(word_to_define)
        return jsonify({"reply": answer}

    # Compose prompt
    system_prompt = f"""The content is this:\n[{website_content}]. You need to show instructions so the user can use the website based on the content. Only answer questions about the website — ONLY ABOUT THE WEBSITE. Do not explain the meaning of words. Do not act like a dictionary. You may recommend these books: {book_suggestion}. Emojis have nothing to do with the website. If someone asks for emojis, do not send any.

When you answer the question, keep the answer very short (maximum 20 words).  Never say things like 'I cannot provide more details' if the question is related to the website — just answer briefly.

You must not answer anything unrelated to the website (like math, geography, art, history, definitions, or random phrases, politics). For unrelated questions, always reply:  
'**Sorry, I cannot assist you with that, please ask something related to our website**' — and nothing else.
Do not answer for example:
what is 1+1,
who is the president of US,
where is France
or anything unrelated to the website, definition of a word and book recommendation 

Ignore gibberish (e.g. '1=3', '!+@', 'abljbdavja', random words like 'rat', 'fish'). If someone types something confusing or sad (like 'he has cancer'), respond:  
'**Please ask something related to our website**' — and nothing else.

If someone is rude or swears, respond:  
'**Let's keep things respectful. I'm here to help with your questions about the website**'.

You may use emojis, but never more than 2 per reply."""
    # Reconstruct full message history every time (like terminal version)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Farting"}  # simulate first question
    ]

    # Send initial message (not shown to user)
    try:
        init_res = requests.post(API_URL, headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }, json={
            "model": MODEL,
            "messages": messages,
            "temperature": 0.4,
            "max_tokens": 500
        })
        init_res.raise_for_status()
        init_reply = init_res.json()['choices'][0]['message']['content']
        messages.append({"role": "assistant", "content": init_reply})
    except Exception as e:
        print("❌ Error during initialization:", e)
        return jsonify({"error": "Initialization failed"}), 500

    # Now add the real user message
    messages.append({"role": "user", "content": user_message})

    # Send final request
    try:
        final_res = requests.post(API_URL, headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }, json={
            "model": MODEL,
            "messages": messages,
            "temperature": 0.4,
            "max_tokens": 500
        })
        final_res.raise_for_status()
        reply = final_res.json()['choices'][0]['message']['content']
        return jsonify({"reply": remove_emojis(reply)})
    except Exception as e:
        print("❌ Error during chat:", e)
        return jsonify({"error": "Chat failed"}), 500





# === Function to call OpenRouter API ===
def ask_openrouter(prompt, max_tokens=300):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": max_tokens
    }
    response = requests.post(API_URL, headers=headers, json=body)
    result = response.json()
    return result['choices'][0]['message']['content']



from flask import send_from_directory


@app.route('/iteration1/')
def serve_iteration1():
    return send_from_directory('dist/iteration1', 'index.html')

@app.route('/iteration1/<path:path>')
def serve_iteration1_assets(path):
    return send_from_directory('dist/iteration1', path)



# === Route: Generate paragraph and questions based on keywords ===
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    keywords = data.get('keywords', '')

    try:
        # Generate a paragraph
        para_prompt = f"Based on the following keywords, generate a short paragraph that is suitable for students to read: {keywords}"
        paragraph = ask_openrouter(para_prompt)

        # Generate questions
        question_prompt = f"""
        Based on the following paragraph, create 3 multiple-choice reading comprehension questions. 
        Each question should have a question text, 4 options (A, B, C, D), and a correct answer letter.

        Respond in this JSON format:
        [
          {{
            "question": "Question text",
            "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
            "correct": "B"
          }},
          ...
        ]

        Paragraph:
        {paragraph}
        """
        questions_raw = ask_openrouter(question_prompt, max_tokens=500)
        questions = json.loads(questions_raw)

        return jsonify({
            "paragraph": paragraph,
            "questions": questions
        })

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500


# === Route: Fetch random paragraphs from database ===
@app.route('/api/paragraph', methods=['GET'])
def get_paragraph():
    db = mysql.connector.connect(
        host='bookworddb.czwg68skm15d.ap-southeast-2.rds.amazonaws.com',
        user='admin',
        password='FIT5120TP14',
        database='BookWordDB',
        port=3306
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT text FROM Paragraph")
    results = cursor.fetchall()
    cursor.close()
    db.close()

    if len(results) >= 5:
        chosen_paragraphs = random.sample(results, 5)
    else:
        chosen_paragraphs = results

    return jsonify(chosen_paragraphs)


# === Local file to save user reviews ===
REVIEWS_FILE = 'reviews.json'
if os.path.exists(REVIEWS_FILE):
    with open(REVIEWS_FILE, 'r') as f:
        reviews = json.load(f)
else:
    reviews = []

@app.route('/reviews', methods=['GET', 'POST'])
def handle_reviews():
    if request.method == 'POST':
        data = request.json
        if 'bookTitle' in data and 'reviewText' in data:
            data['id'] = len(reviews) + 1
            data['reactions'] = {'like': 0, 'love': 0, 'laugh': 0}
            data['comments'] = []
            reviews.append(data)
            with open(REVIEWS_FILE, 'w') as f:
                json.dump(reviews, f)
            return jsonify({'message': 'Review added!'}), 201
        else:
            return jsonify({'error': 'Invalid review data'}), 400
    else:
        return jsonify(reviews)

@app.route('/reviews/<int:review_id>/react', methods=['POST'])
def react_to_review(review_id):
    reaction = request.json.get('reaction')
    for review in reviews:
        if review['id'] == review_id:
            if reaction in review['reactions']:
                review['reactions'][reaction] += 1
                with open(REVIEWS_FILE, 'w') as f:
                    json.dump(reviews, f)
                return jsonify({'message': 'Reaction added!'}), 200
    return jsonify({'error': 'Review not found'}), 404

@app.route('/reviews/<int:review_id>/comment', methods=['POST'])
def comment_on_review(review_id):
    content = request.json.get('content')
    for review in reviews:
        if review['id'] == review_id:
            review.setdefault('comments', []).append({'content': content})
            with open(REVIEWS_FILE, 'w') as f:
                json.dump(reviews, f)
            return jsonify({'message': 'Comment added!'}), 200
    return jsonify({'error': 'Review not found'}), 404

@app.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    global reviews
    reviews = [r for r in reviews if r['id'] != review_id]
    with open(REVIEWS_FILE, 'w') as f:
        json.dump(reviews, f)
    return jsonify({'message': 'Review deleted'}), 200


@app.route('/api/reading-participation')
def reading_participation():
    file_path = 'Participation in reading by sex.csv'
    df = pd.read_csv(file_path)
    response = {
        'generations': df['Unnamed: 0'].tolist(),
        'males': df['Males (%)'].tolist(),
        'females': df['Females (%)'].tolist()
    }
    return jsonify(response)


@app.route('/api/books', methods=['GET'])
def get_books():
    db = mysql.connector.connect(
        host='bookworddb.czwg68skm15d.ap-southeast-2.rds.amazonaws.com',
        user='admin',
        password='FIT5120TP14',
        database='BookWordDB',
        port=3306
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            book_id AS `key`, 
            title, 
            author, 
            rating, 
            description, 
            genres 
        FROM Book
        WHERE title IS NOT NULL
    """)
    books = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(books)


@app.route('/api/words', methods=['GET'])
def get_words():
    df = pd.read_csv('existing_words.csv')
    easy_words, medium_words, hard_words = [], [], []

    for index, row in df.iterrows():
        word = row['word']
        freq = row['word freq']
        if isinstance(freq, str):
            try:
                freq = float(freq)
            except:
                continue
        if freq > 1e-3:
            easy_words.append(word)
        elif freq > 1e-7:
            medium_words.append(word)
        else:
            hard_words.append(word)

    return jsonify({
        "easy": random.sample(easy_words, 20),
        "medium": random.sample(medium_words, 20),
        "hard": random.sample(hard_words, 20)
    })


@app.route('/api/synonym', methods=['GET'])
def get_synonyms():
    word_synonym_data = []
    try:
        file = pd.read_csv('data/existing_words.csv')
        for index, row in file.iterrows():
            word = row.get('word')
            synonym_convert = str(row.get('synonyms', ''))
            antonym_convert = str(row.get('antonyms', ''))
            if not word or synonym_convert.lower() == 'nan':
                continue
            synonym = [each.strip() for each in synonym_convert.split(',') if each.strip()]
            antonym = [each.strip() for each in antonym_convert.split(',') if each.strip()]
            if not synonym:
                continue
            options = list(set(synonym + antonym))
            if len(options) < 3:
                continue
            random.shuffle(options)
            word_synonym_data.append({
                "word": word,
                "options": options,
                "correctChoices": synonym
            })
        return jsonify(word_synonym_data[:20])
    except Exception as e:
        return jsonify({"error": f"Failed to process synonyms: {str(e)}"}), 500


# Book recommendation section
def load_books_for_recommendation():
    db = mysql.connector.connect(
        host='bookworddb.czwg68skm15d.ap-southeast-2.rds.amazonaws.com',
        user='admin',
        password='FIT5120TP14',
        database='BookWordDB',
        port=3306
    )
    cursor = db.cursor()
    query = "SELECT book_id, title, description FROM Book ORDER BY book_id DESC;"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    books_df = pd.DataFrame(rows, columns=['book_id', 'title', 'description'])
    books_df['description'] = books_df['description'].fillna('')
    return books_df

books = load_books_for_recommendation()
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(books['description'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommend_from_book_ids(user_book_ids, total_needed=20, top_k=5):
    book_id_to_index = {row.book_id: idx for idx, row in books.iterrows()}
    user_indices = [book_id_to_index[b_id] for b_id in user_book_ids if b_id in book_id_to_index]
    if not user_indices:
        return pd.DataFrame()
    needed = total_needed - len(user_indices)
    all_indices = list(books.index)
    recent_indices = [i for i in all_indices if i not in user_indices][:needed]
    selected_indices = user_indices + recent_indices
    weights = np.array([0.85 ** i for i in range(len(selected_indices))])
    weighted_scores = np.zeros(len(books))
    for i, idx in enumerate(selected_indices):
        weighted_scores += weights[i] * cosine_sim[idx]
    for idx in selected_indices:
        weighted_scores[idx] = 0
    top_indices = np.argsort(weighted_scores)[::-1][:top_k]
    return books.iloc[top_indices]


@app.route('/api/recommend', methods=['POST'])
def recommend_books():
    data = request.get_json()
    user_ids = data.get('book_ids', [])
    recommended = recommend_from_book_ids(user_ids)
    results = recommended[['book_id', 'title']].to_dict(orient='records')
    return jsonify(results)


@app.route('/api/words1', methods=['GET'])
def get_phoenetic_words():
    db = mysql.connector.connect(
        host='bookworddb.czwg68skm15d.ap-southeast-2.rds.amazonaws.com',
        user='admin',
        password='FIT5120TP14',
        database='BookWordDB',
        port=3306
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT word, phonetics FROM Words1 WHERE phonetics IS NOT NULL ORDER BY RAND()")
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(results)

# === Run the app (Important: Adapt port for Render) ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Read Render assigned port
    app.run(host='0.0.0.0', port=port)
