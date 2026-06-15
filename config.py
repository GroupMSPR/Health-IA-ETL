import os
import uuid
from dotenv import load_dotenv
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, Numeric, SMALLINT, String, Text, Time, Uuid
from sqlalchemy.orm import DeclarativeBase, relationship

load_dotenv()

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
TMP_PATH = os.path.join(BASE_PATH, "tmp")
TO_IMPORT_ID = os.getenv("TO_IMPORT_ID")
ARCHIVE_ID = os.getenv("ARCHIVE_ID")
ERROR_ID = os.getenv("ERROR_ID")
LOG_ID = os.getenv("LOG_ID")

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    profile_picture = Column(Text)
    birthdate = Column(Date, nullable=False)
    gender = Column(String(50), nullable=False)
    weight = Column(Numeric(15, 2), nullable=False)
    height = Column(Integer, nullable=False)
    bmi = Column(Numeric(15, 2), nullable=False)
    body_fat_pct = Column(Numeric(15, 2), nullable=False)
    physical_activity_level = Column(String(50), nullable=False)
    daily_caloric_intake = Column(Integer, nullable=False)
    favorite_exercise_category = Column(String(150))

    consumes = relationship("Consume", back_populates="user")
    practice = relationship("Practice", back_populates="user")
    health_metrics = relationship("Health_metric", back_populates="user")
    subscriptions = relationship("User_subscription", back_populates="user")
    user_constraints = relationship("User_constraint", back_populates="user")
    user_goals = relationship("User_goal", back_populates="user")
    user_equipments = relationship("User_equipment", back_populates="user")

class Food(Base):
    __tablename__ = "foods"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    image = Column(String(500))
    calories = Column(Numeric(15, 2), nullable=False)
    protein = Column(Numeric(15, 2), nullable=False)
    carbohydrates = Column(Numeric(15, 2), nullable=False)
    fat = Column(Numeric(15, 2), nullable=False)
    fiber = Column(Numeric(15, 2), nullable=False)
    sugars = Column(Numeric(15, 2), nullable=False)
    sodium = Column(SMALLINT, nullable=False)
    cholesterol = Column(SMALLINT, nullable=False)

    consumes = relationship("Consume", back_populates="food")
    food_constraints = relationship("Food_constraint", back_populates="food")

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    instructions = Column(Text, nullable=False)
    short_description = Column(String(300), nullable=False)
    category = Column(String(100), nullable=False)
    sub_category = Column(String(150), nullable=False)
    image = Column(String(500))
    difficulty_level = Column(String(50), nullable=False)
    rep_range_min = Column(Integer, nullable=False)
    rep_range_max = Column(Integer, nullable=False)
    recommended_duration_seconds = Column(Integer, nullable=False)
    recommended_rest_seconds = Column(Integer, nullable=False)
    estimated_calories_per_minute = Column(Integer, nullable=False)
    range_of_motion = Column(Integer, nullable=False)
    injury_risk_level = Column(Integer, nullable=False)
    next_progression_exercise = Column(String(50))
    previous_progression_exercise = Column(String(50))

    practice = relationship("Practice", back_populates="exercise")
    exercise_constraints = relationship("Exercise_constraint", back_populates="exercise")
    exercise_goals = relationship("Exercise_goal", back_populates="exercise")
    primary_muscles = relationship("Primary_muscle", back_populates="exercise")
    secondary_muscles = relationship("Secondary_muscle", back_populates="exercise")
    exercise_equipments = relationship("Exercise_equipment", back_populates="exercise")

class Health_metric(Base):
    __tablename__ = "health_metrics"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=False, unique=True)
    date = Column(DateTime, nullable=False)
    start_weight = Column(Numeric(15, 2), nullable=False)
    current_weight = Column(Numeric(15, 2), nullable=False)
    avg_bpm = Column(Numeric(15, 2), nullable=False)
    max_bpm = Column(Numeric(15, 2), nullable=False)
    resting_bpm = Column(Numeric(15, 2), nullable=False)
    steps_count = Column(SMALLINT, nullable=False)
    sleep_time = Column(Time, nullable=False)
    calories_burned = Column(Numeric(15, 2), nullable=False)
    active_minute = Column(Numeric(15, 2), nullable=False)

    user = relationship("User", back_populates="health_metrics")

