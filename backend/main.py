from flask import request, jsonify
from config import app, db
from models import *
from services.whole_scraping_process import final_process


@app.route("/players", methods = ["GET"])
def get_players():
    players = Player.query.all()
    json_players = list(map(lambda x: x.to_json(), players))
    return jsonify({"players": json_players})


@app.route("/add_player", methods = ["POST"])
def add_player():
    player = request.json.get("player")
    position = request.json.get("position")
    average_fpts = request.json.get("averageFPTS")
    projected_fpts = request.json.get("projectedFPTS")
    consistency = request.json.get("consistency")
    injury_risk = request.json.get("injuryRisk")
    consistency_injury_risk = request.json.get("consistencyInjuryRisk")
    overall_score = request.json.get("overallScore")

    if not player or not position or not average_fpts or not projected_fpts or not consistency or not injury_risk:
        return jsonify({"message": "You must include all fields"}), 400
    
    new_player = Player(player = player, position = position, average_fpts = average_fpts, projected_fpts =projected_fpts,
                        consistency = consistency, injury_risk = injury_risk, consistency_injury_risk = consistency_injury_risk, 
                        overall_score = overall_score)
    try:
        db.session.add(new_player)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    

    return jsonify({"message": "User created!"}), 201

@app.route("/update_data", methods = ["POST"])
def update_data():
    final_process()
    return jsonify({"message": "Player data successfully updated in the database."}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all() # spin up the database if it doesn't already exist


    app.run(debug=True)
