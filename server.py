from app import app 

from app.controllers.users import users
from app.controllers.recetas import recetas

app.register_blueprint(users)
app.register_blueprint(recetas)


if __name__ == "__main__":
    app.run(debug=True)