# Health and Fitness Tracking App

## Overview

The Health and Fitness Tracking App is a digital platform designed to assist users in monitoring and understanding their health and fitness data. The app aims to empower individuals to make informed decisions about their lifestyle and wellness routines by leveraging a robust database and user-friendly interface.

## Objectives

- **Personalized Health Monitoring:** Enable users to track specific health metrics tailored to their needs.
- **Workout Logging:** Users can log various workout details, including type, duration, and intensity.
- **Nutritional Tracking:** The app comprehensively monitors users' nutritional intake, focusing on calorie tracking and macro breakdowns.
- **Sleep Pattern Analysis:** Users can record and analyze their sleep duration and quality to better understand their rest cycles.
- **Mental Wellness:** Track mental health activities, stress levels, and general mood to support overall well-being.
- **Health Recommendations:** Provide personalized health recommendations to users based on their logged data.

## Target Audience

This app's primary audience includes health-conscious individuals looking to improve or maintain their fitness and well-being through data-driven insights.

## Data Stored
Scehma.png

- `users`: Stores personal and authentication details of each user along with links to their health and fitness records.
- `body_measurements`: Keeps track of user body metrics like height and weight over time.
- `workout_types`: Defines different types of workouts that users can log.
- `workouts`: Records details of each workout session, including type, duration, intensity, and calories burned.
- `meal_types`: Categorizes types of meals, such as breakfast, lunch, dinner, etc.
- `nutrition`: Logs nutritional intake details, including calorie count and macronutrient breakdown for user meals.
- `sleep`: Captures data on user sleep patterns, including duration and quality of sleep.
- `health_metrics`: Tracks various health metrics such as heart rate and blood pressure for users.
- `mood_types`: Lists types of moods that users can record for mental health tracking.
- `mental_health`: Logs mental health data, including stress levels, mood types, and mindfulness activities.
- `health_recommendations`: Contains personalized health and fitness recommendations for each user.

## Database Schema Design

The database schema provides a comprehensive overview of users' health and fitness data while ensuring data integrity and efficient querying. Primary keys ensure the uniqueness of records, while foreign keys enforce relationships between different data entities. Indexes on frequently searched fields like `username,` `email,` and `recorded_date` across various tables optimize query performance. Data validation is also applied to ensure data input is within reasonable expected range.

## Database Design Considerations

### Primary and Foreign Key Usage

- **Primary Keys** are unique identifiers for each record within a table. In this database, they ensure that each user, workout, nutrition log, etc., has a unique identifier, such as `id,` which is crucial for indexing and managing relationships between tables.

- **Foreign Keys** establish a link between related data across different tables. For example, `user_id` in the `workouts` table references the `id` in the `users` table, enabling the database to maintain consistent and coherent data about which workouts belong to which users.

### Normalization

Normalization is organizing data in a database to reduce redundancy and improve data integrity. This database is normalized to the Third Normal Form (3NF), building upon the requirements of the First (1NF) and Second (2NF) Normal Forms.

#### First Normal Form (1NF)

- **Atomicity**: Each field contains indivisible atomic values with no repeating groups or arrays.
- **Unique Identifiers**: A primary key in each table ensures each record is unique and identifiable.
- **Data Consistency**: Using consistent data types and formats across similar fields prevents data conflicts.

By satisfying 1NF, the database ensures a solid foundation where each table represents a single entity or concept, and each row/column intersection contains a single value.

#### Second Normal Form (2NF)

- **Elimination of Partial Dependencies**: By ensuring that all non-key attributes are fully functionally dependent on the primary key, not just part of it, the database eliminates partial dependencies.
  
This step requires the presence of a primary key, and in the case of composite primary keys, it ensures that no attribute is dependent on only a part of the key. Thus, all the fields in a table relate directly to the primary key, enhancing data retrieval speed and consistency.

#### Third Normal Form (3NF)

- **Removal of Transitive Dependencies**: Non-key attributes are not allowed to depend on other non-key attributes, which means all attributes are directly dependent on the primary key.
  
By reaching 3NF, the database avoids transitive dependencies, which not only keeps data redundancy to a minimum but also protects data integrity by preventing anomalies that can occur during data operations (inserts, updates, or deletions).

### Importance of 3NF

Maintaining 3NF is crucial for several reasons:

- **Data Integrity**: There's a single source of truth for each piece of information, which prevents data duplication and inconsistency.
- **Maintenance**: Simplifies maintenance tasks because updates, inserts, or deletes need to happen in only one place.
- **Performance**: Improves query performance due to reduced data duplication and a more efficient structure.
- **Flexibility**: Makes the database more adaptable to changes, as adjustments for evolving business requirements can be made without extensive redesign.
- **Clarity**: Provides more apparent relationships between entities, which can be crucial for developers and analysts when understanding the database structure.

