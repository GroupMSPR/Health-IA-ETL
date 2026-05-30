import datetime
from typing import Any, List

import pandas

from sqlalchemy.orm import Session
from sqlalchemy.sql.schema import Column
from config import (
    ARCHIVE_ID,
    ERROR_ID,
    LOG_ID,
    Consume,
    Exercise,
    Food,
    Health_metric,
    Practice,
    User,
)
from utils.driveHelper import move_file
from utils.fileManager import WriteLog
from googleapiclient.discovery import Resource
from utils.dataframeFormatter import formatDataFrame


def sendToTable(data: pandas.DataFrame, file, session: Session, service: Resource):

    fileTableNumber: str = file["name"][0]

    fileLowered = file["name"].lower()

    if fileTableNumber.isnumeric():
        if fileTableNumber == "1":
            sendUserToDb(data, file, session, service)
        elif fileTableNumber == "2":
            sendExerciseToDb(data, file, session, service)
        elif fileTableNumber == "3":
            sendFoodToDb(data, file, session, service)
        elif fileTableNumber == "4":
            sendHealthMetricToDb(data, file, session, service)
        elif fileTableNumber == "5":
            sendUserFoodRelationToDb(data, file, session, service)
        elif fileTableNumber == "6":
            sendUserExerciseRelationToDb(data, file, session, service)
        else:
            WriteLog(
                service,
                LOG_ID,
                file["name"],
                "no matches with a table, index out of range 6",
            )
            move_file(service, file["id"], ERROR_ID)
            return
    else:
        if "user" in fileLowered:
            sendUserToDb(data, file, session, service)
        elif "exercise" in fileLowered:
            sendExerciseToDb(data, file, session, service)
        elif "food" in fileLowered:
            sendFoodToDb(data, file, session, service)
        elif "health" in fileLowered:
            sendHealthMetricToDb(data, file, session, service)
        elif "consume" in fileLowered:
            sendUserFoodRelationToDb(data, file, session, service)
        elif "practice" in fileLowered:
            sendUserExerciseRelationToDb(data, file, session, service)
        else:
            WriteLog(
                service,
                LOG_ID,
                file["name"],
                "no matches with a table, no index or name found",
            )
            move_file(service, file["id"], ERROR_ID)
            return


def sendUserToDb(data: pandas.DataFrame, file, session: Session, service: Resource):
    succesful: bool = True

    errorMessage = ""
    field = [
        "email",
        "password",
        "first_name",
        "last_name",
        "birthdate",
        "gender",
        "weight",
        "height",
        "body_fat_pct",
        "constraints",
        "physical_activity_level",
        "daily_caloric_intake",
        "goal",
        "subscription",
        "date_subscription",
    ]

    data, errorMessage = formatDataFrame(data, field)
    if errorMessage != "":
        WriteLog(service, LOG_ID, file["name"], errorMessage)
        move_file(service, file["id"], ERROR_ID)
        return

    data = data.fillna(0)

    try:
        if "birthdate" in data:
            data["birthdate"] = pandas.to_datetime(data["birthdate"]).dt.date

        if "subscription_date" in data:
            data["subscription_date"] = pandas.to_datetime(
                data["subscription_date"]
            ).dt.date

        for _, row in data.iterrows():
            user: User = User()

            if "email" in row and row.get("email") != 0:
                user.email = row.get("email")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain email attribute or email is misspelled or invalid.",
                )
                break

            if "password" in row and row.get("password") != 0:
                user.password = row.get("password")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain password attribute or password is misspelled or invalid.",
                )
                break

            if "first_name" in row and row.get("first_name") != 0:
                user.first_name = row.get("first_name")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain first_name attribute or first_name is misspelled or invalid.",
                )
                break

            if "last_name" in row and row.get("last_name") != 0:
                user.last_name = row.get("last_name")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain last_name attribute or last_name is misspelled or invalid.",
                )
                break

            if "birthdate" in row and row.get("birthdate") != 0:
                user.birthdate = row.get("birthdate")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain birthdate attribute or birthdate is misspelled or invalid.",
                )
                break

            gender = row.get("gender")
            if (
                "gender" in row
                and isinstance(gender, str)
                and gender.lower() in ["male", "female", "other"]
            ):
                user.gender = gender.lower()
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain gender attribute or gender is misspelled or invalid.",
                )
                break

            if "weight" in row and row.get("weight") != 0:
                user.weight = row.get("weight")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain weight attribute or weight is misspelled or invalid.",
                )
                break

            if "height" in row and row.get("height") != 0:
                user.height = row.get("height")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain height attribute or height is misspelled or invalid.",
                )
                break

            user.bmi = round(user.weight / (user.height**2), 2)

            if "body_fat_pct" in row and row.get("body_fat_pct") != 0:
                user.body_fat_pct = row.get("body_fat_pct")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain body_fat_pct attribute or body_fat_pct is misspelled or invalid.",
                )
                break

            constraints = row.get("constraints")
            if isinstance(constraints, list):
                user.constraints = ", ".join(constraints)
            elif "constraints" in row:
                user.constraints = row.get("constraints") or "Non renseigné"
            else:
                user.constraints = "Non renseigné"

            physicalActivityLevel = row.get("physical_activity_level")
            if (
                "physical_activity_level" in row
                and isinstance(physicalActivityLevel, str)
                and physicalActivityLevel.lower() in ["sedentary", "moderate", "active"]
            ):
                user.physical_activity_level = physicalActivityLevel.lower()
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain physical_activity_level attribute or physical_activity_level is misspelled or invalid.",
                )
                break

            if "daily_caloric_intake" in row and row.get("daily_caloric_intake") != 0:
                user.daily_caloric_intake = row.get("daily_caloric_intake")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain daily_caloric_intake attribute or daily_caloric_intake is misspelled or invalid.",
                )
                break

            if "goal" in row and row.get("goal") != 0:
                user.goal = row.get("goal")
            else:
                user.goal = "Non renseigné"

            subscription = row.get("subscription")
            if (
                "subscription" in row
                and isinstance(subscription, str)
                and subscription.lower() in ["freemium", "premium", "premium+"]
            ):
                user.subscription = subscription.lower()
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain subscription attribute or subscription is misspelled or invalid.",
                )
                break

            if row.get("date_subscription") != 0:
                user.date_subscription = row.get("date_subscription")

            session.add(user)
        if succesful:
            session.commit()

    except Exception as ex:
        succesful = False
        session.rollback()
        WriteLog(service, LOG_ID, file["name"], str(ex))

    if succesful:
        move_file(service, file["id"], ARCHIVE_ID, addDateToFile(file["name"]))
    else:
        move_file(service, file["id"], ERROR_ID)


