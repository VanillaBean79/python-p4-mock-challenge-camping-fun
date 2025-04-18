from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey, String, Integer, Column
from sqlalchemy.orm import validates, relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    
    # Add relationship
    campers = db.relationship(
        'Camper', 
        secondary='signups', 
        back_populates='activities',
        
        )
    # Add serialization rules
    serialize_rules = ('-signups', '-campers.signups')


    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    

    signups = db.relationship('Signup', backref='camper', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age
        }
    # Add relationships
    activities = db.relationship(
        'Activity', 
        secondary='signups',
          back_populates='campers')
    # Add serialization rules
    serialize_rules = ('-signups', '-activities.signups')
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Camper must have a name.')
        return name
    
    @validates('age')
    def validate_age(self, key, age):
        if age < 8 or age > 18:
            raise ValueError('Age cannot be younger than 8 or older than 18.')
        return age


    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)

    #Foreign Keys to connecct camper and activity
    camper_id = db.Column(db.Integer, ForeignKey('campers.id', ondelete='CASCADE'), nullable=False)
    activity_id = db.Column(db.Integer, ForeignKey('activities.id', ondelete='CASCADE'), nullable=False)

    # Add relationships
    
    activity = db.relationship('Activity', backref=backref('signups', cascade="all, delete-orphan"))
    # Add serialization rules
    serialize_rules = ('camper.signups', '-activity.signups')
    # Add validation
    @validates('time')
    def validate_time(self, key, time):
        if time < 0 or time > 23:
            raise ValueError('Scheduled time for activity must be within the 24 hours of a day.')
        return time
    

    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.
