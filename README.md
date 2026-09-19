# obrazslov.ru

База знаний экосистемы [blago-nko](https://github.com/blago-nko).

## Статус

Пилотный сайт миграции с Blogger на Hugo (INFRA-047, MIG-002).

## Структура

- `content/posts/` — статьи в markdown с YAML front matter
- `static/images/` — локальные изображения (экспортированные из Blogger)
- `static/verification/` — файлы верификации поисковых систем
- `themes/shared-assets/` — общая тема из blago-nko/shared-assets

## Проверка в облаке (staging)

- Адрес: https://blago-nko.github.io/obrazslov/
- Сборка: GitHub Actions, workflow `hugo.yml` (environment=staging, baseURL с префиксом репозитория)
- Защита от индексации: `meta robots noindex, nofollow` (снимается при переходе на боевой домен)
- Статус деплоя: вкладка Actions репозитория

## Локальная разработка

    hugo server -D

Откройте http://localhost:1313

## Деплой

Автоматический через GitHub Actions при push в main → GitHub Pages.

## Лицензии

- Код (конфиги, скрипты) — AGPLv3, см. LICENSE
- Контент (статьи, изображения) — CC BY-NC 4.0, см. LICENSE-CONTENT

## Связанные репозитории

- [blago-nko/manifests](https://github.com/blago-nko/manifests) — реестр манифестов и задач
- [blago-nko/shared-assets](https://github.com/blago-nko/shared-assets) — общая тема и компоненты
