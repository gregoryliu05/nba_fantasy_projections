#database models 
from config import db # imports the database from config.py


class Player(db.Model): 
    player = db.Column(db.String(80), primary_key = True, nullable = False)
    position = db.Column(db.String(20), unique = False, nullable = False)
    average_fpts = db.Column(db.Integer)
    projected_fpts = db.Column(db.Integer)
    consistency = db.Column(db.Integer)
    injury_risk = db.Column(db.Integer)
    consistency_injury_risk = db.Column(db.Integer)
    overall_score = db.Column(db.Integer)

    def to_json(self):
        return {
            "player": self.player,
            "position": self.position,
            "averageFPTS": self.average_fpts,
            "projectedFPTS": self.projected_fpts,
            "consistency": self.consistency,
            "injuryRisk": self.injury_risk,
            "consistencyInjuryRisk": self.consistency_injury_risk,
            "overallScore": self.overall_score
        }
