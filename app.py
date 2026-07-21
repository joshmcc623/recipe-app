from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route('/')
def home():
    return "Recipe app is alive!"


if __name__ == "__main__":
    app.run(debug=True)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    prep_time = db.Column(db.Integer)  # Minutes
    cook_time = db.Column(db.Integer)  # Minutes
    servings = db.Column(db.Integer)
    instructions = db.Column(db.Text)  # store steps as one text block for now
    is_baking = db.Column(db.boolean, default=False)  # cooking vs baking

    def __repr__(self):
        return f"<Recipe {self.title}>"


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Sting(100), nullable=False)  # e.g. "2", "1.5"
    quantity = db.Column(db.String(20))              # e.g. "cups", "tbsp", "g"

    recipe_id = db.Column(db.Integer, db.ForeignKey(
        "recipe.id"), nullable=False)
    recipe = db.relationship(
        "Recipe", backref=db.backref("ingerdients", lazy=True))
