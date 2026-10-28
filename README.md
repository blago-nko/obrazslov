# Образ слов

База знаний экосистемы blago-nko.

## Статус

Пилотный сайт миграции с Blogger на Hugo (INFRA-047, MIG-002).

Этапы 1 (критичные исправления), 3 (производительность) и 4 (доступность) завершены успешно.
Поиск Pagefind работает для `.html` URL.
Мобильная панель адаптируется под ориентацию экрана.

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

```bash
hugo server -D
```

Откройте http://localhost:1313

## Деплой

Автоматический через GitHub Actions при push в main → GitHub Pages.

## Лицензии

- Код (конфиги, скрипты) — AGPLv3, см. LICENSE
- Контент (статьи, изображения) — CC BY-NC 4.0, см. LICENSE-CONTENT

## Связанные репозитории

- [blago-nko/manifests](https://github.com/blago-nko/manifests) — реестр манифестов и задач
- [blago-nko/shared-assets](https://github.com/blago-nko/shared-assets) — общая тема и компоненты

## ⚠️ Архитектурное решение: Pagefind Glob Override

В общей теме `shared-assets` задокументировано решение INFRA-097 использовать `glob: "**/index.html"` для сайтов с Hugo pretty-URLs.

Однако в репозитории `obrazslov` специально сохранены старые Blogger-URL вида `.html`:

```toml
[permalinks]
posts = "/:year/:month/:filename.html"
```

Поэтому для корректной индексации поиска в этом пилоте используется site-level override в `pagefind.yml`:

```yaml
glob: "**/*.html"
```

**Правило для агентов:** Не менять этот glob обратно на `**/index.html` без предварительного перехода всего сайта на pretty-URLs и настройки редиректов со старых `.html` ссылок. Это сломает миграционные ссылки.
