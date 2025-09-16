import csv

from fastapi import APIRouter, HTTPException
from routers.auth import  authenticate_user
from pydantic import BaseModel
import datetime

router = APIRouter(prefix="/loan", tags=["Loan"])
cars_list = "db/cars.csv"
class Loans(BaseModel):
    rent_days: int

@router.post("/{car_id}")
def rent_car(email: str, password: str,car_id: int, rent_days: int):
    user = authenticate_user(email, password)
    loan = Loans(rent_days=rent_days)

    if loan.rent_days < 0:
        raise HTTPException(status_code=400, detail="rent_days must be greather than 0")
    updated_rows = []
    car_found = False
    total_price = 0
    rented_car = None

    with open (cars_list, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        for row in reader:
            if int(row["id"]) == car_id:
                car_found = True
                if row["available"].lower() != "true":
                    raise HTTPException(status_code=404, detail="Car is already rented")

                price_per_day = float(row["price_per_day_usd"])
                total_price = price_per_day * loan.rent_days
                row["available"] = "False"
                rented_car = row
            updated_rows.append(row)
    if not car_found:
        raise HTTPException(status_code=404, detail="Car is not found")

    with open (cars_list, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)
    loans_file =  "db/loans.csv"
    loan_id = 1
    existing_loans = []

    try:
        with open(loans_file, "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                existing_loans.append(row)
        loan_id = len(existing_loans) + 1
    except FileNotFoundError:
        pass

    with open (loans_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if len(existing_loans) == 0:
            writer.writerow(["loan_id", "car_id", "date"])
        writer.writerow([loan_id, car_id, datetime.date.today().isoformat()])


    return {
        "message": f"Car with ID {car_id} has been rented for {rent_days} days.",
        "car": rented_car,
        "total_price_usd": total_price}

@router.put("/{car_id}/return")
def return_car(email: str, password: str, car_id: int):
    user = authenticate_user(email, password)
    rows = []
    car_found = False
    returned_car = None

    with open (cars_list, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        for row in reader:
            if int(row["id"]) == car_id:
                car_found = True
                if row["available"].lower() == "true":
                    raise HTTPException(status_code=400, detail="Car is not currently rented")
                row["available"] = "True"
                returned_car = row
            rows.append(row)
    if not car_found:
        raise HTTPException(status_code=404, detail="Car is not found")
    with open (cars_list, "w", newline="") as csvfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return {"message": f"Car with id {car_id} has been returned.",
            "car": returned_car}