def sendExerciseToDb(data: pandas.DataFrame, file, session: Session, service: Resource):
    succesful: bool = True

    errorMessage = ""
    field = [
        "name",
        "difficulty_level",
        "type",
        "target_muscle",
        "secondary_muscle",
        "equipment",
        "instructions",
        "constraints",
    ]

    data, errorMessage = formatDataFrame(data, field)
    if errorMessage != "":
        WriteLog(service, LOG_ID, file["name"], errorMessage)
        move_file(service, file["id"], ERROR_ID)
        return

    data = data.fillna(0)

    try:
        for _, row in data.iterrows():
            exercise: Exercise = Exercise()

            if "name" in row and row.get("name") != 0:
                exercise.name = row.get("name")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain name attribute or name is misspelled or invalid.",
                )
                break

            exercise.difficulty_level = row.get("difficulty_level") or "Non renseigné"
            exercise.type = row.get("type") or "Non renseigné"

            target_muscle = row.get("target_muscle")
            if isinstance(target_muscle, list):
                exercise.target_muscle = ", ".join(target_muscle)
            elif "target_muscle" in row:
                exercise.target_muscle = row.get("target_muscle") or "Non renseigné"
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain target_muscle attribute or target_muscle is misspelled.",
                )
                break

            secondaryMuscle = row.get("secondary_muscle") or "No Secondary Muscle"
            if isinstance(secondaryMuscle, list):
                exercise.secondary_muscle = ", ".join(row.get("secondary_muscle") or [])
            elif "secondary_muscle" in row:
                exercise.secondary_muscle = secondaryMuscle
            else:
                exercise.secondary_muscle = "Non renseigné"

            equipment = row.get("equipment") or "Non renseigné"
            if isinstance(equipment, list):
                exercise.equipment = ", ".join(row.get("equipment") or [])
            elif "equipment" in row:
                exercise.equipment = equipment
            else:
                exercise.equipment = "Non renseigné"

            instructions = row.get("instructions") or "Non renseigné"
            if isinstance(instructions, list):
                exercise.instructions = ", ".join(row.get("instructions") or [])
            elif "instructions" in row:
                exercise.instructions = instructions
            else:
                exercise.instructions = "Non renseigné"

            constraints = row.get("constraints")
            if isinstance(constraints, list):
                exercise.constraints = ", ".join(constraints)
            elif "constraints" in row:
                exercise.constraints = row.get("constraints") or "Non renseigné"
            else:
                exercise.constraints = "Non renseigné"

            session.add(exercise)
        if succesful:
            session.commit()
    except Exception as ex:
        succesful = False
        session.rollback()
        WriteLog(service, LOG_ID, file["name"], str(ex))
    if succesful:
        move_file(service, file["id"], ARCHIVE_ID, addDateToFile(file["name"]))
    else:
        move_file(service, file["id"], ERROR_ID)


