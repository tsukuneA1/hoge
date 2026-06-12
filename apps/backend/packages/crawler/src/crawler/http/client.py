import httpx

form = {
    "ControllerParameters": "JAA103SubCon",
    "nendo": "2026",
    "pYear": "2026",
    "p_number": "2000",
    "p_page": "1",
    "pLng": "jp",
}

files = {key: (None, value) for key, value in form.items()}

r = httpx.post('https://www.wsl.waseda.jp/syllabus/JAA101.php', files=files, timeout=60.0)
print(r.text)