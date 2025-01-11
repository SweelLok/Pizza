from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from db_connection import get_pizza, create, update, delete, get_all_pizzas


app = Flask(__name__)
api = Api(app)
CORS(app)


class Pizza(Resource):
	def get(self, id=0):
		if id == 0:
			pizzas = get_all_pizzas()
			pizzas_json = []
			for pizza in pizzas:
				pizzas_json.append(raw_to_json(pizza))
			return pizzas_json
		pizza = get_pizza(id)
		if pizza:
			pizza_json = raw_to_json(pizza)
			return pizza_json
		
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("name")
		parser.add_argument("ingredients")
		parser.add_argument("price")
		params = parser.parse_args()
		answer = create(params["name"], params["ingredients"], params["price"])
		json_data = jsonify(f"Records create with id {answer}")
		json_data.status_code = 201
		return json_data
	
	def put(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument("name")
		parser.add_argument("ingredients")
		parser.add_argument("price")
		params = parser.parse_args()
		update(id, params["name"], params["ingredients"], params["price"])
		json_data = jsonify(f"Records edit with id {id}")
		json_data.status_code = 202
		return json_data
	
	def delete(self, id):
		delete(id)
		json_data = jsonify(f"Records deleted with id {id}")
		json_data.status_code = 200
		return json_data


def raw_to_json(pizza):
	return {
		"id": pizza["id"], 
		"name": pizza["name"], 
		"ingredients": pizza["ingredients"], 
		"price": pizza["price"]
	}


SWAGGER_URL="/swagger"
API_URL="/static/swagger.json"

	
swagger_ui_blueprint = get_swaggerui_blueprint(
   SWAGGER_URL,
   API_URL,
   config={
       'app_name': 'Pizza API'
   }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)



api.add_resource(Pizza, "/api/v1.0/pizza/", 
								 "/api/v1.0/pizza/<int:id>", 
								 "/api/v1.0/pizza/<int:id>/", 
								 "/api/v1.0/pizza")


if __name__ == "__main__":
	app.run(port=32000, debug=True)
