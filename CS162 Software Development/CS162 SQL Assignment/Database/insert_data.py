from faker import Faker
import random
from create import User, BodyMeasurement, WorkoutType, Workout, MealType, Nutrition, Sleep, HealthMetric, MoodType, MentalHealth, HealthRecommendation, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Initialize Faker for data generation
fake = Faker()

# Set up database session
Session = sessionmaker(bind=engine)
session = Session()

def populate_users(session, user_count_range=(5, 20)):
    """Populate the database with random users."""
    for _ in range(random.randint(*user_count_range)):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password_hash=fake.sha256(raw_output=False),
            date_of_birth=fake.date_of_birth()
        )
        session.add(user)

populate_users(session)
session.commit()  # Users need to exist before related records can be added

users = session.query(User).all()

# Helper function to add random body measurements for users
def add_body_measurements(session, users, measurement_range=(1, 3)):
    for user in users:
        for _ in range(random.randint(*measurement_range)):
            measurement = BodyMeasurement(
                user_id=user.id,
                height=random.uniform(1.5, 2.0),
                weight=random.uniform(50.0, 100.0),
                recorded_date=fake.past_date()
            )
            session.add(measurement)

add_body_measurements(session, users)

# Predefined workout types to add to the database
workout_types = ['Running', 'Swimming', 'Cycling', 'Yoga', 'Weight Training']
for workout in workout_types:
    workout_type = WorkoutType(type=workout)
    session.add(workout_type)

session.commit()  # WorkoutType IDs are needed for Workout records

# Populate workouts for each user
def populate_workouts(session, users, workout_type_ids, workout_range=(5, 20)):
    for user in users:
        for _ in range(random.randint(*workout_range)):
            workout = Workout(
                user_id=user.id,
                workout_type_id=random.choice(workout_type_ids),
                duration=random.randint(20, 120),
                intensity_level=random.randint(1, 10),
                calories_burned=random.randint(100, 700),
                date=fake.past_date()
            )
            session.add(workout)

workout_type_ids = [wt.id for wt in session.query(WorkoutType).all()]
populate_workouts(session, users, workout_type_ids)

# Add meal types
meal_types = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
for meal in meal_types:
    meal_type = MealType(type=meal)
    session.add(meal_type)

session.commit()

# Generate random nutrition logs
meal_type_ids = [mt.id for mt in session.query(MealType).all()]
for user in users:
    for _ in range(random.randint(5, 20)):
        nutrition = Nutrition(
            user_id=user.id,
            meal_type_id=random.choice(meal_type_ids),
            calories=random.randint(100, 900),
            protein=random.uniform(10.0, 30.0),
            carbs=random.uniform(20.0, 50.0),
            fats=random.uniform(5.0, 20.0),
            date=fake.past_date()
        )
        session.add(nutrition)

# Generate random sleep records
for user in users:
    for _ in range(random.randint(5, 20)):
        sleep_record = Sleep(
            user_id=user.id,
            duration=random.uniform(4.0, 12.0),
            quality=random.randint(1, 10),
            date=fake.past_date()
        )
        session.add(sleep_record)

# Generate random health metrics
for user in users:
    for _ in range(random.randint(5, 20)):
        health_metric = HealthMetric(
            user_id=user.id,
            heart_rate=random.randint(60, 100),
            blood_pressure=f"{random.randint(100, 140)}/{random.randint(60, 90)}",
            recorded_date=fake.past_date()
        )
        session.add(health_metric)

# Generate mood types
moods = ['Happy', 'Sad', 'Angry', 'Excited', 'Stressed']
for mood in moods:
    mood_type = MoodType(mood=mood)
    session.add(mood_type)

session.commit()

# Generate mental health logs
mood_type_ids = [mt.id for mt in session.query(MoodType).all()]
for user in users:
    for _ in range(random.randint(5, 20)):
        mental_health_log = MentalHealth(
            user_id=user.id,
            mood_type_id=random.choice(mood_type_ids),
            stress_level=random.randint(1, 10),
            mindfulness_duration=random.randint(5, 60),
            activity_description=fake.text(max_nb_chars=200),
            recorded_date=fake.past_date()
        )
        session.add(mental_health_log)

session.commit()
session.close()  # Always close the session when done

session = Session()

try:
    # Begin a transaction to ensure atomicity of user creation and related records
    # Atomicity guarantees that a series of database operations are treated as a single unit,
    # which either all succeed or all fail, thus preventing partial updates that could lead
    # to data inconsistency. This is critical when operations are interdependent, such as
    # creating a user and their associated health records.

    # Create a new user with generated attributes
    new_user = User(
        username=fake.user_name(),
        email=fake.email(),
        password_hash=fake.sha256(raw_output=False),
        date_of_birth=fake.date_of_birth()
    )
    session.add(new_user)
    
    # Flush the session to get the user ID generated by the database
    # This ID is required for the foreign key relationships of subsequent records.
    # Flushing within the transaction ensures the ID is available without committing the transaction,
    # maintaining the atomicity of the operation.
    session.flush()

    # Body measurements and health metrics are related to the user and are critical to the user's profile.
    # By including these operations in the same transaction, we ensure that either all user-related
    # data is persisted correctly or none at all, maintaining the referential integrity and
    # avoiding orphan records in case of failure.

    # Add body measurements for the new user
    new_measurement = BodyMeasurement(
        user_id=new_user.id,
        height=random.uniform(1.5, 2.0),  # Meters
        weight=random.uniform(50.0, 100.0),  # Kilograms
        recorded_date=fake.past_date()
    )
    session.add(new_measurement)

    # Add health metrics for the new user
    new_health_metric = HealthMetric(
        user_id=new_user.id,
        heart_rate=random.randint(60, 100),  # BPM
        blood_pressure=f"{random.randint(100, 140)}/{random.randint(60, 90)}",
        recorded_date=fake.past_date()
    )
    session.add(new_health_metric)

    # Commit the transaction
    # Only after all related records are successfully added do we commit the transaction,
    # ensuring the database reflects a complete set of changes.
    session.commit()

except SQLAlchemyError as e:
    # Roll back the transaction on error
    # If any operation within the transaction fails, rollback is invoked to undo all operations,
    # ensuring that no incomplete or invalid data is left in the database, thus preserving data integrity.
    session.rollback()
    print(f"Transaction failed: {e}")
    raise
finally:
    # Always close the session
    # Independent of the transaction's success or failure, the session is closed to free resources.
    # This is a best practice for database connection management.
    session.close()

def populate_health_recommendations(session, users, recommendation_range=(1, 5)):
    """Populate the database with random health recommendations for users."""
    try:
        # Begin a transaction for health recommendations
        for user in users:
            # Make sure to access the user's id while the session is active
            user_id = user.id  
            for _ in range(random.randint(*recommendation_range)):
                health_recommendation = HealthRecommendation(
                    user_id=user_id,
                    recommendation_text=fake.sentence(nb_words=6),
                    is_active=fake.boolean(chance_of_getting_true=75),
                    created_date=fake.past_date()
                )
                session.add(health_recommendation)
        
        # Commit the transaction after all health recommendations have been added
        session.commit()
        
    except SQLAlchemyError as e:
        # Roll back the transaction if any error occurs
        session.rollback()
        print(f"Transaction failed: {e}")
        raise

# Ensure that the session is not closed until all operations are complete
session = Session()

# Pre-fetch user IDs if they are not already loaded
users = session.query(User).all()  # This should load the user IDs

# Call the function to populate health recommendations
populate_health_recommendations(session, users)

# Close the session after all operations are complete
session.close()