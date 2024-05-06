from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

engine = create_engine('sqlite:///health_system.db')

Base = declarative_base()

class User(Base):
    """
    Representation of a user in the system. Holds the personal details and authentication information,
    along with relationships to various health and fitness records.
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    
    # Relationships to various records that belong to the user.
    workouts = relationship("Workout", back_populates="user")
    measurements = relationship("BodyMeasurement", back_populates="user")
    nutrition_logs = relationship("Nutrition", back_populates="user")
    sleep_records = relationship("Sleep", back_populates="user")
    health_metrics = relationship("HealthMetric", back_populates="user")
    mental_health_logs = relationship("MentalHealth", back_populates="user")
    health_recommendations = relationship("HealthRecommendation", back_populates="user")

    # Indexes for quick lookup on frequently searched fields
    __table_args__ = (
        Index('ix_users_username', 'username'),
        Index('ix_users_email', 'email'),
    )

class BodyMeasurement(Base):
    """
    Body measurements for users, such as height and weight at different points in time.
    """
    __tablename__ = 'body_measurements'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    height = Column(Float)
    weight = Column(Float)
    recorded_date = Column(DateTime, default=datetime.datetime.utcnow)

    # Index for efficient querying by date
    __table_args__ = (Index('ix_body_measurements_recorded_date', 'recorded_date'),)

    user = relationship("User", back_populates="measurements")

class WorkoutType(Base):
    """
    Different types of workouts that can be logged in the system.
    """
    __tablename__ = 'workout_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False, unique=True)
    
    # Relationship with Workout - one workout type can be associated with many workouts
    workouts = relationship("Workout", back_populates="workout_type")

class Workout(Base):
    """
    Workout sessions logged by users. Stores details like duration, intensity, and calories burned.
    """
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    workout_type_id = Column(Integer, ForeignKey('workout_types.id'), nullable=False)
    duration = Column(Integer, nullable=False)
    intensity_level = Column(Integer)
    calories_burned = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    # Index for efficient querying by date
    __table_args__ = (
        Index('ix_workouts_user_id_date', 'user_id', 'date'),)

    user = relationship("User", back_populates="workouts")
    workout_type = relationship("WorkoutType", back_populates="workouts")

class MealType(Base):
    """
    Types of meals that can be recorded (e.g., breakfast, lunch, dinner).
    """
    __tablename__ = 'meal_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False, unique=True)

class Nutrition(Base):
    """
    Nutritional intake records, detailing calorie count and macro breakdown for meals.
    """
    __tablename__ = 'nutrition'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    meal_type_id = Column(Integer, ForeignKey('meal_types.id'), nullable=False)
    calories = Column(Integer, nullable=False)
    protein = Column(Float)
    carbs = Column(Float)
    fats = Column(Float)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    # Index for efficient querying by date
    __table_args__ = (
        Index('ix_nutrition_user_id_date', 'user_id', 'date'),)

    user = relationship("User", back_populates="nutrition_logs")

class Sleep(Base):
    """
    The Sleep class maps to the 'sleep' table and includes information about the user's sleep patterns.
    It tracks the duration, quality, and date of sleep.
    
    Attributes:
        id (Integer): The primary key that uniquely identifies the sleep record.
        user_id (Integer): A foreign key that links to the 'users' table.
        duration (Float): The total number of hours slept.
        quality (Integer): An assessment of the sleep quality on a given scale.
        date (DateTime): The date and time when the sleep data was recorded.
    """
    
    __tablename__ = 'sleep'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    duration = Column(Float, nullable=False)
    quality = Column(Integer)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    # Index for efficient querying by date
    __table_args__ = (
        Index('ix_sleep_user_id_date', 'user_id', 'date'),)

    user = relationship("User", back_populates="sleep_records")

class HealthMetric(Base):
    """
    The HealthMetric class represents a table for tracking various health metrics.
    It stores metrics such as heart rate and blood pressure.

    Attributes:
        id (Integer): The primary key for the health metrics record.
        user_id (Integer): A foreign key that references the 'users' table.
        heart_rate (Integer): The user's heart rate in beats per minute.
        blood_pressure (String): The user's blood pressure readings.
        recorded_date (DateTime): The date and time when the metrics were recorded.
    """
    
    __tablename__ = 'health_metrics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    heart_rate = Column(Integer)
    blood_pressure = Column(String)
    recorded_date = Column(DateTime, default=datetime.datetime.utcnow)

    # Index for efficient querying by user and date
    __table_args__ = (
        Index('ix_health_metrics_user_id_recorded_date', 'user_id', 'recorded_date'),)

    user = relationship("User", back_populates="health_metrics")

class MoodType(Base):
    """
    The MoodType class maps to the 'mood_types' table and defines various types of moods that can be recorded.

    Attributes:
        id (Integer): The primary key for the mood type record.
        mood (String): The descriptor of the mood type.
    """
    
    __tablename__ = 'mood_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    mood = Column(String, nullable=False, unique=True)

class MentalHealth(Base):
    """
    The MentalHealth class tracks mental health-related data including stress levels,
    mindfulness activity duration, and general descriptions of the user's mental health activities.
    
    Attributes:
        id (Integer): The primary key for the mental health record.
        user_id (Integer): A foreign key that links to the 'users' table.
        mood_type_id (Integer): A foreign key that references the 'mood_types' table to identify the mood type.
        stress_level (Integer): A numerical indicator of the user's stress level.
        mindfulness_duration (Integer): Time spent on mindfulness activities in minutes.
        activity_description (String): A brief description of the mental health-related activity.
        recorded_date (DateTime): The date and time the mental health data was logged.
    """
    
    __tablename__ = 'mental_health'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    mood_type_id = Column(Integer, ForeignKey('mood_types.id'), nullable=False)
    stress_level = Column(Integer)
    mindfulness_duration = Column(Integer)
    activity_description = Column(String)
    recorded_date = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="mental_health_logs")

    __table_args__ = (
        Index('ix_mental_health_user_id_recorded_date', 'user_id', 'recorded_date'),)

class HealthRecommendation(Base):
    """
    The HealthRecommendation class is for storing personalized health recommendations for users.
    Recommendations can be marked as active or inactive.
    
    Attributes:
        id (Integer): The primary key for the health recommendation.
        user_id (Integer): A foreign key that references the 'users' table.
        recommendation_text (String): The content of the health recommendation.
        is_active (Boolean): Flag to indicate if the recommendation is currently active.
        created_date (DateTime): The date and time the recommendation was created.
    """
    
    __tablename__ = 'health_recommendations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recommendation_text = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="health_recommendations")

def get_new_session(database_url):
    """
    Create and return a new session for the database connection.

    Args:
        database_url (str): The URL for the database connection.

    Returns:
        Session: A SQLAlchemy session object.
    """
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return Session()

def create_tables():
    """
    Create all tables in the database according to the defined classes and relationships.
    """
    Base.metadata.create_all(engine)

create_tables()