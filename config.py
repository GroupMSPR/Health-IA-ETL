import os
import uuid

from dotenv import load_dotenv
from sqlalchemy import (
    NUMERIC,
    SMALLINT,
    TEXT,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    Time,
    Uuid,
)
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


class Consume(Base):
    __tablename__ = "consume"

    consume_id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id"))
    food_id = Column(ForeignKey("foods.id"))

    user = relationship("User", back_populates="consumes")
    food = relationship("Food", back_populates="consumes")


class Practice(Base):
    __tablename__ = "practice"

    practice_id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id"))
    exercise_id = Column(ForeignKey("exercises.id"))

    user = relationship("User", back_populates="practice")
    exercise = relationship("Exercise", back_populates="practice")


class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True)
    password = Column(String(50))
    birthdate = Column(Date)
    gender = Column(String(50))
    weight = Column(NUMERIC(15, 2))
    height = Column(Integer)
    bmi = Column(NUMERIC(15, 2))
    body_fat_pct = Column(NUMERIC(15, 2))
    physical_activity_level = Column(String(50))
    daily_caloric_intake = Column(Integer)
    goal = Column(TEXT)
    subscription = Column(String(50))
    date_subscription = Column(Date)
    constraints = Column(Text)

    consumes = relationship("Consume", back_populates="user")
    practice = relationship("Practice", back_populates="user")


class Food(Base):
    __tablename__ = "foods"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    category = Column(String(50))
    calories = Column(NUMERIC(15, 2))
    protein = Column(NUMERIC(15, 2))
    carbohydrates = Column(NUMERIC(15, 2))
    fat = Column(NUMERIC(15, 2))
    fiber = Column(NUMERIC(15, 2))
    sugars = Column(NUMERIC(15, 2))
    sodium = Column(SMALLINT)
    cholesterol = Column(SMALLINT)

    consumes = relationship("Consume", back_populates="food")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    target_muscle = Column(Text, nullable=False)
    secondary_muscle = Column(Text, nullable=False)
    equipment = Column(Text, nullable=False)
    difficulty_level = Column(String(50), nullable=False)
    instructions = Column(Text, nullable=False)
    constraints = Column(Text)

    practice = relationship("Practice", back_populates="exercise")


class Health_metric(Base):
    __tablename__ = "health_metrics"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    start_weight = Column(Numeric(15, 2), nullable=False)
    current_weight = Column(Numeric(15, 2), nullable=False)
    avg_bpm = Column(Numeric(15, 2), nullable=False)
    max_bpm = Column(Numeric(15, 2), nullable=False)
    resting_bpm = Column(Numeric(15, 2), nullable=False)
    steps_count = Column(SmallInteger, nullable=False)
    sleep_time = Column(Time, nullable=False)
    calories_burned = Column(Numeric(15, 2), nullable=False)
    active_minute = Column(Numeric(15, 2), nullable=False)
    workout_type = Column(String(50), nullable=False)