class Constraint(Base):
    __tablename__ = "constraints"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(150))
    description = Column(String(50))
    severity = Column(String(50))

    exercise_constraints = relationship("Exercise_constraint", back_populates="constraint")
    user_constraints = relationship("User_constraint", back_populates="constraint")
    food_constraints = relationship("Food_constraint", back_populates="constraint")

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    goal = Column(String(255))

    user_goals = relationship("User_goal", back_populates="goal")
    exercise_goals = relationship("Exercise_goal", back_populates="goal")

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    subscription_type = Column(String(15))

    user_subscriptions = relationship("User_subscription", back_populates="subscription")

class Muscle(Base):
    __tablename__ = "muscles"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(50))

    primary_muscles = relationship("Primary_muscle", back_populates="muscle")
    secondary_muscles = relationship("Secondary_muscle", back_populates="muscle")

class Equipment(Base):
    __tablename__ = "equipments"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(150))

    exercise_equipments = relationship("Exercise_equipment", back_populates="equipment")
    user_equipments = relationship("User_equipment", back_populates="equipment")

class Consume(Base):
    __tablename__ = "consume"

    consume_id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id"))
    food_id = Column(ForeignKey("foods.id"))
    is_liked = Column(Boolean)

    user = relationship("User", back_populates="consumes")
    food = relationship("Food", back_populates="consumes")

class Practice(Base):
    __tablename__ = "practice"

    practice_id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id"))
    exercise_id = Column(ForeignKey("exercises.id"))
    practiced_at = Column(DateTime, nullable=False)
    is_liked = Column(Boolean)

    user = relationship("User", back_populates="practice")
    exercise = relationship("Exercise", back_populates="practice")

class User_subscription(Base):
    __tablename__ = "user_subscription"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id"))
    subscription_id = Column(ForeignKey("subscriptions.id"))
    started_at = Column(DateTime)
    ended_at = Column(DateTime)

    user = relationship("User", back_populates="subscriptions")
    subscription = relationship("Subscription", back_populates="user_subscriptions")

class Exercise_constraint(Base):
    __tablename__ = "exercise_constraint"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    exercise_id = Column(ForeignKey("exercises.id"))
    constraint_id = Column(ForeignKey("constraints.id"))

    exercise = relationship("Exercise", back_populates="exercise_constraints")
    constraint = relationship("Constraint", back_populates="exercise_constraints")

class User_constraint(Base):
    __tablename__ = "user_constraint"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id"))
    constraint_id = Column(ForeignKey("constraints.id"))

    user = relationship("User", back_populates="user_constraints")
    constraint = relationship("Constraint", back_populates="user_constraints")

class User_goal(Base):
    __tablename__ = "user_goal"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id"))
    goal_id = Column(ForeignKey("goals.id"))

    user = relationship("User", back_populates="user_goals")
    goal = relationship("Goal", back_populates="user_goals")

class Exercise_goal(Base):
    __tablename__ = "exercise_goal"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    exercise_id = Column(ForeignKey("exercises.id"))
    goal_id = Column(ForeignKey("goals.id"))

    exercise = relationship("Exercise", back_populates="exercise_goals")
    goal = relationship("Goal", back_populates="exercise_goals")

class Primary_muscle(Base):
    __tablename__ = "primary_muscle"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    exercise_id = Column(ForeignKey("exercises.id"))
    muscle_id = Column(ForeignKey("muscles.id"))

    exercise = relationship("Exercise", back_populates="primary_muscles")
    muscle = relationship("Muscle", back_populates="primary_muscles")

class Secondary_muscle(Base):
    __tablename__ = "secondary_muscle"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    exercise_id = Column(ForeignKey("exercises.id"))
    muscle_id = Column(ForeignKey("muscles.id"))

    exercise = relationship("Exercise", back_populates="secondary_muscles")
    muscle = relationship("Muscle", back_populates="secondary_muscles")

class Exercise_equipment(Base):
    __tablename__ = "exercise_equipment"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    exercise_id = Column(ForeignKey("exercises.id"))
    equipment_id = Column(ForeignKey("equipments.id"))

    exercise = relationship("Exercise", back_populates="exercise_equipments")
    equipment = relationship("Equipment", back_populates="exercise_equipments")

class User_equipment(Base):
    __tablename__ = "user_equipment"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id"))
    equipment_id = Column(ForeignKey("equipments.id"))

    user = relationship("User", back_populates="user_equipments")
    equipment = relationship("Equipment", back_populates="user_equipments")

class Food_constraint(Base):
    __tablename__ = "food_constraint"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    food_id = Column(ForeignKey("foods.id"))
    constraint_id = Column(ForeignKey("constraints.id"))

    food = relationship("Food", back_populates="food_constraints")
    constraint = relationship("Constraint", back_populates="food_constraints")