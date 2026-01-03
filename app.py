# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_migrate import Migrate




app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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
    description = db.Column(db.String(20), nullable=False)

    heropower = db.relationship('HeroPower', back_populates='power')

    serialize_rules = ('-heropower.power',)#this ensures we don't get recursions so it stops at power

    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("description must be at least 20 characters long")
        return description

    def __repr__(self):
        return f'<Power {self.name} for Hero ID {self.hero_id}>'


