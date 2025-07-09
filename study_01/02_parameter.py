from fastapi import FastAPI, Query 
 
app = FastAPI() 

# 1) 사용자 조회: Path Parameter
"""
사용자 ID를 Path 변수로 받아 그대로 반환

- 테스트
$ curl http://127.0.0.1:8000/user/10
예상 → {"user_id": 10}
"""
@app.get("/user/{user_id}")
def read_user(user_id: int):
  return {"user_id": user_id}


# 2) 검색: Query Parameter
"""
검색어(keyword)와 결과 개수(limit)를 쿼리로 받아 응답

- 테스트
$ curl "http://127.0.0.1:8000/search?keyword=fastapi&limit=2"
예상 → {"keyword":"fastapi","limit":2}
"""
@app.get("/search")
def search(keyword: str, limit: int = 10):
  return {"keyword": keyword, "limit": limit}


# 3) 카테고리 + 정렬: Path + Query 혼합
"""
카테고리와 정렬 조건을 함께 처리

- 테스트
$ curl "http://127.0.0.1:8000/items/toys?sort=popular"
예상 → {"category":"toys","sort":"popular"}
"""
@app.get("/items/{category}")
def get_items(category: str, sort: str = "recent"):
  return {"category": category, "sort": sort}


# 4) 숫자 제곱: 과제 1번
"""
숫자를 Path로 받아 제곱값 반환

- 테스트
$ curl http://127.0.0.1:8000/square/7
 예상 → {"input":7,"square":49}
"""
@app.get("/square/{input}")
def get_square(number: int):
  result = number ** 2
  return {"input": number, "square": result}


# 5) 날씨: 과제 2번
"""
도시와 단위를 Query로 받아 임의 온도 반환

- 테스트
$ curl "http://127.0.0.1:8000/weather?city=Seoul"
 예상 → {"city":"Seoul","unit":"C","temperature":"25C"}
"""
@app.get("/weather")
def get_temperature(city: str, unit: str = "C"):
  temperature = f"25{unit}"
  return {"city": city, "unit": unit, "temperature": temperature}


# 6) 제품 + 리뷰 여부: 과제 3번
"""
제품 상세 + 리뷰 포함 여부 처리

- 테스트
$ curl "http://127.0.0.1:8000/product/1?review=true"
 예상 → {"id":1,"name":"Test Product","reviews":[...]}
"""
@app.get("/product/{id}")
def get_product(id: int, review: bool = Query(False)):
  product = {"id": id, "name": "Test Product"}
  if review:
    product["reviews"] = ["좋아요", "만족합니다", "추천해요"]
  return product


# 02_parameter2
import math

# 4) 원 넓이·둘레
'''
- 테스트
$ curl "http://127.0.0.1:8000/circle/3"
'''
@app.get("/circle/{radius}")
def circle(radius: float):
  area = math.pi * radius ** 2
  circumference = 2 * math.pi * radius
  return {"radius": radius, "area": round(area, 2), "circumference": round(circumference, 2)}


# 5) 단위 변환 (km ↔ mile)
'''
테스트
$ curl "http://127.0.0.1:8000/convert?value=1&from_unit=km&to_unit=mile"
'''
@app.get("/convert")
def convert(value: int, from_unit: str = "km", to_unit: str = "mile"):
  factor = 0.621371
  
  if from_unit == "km" and to_unit == "mile":
    result = value * factor
  elif from_unit == "mile" and to_unit == "km":
    result = value / factor
  else:
    return {"error": "지원되지 않는 단위"}
  
  return {"input": value, "from": from_unit, "to": to_unit, "result": round(result, 3)}


# 6) 이름 반복 인사
'''
테스트
$ curl "http://127.0.0.1:8000/greet?name=Tom&times=3"
'''
@app.get("/greet")
def greet(name: str = "World", times: int = 1):
  return {"greeting": " ".join([f"Hello, {name}!"] * times)}