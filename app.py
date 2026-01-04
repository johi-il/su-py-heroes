# app.py
from flask import Flask,jsonify,make_response,request
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_migrate import Migrate




app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///powers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)




class Hero(db.Model, SerializerMixin):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    super_name = db.Column(db.String(),unique=True, nullable=False)

    heropower = db.relationship('HeroPower', back_populates='hero')
    
    serialize_rules = ('-heropower.hero',)

    def __repr__(self):
        return f'<{self.name}>'
    
class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'heropower'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(20), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
   
    hero = db.relationship('Hero', back_populates='heropower')
    power = db.relationship('Power', back_populates='heropower')

    serialize_rules = ('-hero.heropower', '-power.heropower',)

    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("strength must be one of 'Strong', 'Weak', or 'Average'")
        return strength

    def __repr__(self):
        return f'<Heropower : {self.strength} for Hero ID {self.hero_id}>'
    

class Power(db.Model, SerializerMixin):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)

    heropower = db.relationship('HeroPower', back_populates='power')

    serialize_rules = ('-heropower',)#this ensures we don't get recursions so we don't get infinite loops when serializing

    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("description must be at least 20 characters long")
        return description

    def __repr__(self):
        return f'<Power {self.name} for Hero ID {self.hero_id}>'


@app.route('/')
def index():
    return "Welcome to the Superhero API!"

@app.route('/heroes')
def heroes():
    
    heroes=[]
    for hero in Hero.query.all():
        hero_dict={
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name
        }
        heroes.append(hero_dict)

    response = make_response(
        jsonify(heroes),
        200
    )
    return response
        

@app.route('/heroes/<int:id>')
def hero_id(id):
    hero = Hero.query.get(id)
    if not hero:
        response = make_response(
            jsonify({"error": "Hero not found"}),
            404
        )
        return response

    hero_info = hero.to_dict()
    response = make_response(
        jsonify(hero_info),
        200
    )
    return response


@app.route('/powers')
def powers():
    powers=[]
    for power in Power.query.all():
        power_dict={
            "description": power.description,
            "id": power.id,
            "name": power.name
        }
        powers.append(power_dict)

    response = make_response(
        jsonify(powers),
        200
    )
    return response

@app.route('/powers/<int:id>', methods=['PATCH'])
def power_by_id(id):
    power = Power.query.get(id)
    
    if not power:
        return jsonify({"errors": ["Power not found"]}), 404

    # Get data for Postman/API tests)
    data = request.get_json()
    
    # 3. Update attributes safely
    try:
        for attr, value in data.items():
            setattr(power, attr, value)
            
        db.session.commit()
        
        # 4. Return successful response
        return jsonify(power.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400


@app.route('/powers/<int:id>')
def power_id(id):
    power = Power.query.get(id)
    if not power:
        response = make_response(
            jsonify({"error": "Power not found"}),
            404
        )
        return response

    power_info = power.to_dict()
    response = make_response(
        jsonify(power_info),
        200
    )
    return response


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    # Validation
    hero = Hero.query.get(data.get('hero_id'))
    power = Power.query.get(data.get('power_id'))
    
    if not hero or not power:
        return jsonify({"errors": ["validation errors"]}), 400

    try:
        new_heropower = HeroPower(
            strength=data.get('strength'),
            hero_id=data.get('hero_id'),
            power_id=data.get('power_id')
        )
        db.session.add(new_heropower)
        db.session.commit()

        return jsonify(new_heropower.to_dict()), 201
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5555)
