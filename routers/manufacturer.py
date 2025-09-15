import csv

from fastapi import APIRouter, HTTPException
from routers.auth import  authenticate_user
from pydantic import BaseModel

router = APIRouter(prefix="/manufacturer", tags=["Manufacturer"])
manu_list = "db/manufacturer.csv"
class Manufacturer(BaseModel):
    name: str
    country: str
    founded_year: str
    global_sales: str

@router.get("")
def read_manufacturer(email: str, password: str):
    user = authenticate_user(email,password)
    with open(manu_list,"r", newline="", encoding="utf-8") as csvfile:
        csv_dict_reader = csv.DictReader(csvfile)
        manufacturers = list(csv_dict_reader)
        for manu in manufacturers:
            manu.pop("id")
        return manufacturers

@router.post("/add")
def add_manufacturer(email: str, password: str, manu: Manufacturer):
    user = authenticate_user(email,password)
    field_names = ["id", "name", "country", "founded_year", "global_sales"]

    with open(manu_list,"r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        manufacturers = list(reader)
        last_id = max(int(row["id"]) for row in manufacturers)

    new_id = last_id + 1

    with open(manu_list,"a", newline="", encoding="utf-8") as csvfile:
        csv_dict_writer = csv.DictWriter(csvfile, fieldnames=field_names, lineterminator="\n")
        csv_dict_writer.writerow({
            "id": new_id,
            "name": manu.name,
            "country": manu.country,
            "founded_year": manu.founded_year,
            "global_sales": manu.global_sales
        })
        return {"message": "Manufacturer added"}

@router.get("/search")
def search_by_manufacturer(email: str, password: str, name: str):
    user = authenticate_user(email,password)
    with open(manu_list,"r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        manufacturers = list(reader)
        for manu in manufacturers:
            manu.pop("id")
    result = [manu for manu in manufacturers if name.lower() in manu["name"].lower()]

    if not result:
        raise HTTPException(status_code=404, detail="Manufacturer not found")

    return result


