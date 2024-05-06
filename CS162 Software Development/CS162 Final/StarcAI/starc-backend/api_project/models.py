from datetime import datetime, timedelta
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# Create user with username, password, email connected to all their docs
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    documents = db.relationship('Document', backref='user', lazy=True, cascade="all, delete-orphan")

    # Set and check for password using Werkzeug functions.
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Store revoked tokens for logout functionality.
class RevokedTokenModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), unique=True)
    revoked_on = db.Column(db.DateTime, default=datetime.utcnow)

    def add(self):
        cleanup_revoked_tokens()
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)

# Remove used tokens.
def cleanup_revoked_tokens():
    expiration_days = 1
    threshold_date = datetime.utcnow() - timedelta(days=expiration_days)
    RevokedTokenModel.query.filter(RevokedTokenModel.revoked_on < threshold_date).delete()
    db.session.commit()

# Store basic document details.
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    word_count = db.Column(db.Integer, default=0, nullable=False)
    text_chunks = db.relationship('TextChunks', backref='document', lazy=True, cascade="all, delete-orphan")

# Store a complete piece of text associated with each doc. By segregating docs and its text, we can allow for rewrite and scoring process for a subsection of an entire docs text is an extension feature than rewriting the entire doc.
class TextChunks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_text_chunk = db.Column(db.Text, nullable=False)
    rewritten_text = db.Column(db.Text, nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    sentences = db.relationship('Sentence', backref='text_chunk', lazy=True, cascade="all, delete-orphan")
    initial_score = db.relationship('InitialScore', backref='text_chunk', uselist=False, cascade="all, delete-orphan")
    final_score = db.relationship('FinalScore', backref='text_chunk', uselist=False, cascade="all, delete-orphan")

# Store original and rewritten texts chained in order.
class Sentence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.Text, nullable=False)
    rewritten_text = db.Column(db.Text, nullable=False)
    text_chunk_id = db.Column(db.Integer, db.ForeignKey('text_chunks.id'), nullable=False)
    preceding_sentence_id = db.Column(db.Integer, db.ForeignKey('sentence.id'))

# Store scores for original text.
class InitialScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float, nullable=False)
    optimism = db.Column(db.Float, nullable=False)
    forecast = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    text_chunk_id = db.Column(db.Integer, db.ForeignKey('text_chunks.id'), nullable=False)

# Store scores for rewritten text.
class FinalScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float, nullable=False)
    optimism = db.Column(db.Float, nullable=False)
    forecast = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    text_chunk_id = db.Column(db.Integer, db.ForeignKey('text_chunks.id'), nullable=False)
