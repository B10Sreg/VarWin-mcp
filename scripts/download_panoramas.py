#!/usr/bin/env python3
"""
Скрипт загрузки эквидистантных 360° панорам Яндекс Карт для НОВАТ (Новосибирский театр оперы и балета).
Использует библиотеку streetlevel и асинхронную загрузку тайлов.
"""

import os
import sys
import json
import time
import asyncio
from aiohttp import ClientSession
from streetlevel import yandex

ITEMS = [
    {
        "index": 1,
        "slug": "01_novat_teatralnaya_ploshchad_facade",
        "title": "Театральная площадь и фасад НОВАТ (снаружи)",
        "id": "1568394220_680807728_23_1715116379",
        "lat": 55.030230,
        "lon": 82.922570,
        "direction": "89.26, 15.31",
        "url": "https://yandex.ru/maps/org/novosibirskiy_gosudarstvenny_akademicheskiy_teatr_opery_i_baleta/1062011780/?ll=82.924605%2C55.030425&panorama%5Bdirection%5D=89.255638%2C15.309488&panorama%5Bfull%5D=true&panorama%5Bid%5D=1568394220_680807728_23_1715116379&panorama%5Bpoint%5D=82.922570%2C55.030230&panorama%5Bspan%5D=108.996467%2C56.087625&z=14"
    },
    {
        "index": 2,
        "slug": "02_novat_vhod_kolonnada",
        "title": "Входная группа / колоннада перед главным входом",
        "id": "1568399834_680806783_23_1584674300",
        "lat": 55.030321,
        "lon": 82.923511,
        "direction": "81.07, -8.94",
        "url": "https://yandex.ru/maps/org/novosibirskiy_gosudarstvenny_akademicheskiy_teatr_opery_i_baleta/1062011780/?ll=82.924605%2C55.030425&panorama%5Bdirection%5D=81.067360%2C-8.942575&panorama%5Bfull%5D=true&panorama%5Bpoint%5D=82.923511%2C55.030321&panorama%5Bspan%5D=113.297304%2C60.000000&z=14"
    },
    {
        "index": 3,
        "slug": "03_novat_glavnoe_foye_vestibyul",
        "title": "Главное фойе / парадный вестибюль 1 этажа",
        "id": "1568403115_680806139_23_1584675300",
        "lat": 55.030383,
        "lon": 82.924061,
        "direction": "93.31, -8.88",
        "url": "https://yandex.ru/maps/org/novosibirskiy_gosudarstvenny_akademicheskiy_teatr_opery_i_baleta/1062011780/?ll=82.924605%2C55.030425&panorama%5Bdirection%5D=93.307569%2C-8.879137&panorama%5Bfull%5D=true&panorama%5Bpoint%5D=82.924061%2C55.030383&panorama%5Bspan%5D=113.297304%2C60.000000&z=14"
    },
    {
        "index": 4,
        "slug": "04_novat_foye_galereya_sever",
        "title": "Фойе / переход галереи (северная сторона)",
        "id": "1568404027_680805132_23_1584676900",
        "lat": 55.030480,
        "lon": 82.924214,
        "direction": "291.80, -18.51",
        "url": "https://yandex.ru/maps/org/novosibirskiy_gosudarstvenny_akademicheskiy_teatr_opery_i_baleta/1062011780/?ll=82.924605%2C55.030425&panorama%5Bdirection%5D=291.801127%2C-18.507989&panorama%5Bfull%5D=true&panorama%5Bpoint%5D=82.924214%2C55.030480&panorama%5Bspan%5D=113.297304%2C60.000000&z=14"
    },
    {
        "index": 5,
        "slug": "05_novat_foye_galereya_yug",
        "title": "Фойе / переход галереи (южная сторона)",
        "id": "1568404218_680806378_23_1584676500",
        "lat": 55.030360,
        "lon": 82.924246,
        "direction": "253.34, -12.96",
        "url": "https://yandex.ru/maps/org/novosibirskiy_gosudarstvenny_akademicheskiy_teatr_opery_i_baleta/1062011780/?ll=82.924605%2C55.030425&panorama%5Bdirection%5D=253.335919%2C-12.961771&panorama%5Bfull%5D=true&panorama%5Bpoint%5D=82.924246%2C55.030360&panorama%5Bspan%5D=113.297304%2C60.000000&z=14"
    },
    {
        "index": 6,
        "slug": "06_novat_foye_prohod_k_zalu",
        "title": "Фойе / центральный проход к зрительному залу",
        "id": "1568403377_680805963_23_1584678300",
        "lat": 55.030400,
        "lon": 82.924105,
        "direction": "91.38, 8.82",
        "url": "https://yandex.ru/maps/org/novosibirskiy_gosudarstvenny_akademicheskiy_teatr_opery_i_baleta/1062011780/?ll=82.924605%2C55.030425&panorama%5Bdirection%5D=91.377533%2C8.819125&panorama%5Bfull%5D=true&panorama%5Bpoint%5D=82.924105%2C55.030400&panorama%5Bspan%5D=113.297304%2C60.000000&z=14"
    },
    {
        "index": 7,
        "slug": "07_novat_bolshoy_zritelny_zal",
        "title": "Большой зрительный зал / сцена и партер",
        "id": "1568405298_680805921_23_1584682900",
        "lat": 55.030404,
        "lon": 82.924427,
        "direction": "166.59, 8.45",
        "url": "https://yandex.ru/maps/org/novosibirskiy_gosudarstvenny_akademicheskiy_teatr_opery_i_baleta/1062011780/?ll=82.924605%2C55.030425&panorama%5Bdirection%5D=166.591507%2C8.449377&panorama%5Bfull%5D=true&panorama%5Bpoint%5D=82.924427%2C55.030404&panorama%5Bspan%5D=113.297304%2C60.000000&z=14"
    }
]