def sendFoodToDb(data: pandas.DataFrame, file, session: Session, service: Resource):
    succesful: bool = True

    errorMessage = ""
    field = [
        "name",
        "category",
        "calories",
        "protein",
        "carbohydrates",
        "fat",
        "fiber",
        "sugars",
        "sodium",
        "cholesterol",
    ]

    data, errorMessage = formatDataFrame(data, field)
    if errorMessage != "":
        WriteLog(service, LOG_ID, file["name"], errorMessage)
        move_file(service, file["id"], ERROR_ID)
        return

    data = data.fillna(0)
    try:
        for _, row in data.iterrows():
            food: Food = Food()

            if "name" in row and row.get("name") != 0:
                food.name = row.get("name")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain name attribute or name is misspelled.",
                )
                break

            food.category = row.get("category", "Non renseigné") or "Non renseigné"
            food.calories = row.get("calories", 0)
            food.protein = row.get("protein", 0)
            food.carbohydrates = row.get("carbohydrates", 0)
            food.fat = row.get("fat", 0)
            food.fiber = row.get("fiber", 0)
            food.sugars = row.get("sugars", 0)

            sodium = row.get("sodium", 0)
            if sodium > 32767:
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    food.name + "sodium is above smallint limit",
                )
                succesful = False
                break
            else:
                food.sodium = sodium

            cholesterol = row.get("cholesterol", 0)
            if cholesterol > 32767:
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    food.name + " cholesterol is above smallint limit",
                )
                succesful = False
                break
            else:
                food.cholesterol = cholesterol

            session.add(food)
        if succesful:
            session.commit()
    except Exception as ex:
        succesful = False
        session.rollback()
        WriteLog(service, LOG_ID, file["name"], str(ex))

    if succesful:
        move_file(service, file["id"], ARCHIVE_ID, addDateToFile(file["name"]))
    else:
        move_file(service, file["id"], ERROR_ID)


def sendHealthMetricToDb(
    data: pandas.DataFrame, file, session: Session, service: Resource
):
    succesful: bool = True

    errorMessage = ""
    field = [
        "user_email",
        "date",
        "start_weight",
        "current_weight",
        "avg_bpm",
        "max_bpm",
        "resting_bpm",
        "steps_count",
        "sleep_time",
        "calories_burned",
        "active_minute",
        "workout_type",
    ]

    data, errorMessage = formatDataFrame(data, field)
    if errorMessage != "":
        WriteLog(service, LOG_ID, file["name"], errorMessage)
        move_file(service, file["id"], ERROR_ID)
        return

    data = data.fillna(0)
    if "date" in data:
        data["date"] = pandas.to_datetime(data["date"])

    users = session.query(User.id, User.email).all()

    user_map = {}

    for user in users:
        user_map[user.email] = user.id

    try:
        for _, row in data.iterrows():
            healthMetric: Health_metric = Health_metric()

            email = row.get("user_email")
            if "user_email" in row and email != 0:
                if email in user_map:
                    healthMetric.user_id = user_map[email]
                else:
                    succesful = False
                    WriteLog(service, LOG_ID, file["name"], "no user with that email")
                    break
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain user_email attribute or user_email is misspelled.",
                )
                break

            if "date" in row and row.get("date") != 0:
                healthMetric.date = row.get("date")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain date attribute or date is misspelled.",
                )
                break

            if "start_weight" in row and row.get("start_weight") != 0:
                healthMetric.start_weight = row.get("start_weight")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain start_weight attribute or start_weight is misspelled.",
                )
                break

            if "current_weight" in row and row.get("current_weight") != 0:
                healthMetric.current_weight = row.get("current_weight")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain current_weight attribute or current_weight is misspelled.",
                )
                break

            if "avg_bpm" in row and row.get("avg_bpm") != 0:
                healthMetric.avg_bpm = row.get("avg_bpm")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain avg_bpm attribute or avg_bpm is misspelled.",
                )
                break

            if "max_bpm" in row and row.get("max_bpm") != 0:
                healthMetric.max_bpm = row.get("max_bpm")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain max_bpm attribute or max_bpm is misspelled.",
                )
                break

            if "resting_bpm" in row and row.get("resting_bpm") != 0:
                healthMetric.resting_bpm = row.get("resting_bpm")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain resting_bpm attribute or resting_bpm is misspelled.",
                )
                break

            if "steps_count" in row and row.get("steps_count") != 0:
                healthMetric.steps_count = row.get("steps_count")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain steps_count attribute or steps_count is misspelled.",
                )
                break

            if "sleep_time" in row and row.get("sleep_time") != 0:
                healthMetric.sleep_time = row.get("sleep_time")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain sleep_time attribute or sleep_time is misspelled.",
                )
                break

            if "calories_burned" in row and row.get("calories_burned") != 0:
                healthMetric.calories_burned = row.get("calories_burned")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain calories_burned attribute or calories_burned is misspelled.",
                )
                break

            if "active_minute" in row and row.get("active_minute") != 0:
                healthMetric.active_minute = row.get("active_minute")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain active_minute attribute or active_minute is misspelled.",
                )
                break

            if "workout_type" in row and row.get("workout_type") != 0:
                healthMetric.workout_type = row.get("workout_type")
            else:
                succesful = False
                WriteLog(
                    service,
                    LOG_ID,
                    file["name"],
                    "file does not contain workout_type attribute or workout_type is misspelled.",
                )
                break

            session.add(healthMetric)
        if succesful:
            session.commit()
    except Exception as ex:
        succesful = False
        session.rollback()
        WriteLog(service, LOG_ID, file["name"], str(ex))

    if succesful:
        move_file(service, file["id"], ARCHIVE_ID, addDateToFile(file["name"]))
    else:
        move_file(service, file["id"], ERROR_ID)


