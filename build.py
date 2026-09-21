#!/usr/bin/env python3
"""Собирает site/index.html (самостоятельная страница) из index.html (исходник артефакта).

index.html написан для Claude Artifacts: без <!doctype>, <html> и <head> —
платформа оборачивает его сама. Для деплоя оболочку нужно добавить руками.
"""
import io, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "index.html")
OUT = os.path.join(ROOT, "site", "index.html")

DESC = ("План восхождения на Асаму 22 сентября: сомма Куробу, спуск по J-банду в кальдеру "
        "и выход на Маэкакэ-яму — профиль, дедлайны и свет, меняющийся по ходу скролла.")

def main():
    src = io.open(SRC, encoding="utf-8").read()
    src = src.replace('<meta charset="utf-8">\n', '', 1)
    m = re.search(r'<title>(.*?)</title>\n', src)
    if not m:
        raise SystemExit("в index.html не найден <title>")
    title = m.group(1)
    src = src[:m.start()] + src[m.end():]

    head = (
        '<!doctype html>\n<html lang="ru">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<title>%s</title>\n'
        '<meta name="description" content="%s">\n'
        '<meta name="theme-color" content="#0B0D11">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:title" content="%s">\n'
        '<meta property="og:description" content="%s">\n'
        '<meta name="robots" content="noindex">\n'
        '<style>\n'
        '  html{background:#0B0D11;color-scheme:dark}\n'
        '  :root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}\n'
        '  body{margin:0;font:14px system-ui,-apple-system,"Segoe UI",sans-serif}\n'
        '  img{max-width:100%%}\n'
        '  [hidden]{display:none!important}\n'
        '</style>\n</head>\n<body>\n'
    ) % (title, DESC, title, DESC)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(head + src.lstrip("\n") + "\n</body>\n</html>\n")
    print("собрано:", OUT)

if __name__ == "__main__":
    main()