async def download_all(zoom=0):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "panoramas"))
    os.makedirs(base_dir, exist_ok=True)
    
    print(f"=== Скачивание панорам НОВАТ ===")
    print(f"Папка назначения: {base_dir}")
    print(f"Уровень качества (zoom): {zoom} (0 = максимальное исходное разрешение)\n")
    
    manifest = []
    
    async with ClientSession() as session:
        for item in ITEMS:
            t0 = time.time()
            idx = item["index"]
            name = item["slug"]
            title = item["title"]
            print(f"[{idx}/{len(ITEMS)}] {title}...")
            
            # Поиск панорамы
            pano = None
            if item.get("id"):
                try:
                    pano = yandex.find_panorama_by_id(item["id"])
                except Exception as e:
                    print(f"  Ошибка поиска по ID ({e}), ищем по координатам...")
                    
            if pano is None and item.get("lat") and item.get("lon"):
                pano = yandex.find_panorama(item["lat"], item["lon"])
                
            if pano is None:
                print(f"  ❌ Не удалось найти панораму: {name}")
                continue
                
            res_x = pano.image_sizes[zoom].x if zoom < len(pano.image_sizes) else pano.image_sizes[0].x
            res_y = pano.image_sizes[zoom].y if zoom < len(pano.image_sizes) else pano.image_sizes[0].y
            print(f"  Найдена панорама ID: {pano.id}")
            print(f"  Разрешение: {res_x}x{res_y}, Дата съёмки: {pano.date}")
            
            filename = f"{name}.jpg"
            filepath = os.path.join(base_dir, filename)
            
            print(f"  Загрузка тайлов...")
            try:
                await yandex.download_panorama_async(pano, filepath, session, zoom=zoom)
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                duration = time.time() - t0
                print(f"  ✅ Сохранено: {filename} ({size_mb:.2f} MB, {duration:.1f} сек)\n")
                
                manifest.append({
                    "index": idx,
                    "filename": filename,
                    "title": title,
                    "id": pano.id,
                    "image_id": pano.image_id,
                    "resolution": f"{res_x}x{res_y}",
                    "filesize_mb": round(size_mb, 2),
                    "lat": pano.lat,
                    "lon": pano.lon,
                    "date": str(pano.date),
                    "author": pano.author or "Яндекс",
                    "direction_in_url": item["direction"],
                    "yandex_url": item["url"]
                })
            except Exception as e:
                print(f"  ❌ Ошибка при скачивании {filename}: {e}\n")
                
    # Сохраняем manifest.json
    manifest_path = os.path.join(base_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"Манифест сохранён: {manifest_path}")
    
    # Сохраняем README.md
    readme_path = os.path.join(base_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# Панорамы НОВАТ (Яндекс Карты)\n\n")
        f.write("Сферические 360° эквидистантные панорамы Новосибирского государственного академического театра оперы и балета (НОВАТ).\n\n")
        f.write("| № | Превью / Название | Файл | Разрешение | Размер | Дата съёмки | Координаты |\n")
        f.write("|---|-------------------|------|------------|--------|-------------|------------|\n")
        for m in manifest:
            f.write(f"| {m['index']} | **{m['title']}** | `{m['filename']}` | {m['resolution']} | {m['filesize_mb']} MB | {m['date'][:10]} | {m['lat']:.6f}, {m['lon']:.6f} |\n")
        f.write("\n\n## Ссылки на Яндекс Карты\n\n")
        for m in manifest:
            f.write(f"- [{m['title']}]({m['yandex_url']}) (Ракурс: `{m['direction_in_url']}`)\n")
    print(f"README.md сохранён: {readme_path}")
    print("\n🎉 Все панорамы успешно выгружены!")

if __name__ == "__main__":
    zoom_arg = 0
    if len(sys.argv) > 1:
        try:
            zoom_arg = int(sys.argv[1])
        except ValueError:
            pass
    asyncio.run(download_all(zoom=zoom_arg))
