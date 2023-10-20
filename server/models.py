from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

from sqlalchemy import CheckConstraint,UniqueConstraint
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    __table_args__ = (
        CheckConstraint('length(phone_number) = 10', name='valid_phone_number'),
        UniqueConstraint('name', name='unique_author_name'),
    )

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Name is required.')
        return name
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and not phone_number.isdigit():
            raise ValueError('Phone number must contain only digits.')
        if phone_number and len(phone_number) != 10:
            raise ValueError('Phone number must be exactly ten digits long.')
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    __table_args__ = (
        CheckConstraint('length(content) >= 250', name='content_min_length'),
        CheckConstraint('length(summary) <= 250', name='summary_max_length'),
        CheckConstraint("category IN ('Fiction', 'Non-Fiction')", name = "valid_category"),
    )

    @validates("title")
    def validate_title(self,key,title):
        if not title:
            raise ValueError('Post must contain Title')
        return title
    @validates("title")
    def validate_title(self,key,title):
        if title not  in ["Won't Believe","Secret","Top [number]","Guess"]:
            raise ValueError('Title must be sufficiently clickbait-y')
        return title
    
    
    @validates('content')
    def validate_content(self, key, content):
        if not content or len(content) < 250:
            raise ValueError('Content must be at least 250 characters long.')
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) >= 250:
            raise ValueError('Summary must be at most 250 characters long.')
        return summary
    
    @validates('category')
    def validate_category(self,key,category):
        if category not in ["Fiction",'Non-Fiction']:
            raise ValueError('Must be either Fiction or Non Fiction')




    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
