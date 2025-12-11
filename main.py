from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
import urllib.parse

app = FastAPI(title="CArgo — Агрегатор доставки")

# Статика и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Города
TOP_CITIES = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань"]
CITIES = TOP_CITIES + [
    "Нижний Новгород", "Краснодар", "Самара", "Ростов-на-Дону", "Уфа",
    "Красноярск", "Пермь", "Воронеж", "Волгоград", "Саратов", "Тюмень",
    "Челябинск", "Омск", "Ярославль", "Иркутск", "Владивосток", "Хабаровск"
]

COMPANIES = ["СДЭК", "Boxberry", "Почта России", "Деловые Линии"]


def generate_booking_links(from_city: str, to_city: str, weight: float, declared: int) -> dict:
    """
    Генерация ссылок на калькуляторы перевозчиков.
    Здесь пока без прямых API — ссылки ведут на их формы расчёта.
    """
    fc = urllib.parse.quote(from_city)
    tc = urllib.parse.quote(to_city)
    w_g = int(weight * 1000)

    return {
        "СДЭК": "https://www.cdek.ru/ru/calculate",
        "Boxberry": "https://boxberry.ru/calculate_the_cost_of_sending_a_letter_or_a_parcel",
        "Почта России": f"https://www.pochta.ru/parcels?weight={w_g}&from={fc}&to={tc}",
        "Деловые Линии": "https://www.dellin.ru/requests/"
    }


def calculate_delivery(
    from_c: str,
    to_c: str,
    weight: float,
    declared: int,
    companies: List[str]
) -> List[dict]:
    """
    Эмуляция расчёта стоимости (эвристика).
    Для реальных цен сюда можно будет подставить запросы к API ТК.
    """
    offers: List[dict] = []

    # Коэффициент "расстояния"
    base_dist_coef = 1.0
    if (from_c == "Москва" and to_c == "Санкт-Петербург") or (from_c == "Санкт-Петербург" and to_c == "Москва"):
        base_dist_coef = 0.8
    elif "Владивосток" in [from_c, to_c] or "Хабаровск" in [from_c, to_c]:
        base_dist_coef = 2.5

    # СДЭК
    if "СДЭК" in companies:
        base = 350 * base_dist_coef
        cost = int(base + (weight * 80) + (declared * 0.007))
        offers.append({
            "company": "СДЭК",
            "tariff": "Посылочка (Склад)",
            "price": cost,
            "time": "2-4 дня",
            "badge": "Быстро"
        })

    # Boxberry
    if "Boxberry" in companies:
        base = 290 * base_dist_coef
        cost = int(base + (weight * 70) + (declared * 0.005))
        offers.append({
            "company": "Boxberry",
            "tariff": "Стандарт",
            "price": cost,
            "time": "3-5 дней",
            "badge": "Выгодно"
        })

    # Почта России
    if "Почта России" in companies:
        p_price = int(250 * base_dist_coef + weight * 50)
        offers.append({
            "company": "Почта России",
            "tariff": "Посылка",
            "price": p_price,
            "time": "4-8 дней",
            "badge": None
        })

    # Деловые Линии
    if "Деловые Линии" in companies:
        offers.append({
            "company": "Деловые Линии",
            "tariff": "Авто",
            "price": int(600 * base_dist_coef + weight * 30),
            "time": "3-6 дней",
            "badge": "Крупный груз"
        })

    # Самое дешёвое — первым
    offers.sort(key=lambda x: x["price"])
    return offers


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "cities": sorted(CITIES),
            "companies": COMPANIES,
            "selected_companies": [],
            "from_city": "",
            "to_city": "",
            "weight": 1,
            "declared": 0,
            "offers": [],
            "booking_links": {},
            "error": None,
        },
    )


@app.post("/", response_class=HTMLResponse)
async def calc(
    request: Request,
    from_city: str = Form(...),
    to_city: str = Form(...),
    weight: float = Form(...),
    declared: int = Form(0),
    companies: List[str] = Form(COMPANIES),
):
    error = None
    offers: List[dict] = []
    links: dict = {}

    if from_city == to_city:
        error = "Выберите разные города!"
    else:
        offers = calculate_delivery(from_city, to_city, weight, declared, companies)
        links = generate_booking_links(from_city, to_city, weight, declared)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "cities": sorted(CITIES),
            "companies": COMPANIES,
            "selected_companies": companies,
            "from_city": from_city,
            "to_city": to_city,
            "weight": weight,
            "declared": declared,
            "offers": offers,
            "booking_links": links,
            "error": error,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
