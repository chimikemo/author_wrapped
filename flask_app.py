from flask import Flask, render_template, request, jsonify, send_from_directory, url_for, session, redirect, current_app
from backend.utils.retriever import find_items
from backend.utils.images import create_collage_for_author
from backend.utils.aura import create_authors_aura_image, create_authors_aura_image_new
from backend.utils.wrapped_image import create_wrapped_for_author
from backend.classes.Work import Work
import os
import random
import json
from collections import defaultdict, deque
import time
import csv

updates = defaultdict(list)

app = Flask(__name__)
app.secret_key = "chimikemo"

# setting up queue so it hopefully wont break on pythonanywhere
waiting_queue = deque()
MAX_ACTIVE_USERS = 5

@app.before_request
def limit_concurrent_users():
    user_id = session.get("user_id")
    if not user_id:
        user_id = str(time.time()) + str(len(waiting_queue))
        session["user_id"] = user_id

    if user_id not in waiting_queue:
        waiting_queue.append(user_id)

    if waiting_queue[0] != user_id:
        return render_template("waiting.html", position=list(waiting_queue).index(user_id)+1)


@app.after_request
def remove_user(response):
    user_id = session.get("user_id")
    if user_id and waiting_queue and waiting_queue[0] == user_id:
        waiting_queue.popleft()
    return response

def log(author, message):
    updates[author].append(message)

@app.route("/status/<author>")
def get_status(author):
    return jsonify(updates.get(author, []))

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quiz")
def quiz():
    with open ('backend/quiz/questions.csv', mode='r', encoding='utf-8') as file:
        questions = csv.DictReader(file)
        return render_template("quiz.html", questions=questions)

@app.route("/quiz-result", methods=['POST'])
def submit_form():
    with open ('backend/quiz/questions.csv', mode='r', encoding='utf-8') as file_q:
        with open ('backend/quiz/description.csv', mode='r', encoding='utf-8') as file_d:
            questions = csv.DictReader(file_q)
            descriptions = csv.DictReader(file_d)
            user_answers = request.form.get('user_answers')
            answers = request.form.to_dict()
            answers = request.form.to_dict()
            print(answers)
            return render_template("quiz_results.html", descriptions=descriptions, user_answers=user_answers)



@app.route("/backend/images/generated_images/<path:filename>")
def serve_generated_image(filename):
    base_dir = os.path.join(current_app.root_path, "backend", "images", "generated_images")
    return send_from_directory(base_dir, filename)

@app.route("/test", methods=["POST"])
def create_authors_images():
    print("------------------------- STARTING NEW RUN -------------------------")
    author_name = request.form.get("username", "").strip()

    updates[author_name] = []

    if not author_name:
        return jsonify({"error": "No username provided"}), 400

    log(author_name, f"looking for {author_name}'s Ao3 works...")

    log(author_name, "this might take a minute (or more), depending on how many works you have.")

    list_of_works = find_items(Work, "users", author_name, "works")
    shortened_author_name = author_name.split("/")[-1]

    if len(list_of_works) == 0:
        return jsonify({"error": f"Author {author_name} has no works"}), 404

    log(author_name, "filtering out works from 2025...")


    works_2025 = [l for l in list_of_works if "2025" in l.date]

    if works_2025:
        list_of_works = works_2025
        print("This author published in 2025 -- proceeding with only works frm this year")
    else:
        print("This author hasn't published in 2025 -- proceeding with historical wrapped")


    os.makedirs(f"backend/images/generated_images/{shortened_author_name}", exist_ok=True)

    colors = ["blue", "pink", "orange", "purple", "green", "red"]
    color = random.choice(colors)

    log(author_name, f"it has been (scientifically) determined that {author_name}'s color is {color}")

    geometric_bg = f"backend/images/geometric/{color}.png"
    gradient_bg = f"backend/images/gradients/{color}.jpg"

    json_tags = json.load(open("backend/maps/aura.json", "r"))

    log(author_name, f"using advanced math and science to generate {author_name}'s moodboard....")

    create_collage_for_author(
        list_of_works,
        json_tags,
        1024,
        f"backend/images/generated_images/{shortened_author_name}/collage.png",
        gradient_bg
    )

    log(author_name, "moodboard completed!")
    log(author_name, f"using astrology and calculus to determine {author_name}'s aura...")

    create_authors_aura_image_new(list_of_works, shortened_author_name, gradient_bg, geometric_bg)

    log(author_name, "aura completed!")
    log(author_name, f"for the grand finale, generate {author_name}'s wrapped!")

    create_wrapped_for_author(list_of_works, shortened_author_name, geometric_bg, gradient_bg)

    collage_url = url_for(
        "serve_generated_image",
        filename=f"{shortened_author_name}/collage.png"
    )
    aura_url = url_for(
        "serve_generated_image",
        filename=f"{shortened_author_name}/aura.png"
    )
    wrapped_url = url_for(
        "serve_generated_image",
        filename=f"{shortened_author_name}/wrapped.png"
    )

    return jsonify({"collage": collage_url,
                    "wrapped": wrapped_url,
                    "aura": aura_url,
                    "DEBUG": True})


if __name__ == "__main__":
    app.run(debug=True,
        use_reloader=False,
            host="0.0.0.0", port=5001, )