def sendUserFoodRelationToDb(
    data: pandas.DataFrame, file, session: Session, service: Resource
):
    succesful: bool = True

    errorMessage = ""
    field = ["email", "food_name"]

    data, errorMessage = formatDataFrame(data, field)
    if errorMessage != "":
        WriteLog(service, LOG_ID, file["name"], errorMessage)
        move_file(service, file["id"], ERROR_ID)
        return

    try:
        emails: list[Any] = data["email"].tolist()
        foodNames: list[Any] = data["food_name"].tolist()

        users: List[User] = session.query(User).filter(User.email.in_(emails)).all()
        foods: List[Food] = session.query(Food).filter(Food.name.in_(foodNames)).all()

        userMap: dict[Column[str], User] = {u.email: u for u in users}
        foodMap: dict[Column[str], Food] = {f.name: f for f in foods}

        for _, row in data.iterrows():
            consume: Consume = Consume()

            consume.food = foodMap.get(row.get("food_name"))
            consume.user = userMap.get(row.get("email"))

            session.add(consume)

        if succesful:
            session.commit()

    except Exception as ex:
        succesful = False
        session.rollback()
        WriteLog(service, LOG_ID, file["name"], str(ex))
    if succesful:
        move_file(service, file["id"], ARCHIVE_ID, addDateToFile(file["name"]))
    else:
        move_file(service, file["id"], ERROR_ID)


def sendUserExerciseRelationToDb(
    data: pandas.DataFrame, file, session: Session, service: Resource
):
    succesful: bool = True

    errorMessage = ""
    field = ["email", "exercise_name"]

    data, errorMessage = formatDataFrame(data, field)
    if errorMessage != "":
        WriteLog(service, LOG_ID, file["name"], errorMessage)
        move_file(service, file["id"], ERROR_ID)
        return

    try:
        emails: list[Any] = data["email"].tolist()
        exerciseNames: list[Any] = data["exercise_name"].tolist()

        users: List[User] = session.query(User).filter(User.email.in_(emails)).all()
        exercises: List[Exercise] = (
            session.query(Exercise).filter(Exercise.name.in_(exerciseNames)).all()
        )

        userMap: dict[Column[str], User] = {u.email: u for u in users}
        exerciseMap: dict[Column[str], Exercise] = {e.name: e for e in exercises}

        for _, row in data.iterrows():
            practice: Practice = Practice()

            practice.exercise = exerciseMap.get(row.get("exercise_name"))
            practice.user = userMap.get(row.get("email"))

            session.add(practice)

        if succesful:
            session.commit()

    except Exception as ex:
        succesful = False
        session.rollback()
        WriteLog(service, LOG_ID, file["name"], str(ex))
    if succesful:
        move_file(service, file["id"], ARCHIVE_ID, addDateToFile(file["name"]))
    else:
        move_file(service, file["id"], ERROR_ID)


def addDateToFile(file_name: str):
    timestamp = datetime.datetime.now().strftime("%Y_%d_%w_%H_%M_%S")
    return f"{timestamp}_{file_name}"
