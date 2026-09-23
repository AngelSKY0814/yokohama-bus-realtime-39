import re
import json
import time
import requests
from concurrent.futures import ThreadPoolExecutor

courses = [
{
        "courseId": "0001600664",
        "route": "39系統",
        "destination": "小机駅前経由 横浜駅西口行",
        "direction": "yokohama"
    },
    {
        "courseId": "0001600669",
        "route": "39系統",
        "destination": "小机駅前経由 横浜駅西口行",
        "direction": "yokohama"
    },
{
        "courseId": "0001601079",
        "route": "12系統",
        "destination": "緑車庫前経由 西菅田団地行",
        "direction": "nishisugeta"
    },
{

        "courseId": "0001600429",
        "route": "12系統",
        "destination": "西菅田団地行",
        "direction": "nishisugeta"
    },
{

        "courseId": "0001600290",
        "route": "12系統",
        "destination": "白山中央経由　西菅田団地行",
        "direction": "nishisugeta"
    },
{

        "courseId": "0001600642",
        "route": "12系統",
        "destination": "白山高校行",
        "direction": "hakusan"
    },
{
    "courseId": "0001600633",
    "route": "12系統",
    "destination": "鴨居駅前",
    "direction": "kamoista"
    },
    {
    "courseId": "0001600644",
    "route": "1系統",
    "destination": "緑車庫前",
    "direction": "midori"
    },
{
    "courseId": "0001600593",
    "route": "39系統",
    "destination": "小机駅前経由 緑車庫前行",
    "direction": "up"
    },
    {
        "courseId": "0001600127",
        "route": "39系統",
        "destination": "東本郷町経由 緑車庫前行",
        "direction": "up"
    },
    {
        "courseId": "0001600641",
        "route": "39系統",
        "destination": "小机駅前経由 中山駅前行",
        "direction": "up"
    },
    {
        "courseId": 0001600635",
        "route": "39系統",
        "destination": "小机駅前経由 中山駅前行",
        "direction": "up"
   },
 {
        "courseId": "0001600498",
        "route": "12系統",
        "destination": "鴨居駅前行",
        "direction":"up"
    },
{
        "courseId": "0001600133",
        "route": "12系統",
        "destination": "緑車庫前行",
        "direction":"up"
    },
{
        "courseId": "0001600500",
        "route": "12系統",
        "destination": "白山高校行",
        "direction": "up"
    },
    {
        "courseId": "0001600106",
        "route": "12系統",
        "destination": "白山高校行",
        "direction": "up"
    },
    {
        "courseId": "0001600636",
        "route": "12系統",
        "destination": "中山駅前行",
        "direction": "up"
    },
      {
        "courseId": "0001600637",
        "route": "12系統",
        "destination": "中山駅前行",
        "direction": "up"
    },
{
        "courseId": "0001601086",
        "route": "12系統",
        "destination": "中山駅前行",
        "direction":"up"
    },
{
        "courseId": "0001600646",
        "route": "1系統",
        "destination": "中山駅前行",
        "direction":"up"
    },




]

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "ja-JP,ja;q=0.9"
}

def get_buses(course):
    course_id = course["courseId"]

    url = (
        "https://navi.hamabus.city.yokohama.lg.jp/"
        "koutuu/pc/location/BusOperationResult"
        f"?courseId={course_id}"
    )

    print()
    print("================================")
    print(course["route"])
    print(course["destination"])
    print("courseId:", course_id)
    print("取得中...")
    print("================================")

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )
        response.raise_for_status()

        html = response.text

        print("HTML取得成功")
        print("文字数:", len(html))

    except Exception as e:
        print("取得エラー:", e)
        return []

    pattern = re.compile(
        r'latlng\s*=\s*new\s+navitime\.geo\.LatLng'
        r'\("([^"]+)",\s*"([^"]+)"\)'
        r'.{0,3000}?'
        r'title:\s*"([^"]+)"',
        re.DOTALL
    )

    matches = pattern.findall(html)
    buses = []

    for latitude, longitude, vehicle_id in matches:
        if not vehicle_id.isdigit():
            continue

        bus = {
            "id": vehicle_id,
            "latitude": float(latitude),
            "longitude": float(longitude),
            "route": course["route"],
            "destination": course["destination"],
            "courseId": course_id,
            "direction": course["direction"]
        }

        buses.append(bus)

        print(
            "バス:",
            vehicle_id,
            latitude,
            longitude
        )

    print("見つかったバス:", len(buses), "台")

    return buses

def update_all_buses():
    all_buses = []

    print()
    print("################################")
    print("横浜市営バス情報を更新します")
    print("################################")

    for course in courses:
        buses = get_buses(course)
        all_buses.extend(buses)
        time.sleep(1)

    data = {
        "updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(all_buses),
        "buses": all_buses
    }

    with open(
        "bus_position.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    print()
    print("################################")
    print("JSON保存完了")
    print("バスの合計:", len(all_buses), "台")
    print("################################")

print("横浜市営バス 自動更新システム")
print("停止する場合は Ctrl + C")
print()

update_all_buses()
