#
# Memento
# Backend
# IAM Models 
#

from ..app import db
from sqlalchemy.orm import validates
import re

# defines an organisation that users and teams belong to
class Organisation(db.Model):
    # model fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    logo_url = db.Column(db.String(2048), nullable=True)
    # relationships 
    teams = db.relationship("Team", backref=db.backref("organisation"), lazy=True)
    members = db.relationship("User", backref=db.backref("organisation"), lazy=True)
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise AssertionError('Organisation name must not be empty')
        elif len(name) < 2 or len(name) > 256:
            raise AssertionError(' must be between 2 and 256 characters long')
        else:
            return name
        

# defines a team in an organisation  that users can be belng too
class Team(db.Model):
    # model fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    # relationships 
    org_id = db.Column(db.Integer, db.ForeignKey("organisation.id"),
                       nullable=False)
    members = db.relationship("User", backref=db.backref("team"), lazy=True)



# defines a user in the organisation.
class User(db.Model):
    # user kinds/types
    class Kind:
        Worker = "worker" # worker
        Supervisor = "supervisor" # supervisor of worker
        Admin = "admin" # root adminstrative user for the organisation
        Service = "service" # service account

    # model fields
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    email = db.Column(db.String(512), unique=True, nullable=False)
    # relationships 
    org_id = db.Column(db.Integer, db.ForeignKey("organisation.id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)

    @validates('kind')
    def validate_kind(self, key, kind):
        kind_list = ['worker','supervisor','admin','service']
        if not kind:
            raise AssertionError ('kind must not be empty')
        elif len(kind) < 2 or len(kind) > 64:
            raise AssertionError ('must be between 2 and 64 characters long')
        elif kind not in kind_list:
            raise AssertionError ('Enter either worker, supervisor, admin or service')
        else:
            return kind


    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise AssertionError('Name must not be empty')
        elif len(name) < 2 or len(name) > 256:
            raise AssertionError(' must be between 2 and 256 characters long')
        else:
            return name

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('Email must not be empty')
        elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
            raise AssertionError('Ensure it is the correct email input')
        else:
            return email

    @validates('password')
    def validate_password(self, key, password):
        if not password:
            raise AssertionError('Password must not be empty')
        elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",password):
            raise AssertionError('minimum eight characters, at least one uppercase letter, one lowercase letter and one number')
        else:
         return password

# defines an assignment of management (supervisors) to workers and teams
class Management(db.Model):
    # management kinds/types
    class Kind:
        Worker = "worker" # manage only a single worker
        Team = "team" # worker

    # model fields
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(64), nullable=False)
    # relationships
    target_id = db.Column(db.Integer, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    manager = db.relationship("User", lazy=True)

    @validates('kind')
    def validate_kind(self, key, kind):
        if not kind:
            raise AssertionError ('kind must not be empty')
        elif len(kind) < 1 or len(kind) > 64:        
            raise AssertionError ('must be between 1 and 64 characters long')
        elif kind != "worker" or kind != "team":
            raise AssertionError ('Enter either worker or team')
        else:
            return kind



