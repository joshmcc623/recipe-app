from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    prep_time = db.Column(db.Integer)   # minutes
    cook_time = db.Column(db.Integer)   # minutes
    servings = db.Column(db.Integer)
    instructions = db.Column(db.Text)   # store steps as one text block for now
    is_baking = db.Column(db.Boolean, default=False)  # cooking vs baking

    def __repr__(self):
        return f"<Recipe {self.title}>"

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50))   # e.g. "2", "1.5"
    unit = db.Column(db.String(20))       # e.g. "cups", "tbsp", "g"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)
    recipe = db.relationship("Recipe", backref=db.backref("ingredients", lazy=True))


@app.route('/')
def home():
    return "Recipe app is alive!"


@app.route('/recipes')
def list_recipes():
    recipes = Recipe.query.all()
    return render_template("recipes.html", recipes=recipes)


if __name__ == "__main__":
    app.run(debug=True)
