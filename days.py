from enum import Enum
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

neat_days = FastAPI()

neat_days.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class DayOfWeek(Enum):
    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"


def get_day_string(day: DayOfWeek) -> str:
    match day:
        case DayOfWeek.SUNDAY:
            return ("A day of rest")
        case DayOfWeek.MONDAY:
            return ("It's a Monday *in mischevious voice*")
        case DayOfWeek.TUESDAY:
            return ("Eat some TACOOOOOOOSSSSS")
        case DayOfWeek.WEDNESDAY:
            return ("HUMP DAYYEEEEEEE!!")
        case DayOfWeek.THURSDAY:
            return ("Almost the weekend")
        case DayOfWeek.FRIDAY:
            return ("Get dat bonfire roarin'")
        case DayOfWeek.SATURDAY:
            return ("Get that yardwork done")


@neat_days.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# def DayRequest(BaseModel):
    # day: str


@neat_days.post("/day-message/", response_class=HTMLResponse)
async def day_message(request: Request, day: str = Form(...)):
    # day = input("What Day of the Week do you want to see? ").upper()
    day_str = day.upper()
    try:
        day_enum = DayOfWeek[day_str]
        message = get_day_string(day_enum)
        return templates.TemplateResponse("index.html", {"request": request, "message": message})
        # print(get_day_string(day_enum))

    except KeyError:
        error_message = f"{day} is not a valid day of the week."
        return templates.TemplateResponse("index.html", {"request": request, "message": error_message})


if __name__ == "__main__":
    day_message()
