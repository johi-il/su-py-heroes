# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy_serializer import SerializerMixin




app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)




class Hero(db.Model, SerializerMixin):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    super_name = db.Column(db.String(),unique=True, nullable=False)

    serialize_rules = ('-heropower.hero',)

    def __repr__(self):
        return f'<Hero {self.name}>'
    
class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'heropower'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(20), CheckConstraint("strength IN ('weak', 'strong', 'average')"), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)

    serialize_rules = ('-hero.heropower', '-power.heropower',)


    def __repr__(self):
        return f'<Heropower {self.strength} of Hero ID {self.hero_id}>'
    

    class Power(db.Model, SerializerMixin):
        __tablename__ = 'power'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(), nullable=False)
        description = db.Column(db.String(20), nullable=False)


        serialize_rules = ('-heropower.power',)#this ensures we don't get recursions so it stops at power

        def __repr__(self):
            return f'<Power {self.name} of Hero ID {self.hero_id}>'
    

