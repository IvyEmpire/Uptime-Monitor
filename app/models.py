from app import db


class Incident (db.Model):
    id = db.Column ('Incident ID', db.Integer, primary_key = True)
    name = db.Column (db.String(80), index = True, unique = False, nullable = False)
    message = db.Column (db.String(128), index = True, unique = False, nullable = False)
    status = db.Column (db.Integer, index =True, unique = False, nullable = False)
    visiable = db.Column (db.Integer, index =True, unique = False, nullable = False)
    component_id = db.Column (db.Integer, index = True, unique = False, nullable = True)
    component_status = db.Column (db.Integer, index = True, unqiue = False, nullable = True)
    notify = db.Column (db.Boolean, index = True, unqiue = False, nullable = True )
    # created_at = db.Column (db.DateTime, index = True, unique = True, nullable = True)
    # template = db.Column (db.String(32), index =True, unique = False, nullable  =False)


    def __init__(self, id, name, message, status, visiable, component_id, component_status, notify):
        self.id = id
        self.name = name
        self.message = message
        self.status = status
        self.visiable = visiable
        self.component_id = component_id
        self.component_status = component_status
        self.notify =notify

