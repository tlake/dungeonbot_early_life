
class RollModel(db.model):
    id = db.Column(db.Integer, primary_key=True)
    string_id = db.Column(db.String(256))