The careful design aligned with 1NF, 2NF, and 3NF principles is essential for a robust, reliable, and efficient database system like the Health and Fitness Tracking App.

### Query Optimization with Indices
Indices in this health and fitness tracking application are used to speed up data retrieval from the database. They are especially valuable when querying large datasets, as they prevent the need for full table scans. For instance, the `users` table has indices on `username` and `email,` which are likely to be used often to look up user information, thus accelerating search operations. Similarly, tables like `body_measurements,` `workouts,` `nutrition,` `sleep,` `health_metrics,` and `mental_health` have indices on user-related foreign keys and dates. Queries often filter or sort based on dates and user IDs. Indices on these columns mean the database can quickly locate and retrieve the relevant records without scanning the table. This leads to faster response times for end-users and reduced load on the database server, which is critical for providing a smooth user experience.


## Transactions and ACID Concepts in Data Insertion

The insert_data file illustrates database transactions, a key part of the ACID properties (Atomicity, Consistency, Isolation, Durability) essential for maintaining database integrity.

### Atomicity
Atomicity is demonstrated through transactions when adding new users and related records like body measurements and health metrics. The code ensures that all operations within a transaction block are treated as a single unit, meaning that they either succeed or are not applied. This is achieved by wrapping user creation and related data insertions within a `try` block, flushing to obtain user IDs for related records without committing, and then committing all at once if all insertions are successful.

### Consistency
Consistency is maintained by enforcing data integrity constraints and relationships. If a transaction fails, a `rollback` is initiated to undo any changes made during the transaction, ensuring the database remains consistent.

### Isolation
Isolation is implicitly managed by SQLAlchemy's session and transaction management system. Each transaction is isolated from others, ensuring that the operations within a transaction are completed without interference from other concurrent transactions.

### Durability
Durability is guaranteed by committing the transactions to the database. Once the transaction is executed, the changes are permanent, even in the event of a system failure, ensuring the reliability of the data.

The use of transactions in this code shows a commitment to the ACID properties, ensuring that the database operations are reliable, consistent, and correct.

## Database Query Intentions

The SQL queries in the code aim to extract specific insights from a health and fitness tracking application's database:

### Total Calories Burned Per User
This query calculates the sum of calories each user burns through their workout sessions, giving an overview of their total energy expenditure.
Query Screenshots/Screen Shot 2023-11-09 at 3.25.00 PM.png

### Latest Body Measurements Per User
This query retrieves each user's most recent height and weight measurements, providing up-to-date information on their physical dimensions.
Query Screenshots/Screen Shot 2023-11-09 at 3.25.45 PM.png

### Average Sleep Duration
This query determines the average sleep duration for each user over the past month, offering insight into their sleep patterns.
Query Screenshots/Screen Shot 2023-11-09 at 3.25.54 PM.png

### Top 5 Frequent Workout Types
This query identifies the five most common workout types across all users, highlighting the most popular fitness activities within the app's community.
Query Screenshots/Screen Shot 2023-11-09 at 3.26.01 PM.png

### Last Nutrition Log Entry
This query finds the details of each user's last recorded nutrition log, showing their most recent dietary intake.
Query Screenshots/Screen Shot 2023-11-09 at 3.26.13 PM.png

### Average Heart Rate Per User
This query computes the average heart rate for each user, which can indicate cardiovascular fitness or stress.
Query Screenshots/Screen Shot 2023-11-09 at 3.26.19 PM.png

### Latest Mental Health Log
This query fetches each user's latest recorded mental health log, revealing their most recent stress levels and mindfulness activity durations.
Query Screenshots/Screen Shot 2023-11-09 at 3.26.27 PM.png

## File Overview

### `create.py`
- **Purpose**: Establishes the structure of the database.
- **Functionality**: Contains class definitions for each table using SQLAlchemy ORM, sets up the database engine, and executes commands to create the database with the defined schema.

### `insert_data.py`
- **Purpose**: Populates the database with data.
- **Functionality**: Utilizes the Faker library to generate and insert randomized but realistic data into the tables for users, body measurements, workouts, meal types, nutrition logs, sleep records, health metrics, and mental health logs.

### `query_data.py`
- **Purpose**: Retrieves and displays information from the database.
- **Functionality**: Contains various SQL queries executed via SQLAlchemy ORM that pull and aggregate data from the database, such as total calories burned per user, latest body measurements, average sleep duration, frequent workout types, last nutrition log, and latest mental health logs. Outputs the results of these queries to the console.

## Setting Up the Development Environment

Instructions for setting up the Python virtual environment and installing dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

python create.py
python insert_data.py
python query_data.py
```

## Testing

DB Browser for SQLite was used for testing.
DB Browser.png