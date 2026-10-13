#!/usr/bin/env python3
"""
CLI инструмент для скачивания сферических 360° панорам Яндекс Карт в максимальном качестве.
Поддерживает ссылки на Яндекс Карты, координаты (lat, lon) и ID панорам.
"""

import sys
import os

# Автоматическое переключение на проектный .venv при необходимости
try:
    from streetlevel import yandex
except ImportError:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_py = os.path.abspath(os.path.join(script_dir, "..", ".venv", "bin", "python3"))
    if os.path.exists(venv_py) and sys.executable != venv_py:
        os.execv(venv_py, [venv_py] + sys.argv)
    else:
        print("Ошибка: библиотека streetlevel не найдена.")
        print("Установите зависимости командой:")
        print("  pip install streetlevel pyexiv2 pillow requests aiohttp")
        sys.exit(1)

import re
import time
import asyncio
import argparse
import urllib.parse
from aiohttp import ClientSession


def parse_input(target: str):
    """
    Парсит переданную строку (URL, ID панорамы или координаты).
    """
    target = target.strip()
    
    # 1. Если это URL Яндекс Карт
    if "yandex" in target or "maps" in target or target.startswith("http"):
        parsed = urllib.parse.urlparse(target)
        params = urllib.parse.parse_qs(parsed.query)
        
        pano_id = params.get("panorama[id]", [None])[0]
        point = params.get("panorama[point]", [None])[0]
        ll = params.get("ll", [None])[0]
        
        lat = None
        lon = None
        coords_str = point or ll
        if coords_str:
            parts = coords_str.split(",")
            if len(parts) == 2:
                try:
                    lon = float(parts[0])
                    lat = float(parts[1])
                except ValueError:
                    pass
                    
        return {"id": pano_id, "lat": lat, "lon": lon, "raw": target}

    # 2. Если переданы координаты вида "lat, lon" или "lat,lon"
    coord_match = re.match(r"^([+-]?\d+(?:\.\d+)?)[,\s]+([+-]?\d+(?:\.\d+)?)$", target)
    if coord_match:
        val1 = float(coord_match.group(1))
        val2 = float(coord_match.group(2))
        # Обычно широта (lat) в России ~ 40-75, долгота (lon) ~ 20-180
        # Если первый аргумент явно больше второго и > 80, скорее всего это lon, lat
        if val1 > 75 and val2 < 75:
            lon, lat = val1, val2
        else:
            lat, lon = val1, val2
        return {"id": None, "lat": lat, "lon": lon, "raw": target}

    # 3. Иначе считаем это ID панорамы
    return {"id": target, "lat": None, "lon": None, "raw": target}


async def download_one(target_str: str, output_path: str = None, zoom: int = 0, session: ClientSession = None):
    info = parse_input(target_str)
    
    pano = None
    if info["id"]:
        try:
            pano = yandex.find_panorama_by_id(info["id"])
        except Exception as e:
            pass
            
    if pano is None and info["lat"] is not None and info["lon"] is not None:
        try:
            pano = yandex.find_panorama(info["lat"], info["lon"])
        except Exception as e:
            print(f"❌ Ошибка поиска по координатам: {e}")
            return False

    if pano is None:
        print(f"❌ Панорама не найдена для: {target_str}")
        return False

    available_sizes = pano.image_sizes or []
    if not available_sizes:
        print(f"❌ Нет доступных размеров изображения для панорамы {pano.id}")
        return False

    actual_zoom = max(0, min(zoom, len(available_sizes) - 1))
    size = available_sizes[actual_zoom]
    
    print(f"\n📸 Найдена панорама:")
    print(f"  • ID: {pano.id}")
    print(f"  • Координаты: {pano.lat:.6f}, {pano.lon:.6f}")
    print(f"  • Разрешение: {size.x} × {size.y} px (zoom {actual_zoom} из {len(available_sizes)-1})")
    print(f"  • Дата съёмки: {pano.date}")
    if pano.author:
        print(f"  • Автор: {pano.author}")

    if not output_path:
        output_path = f"panorama_{pano.id}.jpg"
    elif os.path.isdir(output_path):
        output_path = os.path.join(output_path, f"panorama_{pano.id}.jpg")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    print(f"  ⬇️ Скачивание тайлов в '{output_path}'...")
    t0 = time.time()
    
    close_session = False
    if session is None:
        session = ClientSession()
        close_session = True
        
    try:
        await yandex.download_panorama_async(pano, output_path, session, zoom=actual_zoom)
        filesize_mb = os.path.getsize(output_path) / (1024 * 1024)
        duration = time.time() - t0
        print(f"  ✅ Успешно сохранено: {output_path} ({filesize_mb:.2f} MB, {duration:.1f} сек)")
        return True
    except Exception as e:
        print(f"  ❌ Ошибка загрузки: {e}")
        return False
    finally:
        if close_session:
            await session.close()


async def main_async():
    parser = argparse.ArgumentParser(
        description="Загрузчик 360° эквидистантных панорам Яндекс Карт в максимальном качестве."
    )
    parser.add_argument(
        "targets",
        nargs="+",
        help="Ссылка на Яндекс Карты, ID панорамы или координаты 'lat,lon'"
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Путь к выходному файлу или директории (по умолчанию: panorama_<id>.jpg в текущей папке)"
    )
    parser.add_argument(
        "-z", "--zoom",
        type=int,
        default=0,
        help="Уровень приближения/качества: 0 = максимальное исходное качество (по умолчанию), 1 = высокое (~7K), 2 = среднее (~3.5K)"
    )
    
    args = parser.parse_args()
    
    async with ClientSession() as session:
        for target in args.targets:
            await download_one(target, output_path=args.output, zoom=args.zoom, session=session)


def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\nЗагрузка прервана пользователем.")


if __name__ == "__main__":
    main()
