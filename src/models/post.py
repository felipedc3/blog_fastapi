import sqlalchemy
from src.database import metadata

posts = sqlalchemy.Table(
    'posts',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('title', sqlalchemy.String(150), nullable=False, unique=True),
    sqlalchemy.Column('content', sqlalchemy.String, nullable=False),
    sqlalchemy.Column('published_at', sqlalchemy.DateTime, nullable=True),
    sqlalchemy.Column('published', sqlalchemy.Boolean, default=False),
    
)