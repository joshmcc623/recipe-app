from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


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

    recipe_id = db.Column(db.Integer, db.ForeignKey(
        "recipe.id"), nullable=False)
    recipe = db.relationship(
        "Recipe", backref=db.backref("ingredients", lazy=True))


@app.route('/')
def home():
    return "Recipe app is alive!"


@app.route('/recipes', strict_slashes=False)
def list_recipes():
    recipes = Recipe.query.all()
    return render_template("recipes.html", recipes=recipes)


@app.route("/recipes/<int:recipe_id>", strict_slashes=False)
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template("recipe_detail.html", recipe=recipe)


@app.route("/recipes/new", methods=["GET", "POST"], strict_slashes=False)
def new_recipe():
    if request.method == "POST":
        recipe = Recipe(
            title=request.form["title"],
            description=request.form["description"],
            prep_time=request.form["prep_time"],
            cook_time=request.form["cook_time"],
            servings=request.form["servings"],
            instructions=request.form["instructions"],
            is_baking="is_baking" in request.form
        )
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for("view_recipe", recipe_id=recipe.id))

    return render_template("new_recipe.html")


if __name__ == "__main__":
    app.run(debug=True)
