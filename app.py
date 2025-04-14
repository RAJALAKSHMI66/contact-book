from flask import Flask, render_template_string, request, redirect
import json, os

app = Flask(__name__)

DB_FILE = "contacts.json"

# Load contacts from JSON file
def load_contacts():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as file:
        return json.load(file)

# Save contacts to JSON file
def save_contacts(contacts):
    with open(DB_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

@app.route("/")
def index():
    contacts = load_contacts()
    with open("index.html", "r") as f:
        html = f.read()
    return render_template_string(html, contacts=contacts)

@app.route("/add", methods=["POST"])
def add_contact():
    name = request.form["name"]
    phone = request.form["phone"]
    if name and phone:
        contacts = load_contacts()
        contacts.append({"name": name, "phone": phone})
        save_contacts(contacts)
    return redirect("/")

@app.route("/delete/<name>")
def delete_contact(name):
    contacts = load_contacts()
    contacts = [contact for contact in contacts if contact["name"] != name]
    save_contacts(contacts)
    return redirect("/")

@app.route("/style.css")
def serve_css():
    with open("style.css", "r") as f:
        return f.read(), 200, {'Content-Type': 'text/css'}

if __name__ == "__main__":
    app.run(debug=True)
