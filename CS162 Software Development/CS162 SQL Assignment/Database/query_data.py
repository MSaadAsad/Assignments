# Import necessary libraries and modules from SQLAlchemy and datetime package.
from sqlalchemy import func, and_
from datetime import datetime, timedelta

# Import classes for each table in the database and the engine object from create.py.
from create import (
    User, BodyMeasurement, WorkoutType, Workout, MealType,
    Nutrition, Sleep, HealthMetric, MentalHealth, engine
)

# Import sessionmaker for creating a session with the database.
from sqlalchemy.orm import sessionmaker

# Set up a new session factory bound to the engine.
Session = sessionmaker(bind=engine)
session = Session()  # Instantiate a session.

# --- Calories Burned Query ---
# Query to find the total number of calories burned per user.
# Joins User and Workout tables, groups by username, and sums the calories burned.
total_calories_per_user = session.query(
    User.username,
    func.sum(Workout.calories_burned).label('total_calories_burned')
).join(User.workouts).group_by(User.username)

print("Total Calories Burned Per User:")
for username, total_calories in total_calories_per_user:
    print(f"{username:20} | {total_calories:10} calories")
print("-" * 35)

# --- Latest Body Measurements Query ---
# Subquery to get the latest body measurement date for each user.
latest_body_measurement_subquery = session.query(
    BodyMeasurement.user_id,
    func.max(BodyMeasurement.recorded_date).label('latest_date')
).group_by(BodyMeasurement.user_id).subquery('latest_measurements')

# Main query to get the latest body measurements using the subquery.
latest_body_measurement = session.query(
    User.username,
    BodyMeasurement.height,
    BodyMeasurement.weight
).join(User.measurements).join(
    latest_body_measurement_subquery,
    and_(
        BodyMeasurement.user_id == latest_body_measurement_subquery.c.user_id,
        BodyMeasurement.recorded_date == latest_body_measurement_subquery.c.latest_date
    )
).all()

print("Users and Their Latest Body Measurements:")
for username, height, weight in latest_body_measurement:
    print(f"{username:20} | Height: {height:10} cm | Weight: {weight:10} kg")
print("-" * 60)

# --- Average Sleep Duration Query ---
# Query to find the average sleep duration per user over the past month.
# Filters Sleep records to the last 30 days and calculates the average duration.
average_sleep_duration = session.query(
    User.username,
    func.avg(Sleep.duration).label('average_sleep_duration')
).join(User.sleep_records).filter(
    Sleep.date.between(datetime.now() - timedelta(days=30), datetime.now())
).group_by(User.username)

print("Average Sleep Duration Over the Last Month:")
for username, average_duration in average_sleep_duration:
    print(f"{username:20} | {average_duration:10.2f} hours")
print("-" * 35)

# --- Frequent Workout Types Query ---
# Query to find the top 5 most frequent workout types.
top_workout_types = session.query(
    WorkoutType.type,
    func.count(Workout.id).label('frequency')
).join(WorkoutType.workouts).group_by(WorkoutType.type).order_by(
    func.count(Workout.id).desc()
).limit(5)

print("Top 5 Most Frequent Workout Types:")
for workout_type, frequency in top_workout_types:
    print(f"{workout_type:20} | {frequency:10} times")
print("-" * 35)

# --- Last Nutrition Log Query ---
# Subquery to get the last nutrition log date for each user.
last_nutrition_date_subquery = session.query(
    Nutrition.user_id,
    func.max(Nutrition.date).label('last_date')
).group_by(Nutrition.user_id).subquery('last_nutrition_log')

# Query to get nutrition details on the last logged day by joining with the subquery.
nutrition_on_last_logged_day = session.query(
    User.username,
    Nutrition.calories,
    Nutrition.protein,
    Nutrition.carbs,
    Nutrition.fats
).join(User.nutrition_logs).join(
    last_nutrition_date_subquery,
    and_(
        Nutrition.user_id == last_nutrition_date_subquery.c.user_id,
        Nutrition.date == last_nutrition_date_subquery.c.last_date
    )
).all()

print("Users' Nutrition Intake on Their Last Logged Day:")
for username, calories, protein, carbs, fats in nutrition_on_last_logged_day:
    print(f"{username:20} | Calories: {calories:10} kcal | Protein: {protein:5}g | Carbs: {carbs:5}g | Fats: {fats:5}g")
print("-" * 85)

# --- Health Metrics and Mental Health Queries ---
# Query for average heart rate per user.
average_heart_rate = session.query(
    User.username,
    func.avg(HealthMetric.heart_rate).label('average_heart_rate')
).join(User.health_metrics).group_by(User.username)

print("Average Heart Rate Per User:")
for username, avg_hr in average_heart_rate:
    print(f"{username:20} | {avg_hr:10.2f} bpm")
print("-" * 35)

# Subquery to get the latest mental health log date per user.
latest_mental_health_subquery = session.query(
    MentalHealth.user_id,
    func.max(MentalHealth.recorded_date).label('latest_date')
).group_by(MentalHealth.user_id).subquery('latest_mental_health')

# Query for the latest mental health log per user using the subquery for the latest date.
latest_mental_health = session.query(
    User.username,
    MentalHealth.stress_level,
    MentalHealth.mindfulness_duration
).join(User.mental_health_logs).join(
    latest_mental_health_subquery,
    and_(
        MentalHealth.user_id == latest_mental_health_subquery.c.user_id,
        MentalHealth.recorded_date == latest_mental_health_subquery.c.latest_date
    )
).all()

print("Users and Their Latest Mental Health Logs:")
for username, stress_level, mindfulness_duration in latest_mental_health:
    print(f"{username:20} | Stress Level: {stress_level:10} | Mindfulness Duration: {mindfulness_duration:10} min")
print("-" * 85)

# Close the session after you're done with the queries to release resources.
session.close()