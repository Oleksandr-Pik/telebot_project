import time
import random
import requests


def get_time(text: str):
    current_time = time.localtime()
    output_time = f"{current_time.tm_hour}:{current_time.tm_min}"
    return {"час": output_time}


def get_ramdom_number(text: str):
    return {"число": random.randint(0, 100)}


def get_random_flip(text: str):
    variants = ["орел", "решка"]
    winner = random.choice(variants)
    if winner == "орел":
        return {"сторона_переможець": "орел", "сторона_переможений": "решка"}
    else:
        return {"сторона_переможець": "решка", "сторона_переможений": "орел"}


def get_dollar_curency(text: str):
    result = requests.get(
        "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
    )
    result = result.json()
    total = str(round(float(result[1]["sale"]), 2))
    total = total.split(".")
    return {"курс_грн": total[0], "курс_копійка": total[1]}

