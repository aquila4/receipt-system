from flask import Flask, redirect
from app import create_app

app = create_app()

# 👉 ADD THIS HERE
@app.route("/")
def home():
    return redirect("/receipt/")

if __name__ == "__main__":
    app.run(debug=True)