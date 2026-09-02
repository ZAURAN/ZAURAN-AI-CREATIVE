# zauran-ai-creative

Скилл для Claude Code (и совместимых агентов с поддержкой `SKILL.md`), который ведёт креативную AI-задачу от идеи до готового файла: бриф → выбор модели → креативное направление → раскадровка → промт → генерация → проверка → выдача → запись выводов в Obsidian.

Не «генератор промтов», а оркестратор всего производственного цикла. Останавливается на промте только если попросили именно промт.

## Что умеет

**Изображения**
- **Nano Banana Pro** (Gemini 3 Pro Image) — 5-элементная структура промта + библиотека из 70 community-рецептов (`nano-banana-pro/`).
- **GPT Image** (gpt-image-2) — категории/шаблоны, порядок `сцена → субъект → детали → ограничения`, 523 разобранных кейса (`references/gpt-image-2-cases.json`).
- **Seedream 5.0 Pro/Lite** — порядок `субъект → локация → композиция → свет → стиль → ограничения`, формула правки `change only …` + preserve-список.
- **Библиотека YouMind** — 15 373 промта по 10+ категориям (`references/youmind-prompts/`), поиск через скрипт, используется как «донор формы» для промта.

**Видео**
- **Seedance 2.5 / Higgsfield** — один production-ready промт по методам CINEDANCE V4 (оптика, блокинг, физика, свет), Tig's Scene Engine (драматургия), Acting Task (игра), Blocking Map (геометрия нескольких персонажей).
- **Seedance 2.0** (Dreamina, Jimeng, CapCut, Doubao, Ark, BytePlus, fal) — вендоренный пакет `seedance-2.0/`: Director's Read, состояние секвенции, retake-протокол, анти-слоп лексикон, словари ru/zh/ja/ko/es, схемы JSON.
- **MiniMax H3** (Hailuo H3) — аудиовизуальный клип 4–15 с: таймлайн, диалог с lip sync, диегетика, ambience, музыка — в официальном формате полей.
- **Gemini Omni Flash** — клип 3–10 с со звуком, first/last frame, референсы через `<IMAGE_REF_N>`, разговорное редактирование, расширение до 40 с; continuity lock против самонарезки на шоты.

**Общее**
- Идея → концепция (инсайт, аудитория, драматургия, VO, шот-лист).
- Комната/локация → раскадровка с единой геометрией.
- Фото → генерация вариантов / точечная редакция с `LOCKED` и `EDITABLE` зонами.
- Полный цикл: концепция → раскадровка → keyframes → видео → QA → доставка.

## Как работает

1. **Загрузка контекста.** Читает `references/knowledge-routing.md`, чат, вложения, уже созданные файлы. Не переспрашивает то, что и так ясно.
2. **Короткий бриф.** По 1–3 вопроса за раз, с вариантами и рекомендуемым. Обязательные гейты:
   - **модель** — если не названа и не выводится, задаёт один вопрос с вариантами (только нужная группа: изображение или видео), рекомендуемый — первым;
   - **среда генерации** — прямой API / AI Studio, Flow, Magnific/Freepik canvas, fal, Segmind, Runware, веб-интерфейс модели и т. д.
3. **`BRIEF LOCK`** перед дорогой генерацией — компактная фиксация: что делаем, формат, что сохранить, что менять, что запрещено, роли референсов, куда сохранять.
4. **Референсы как контракт.** У каждого — одна роль (композиция / камера / локация / стиль / персонаж / продукт / свет / движение). Для нескольких брендов — `brand-surface contract`. Приоритет при конфликте: последнее указание → brief lock → референс в роли → ранние пожелания.
5. **Промт под конкретную модель** по её reference-файлу. Не грузит все кинематографические модули подряд — только нужные по `cinematic-orchestration.md`.
6. **QA результата, а не намерения.** Открывает картинку/видео, сверяет с brief lock: геометрия, руки/лица, текст/логотипы, continuity, первый/последний кадр, разрешение, путь файла. Не считает задачу готовой, пока файл не существует и не проверен.
7. **Obsidian learning capture.** После реальной генерации пишет: модель, промт/настройки, что сработало, что нет, какую правку подтвердил пользователь.

**Быстрый режим точечной правки** — если пользователь сказал «без проверки / сразу отдай»: один запуск, никакого QA, только сохранить и дать ссылку.

## Правила выдачи промта

- Всегда **полный цельный промт**, готовый к копированию. Никаких «добавь этот блок к предыдущему».
- **Реестр требований** `R1, R2, …` с источником и статусом `active | removed`. Правка дополняет реестр; требование снимается только по явной команде или при физической несовместимости.
- **Пересборка без потерь**: неизменённые блоки переносятся дословно, после каждой правки отчёт «добавлено / изменено / удалено / без изменений».
- **Версии в файле**: `PROMPT_vN.md` (или `PROMPT_<shot>_vN.md`) в папке проекта; каждая итерация начинается с чтения последнего файла, а не с памяти чата.

## Структура

```
SKILL.md                      # точка входа, правила оркестрации
references/
  knowledge-routing.md        # что читать под какой тип задачи
  intake-and-brief.md         # бриф, гейт выбора модели и среды
  photo-and-storyboard.md     # фото, раскадровки, room → storyboard
  video-and-continuity.md     # видео, переходы, continuity
  storyboard-to-video.md      # review board vs clean generation pack
  qa-and-delivery.md          # проверка и выдача
  cinematic-orchestration.md  # маршрутизация CINEDANCE / Tig-модулей
  cinedance-*.md              # оптика, блокинг, физика/свет
  tig-scene-engine.md         # драматургия Goal→Obstacle→Tactic→Reversal→Value Shift
  tig-acting-task.md          # актёрская игра
  tig-blocking-map.md         # многоперсонажный блокинг
  nano-banana-pro.md          # контракт NBP
  gpt-image-2*.md/json        # контракт GPT Image + шаблоны + кейсы
  seedream-5.md               # контракт Seedream 5.0
  seedance-2.5.md             # платформенный контракт Seedance 2.5
  seedance-2.0.md             # маршрут в вендоренный пакет
  minimax-h3.md               # контракт MiniMax H3
  gemini-omni-flash*.md       # контракт Omni Flash: API, аудио, медиа, правка, отказы
  youmind-prompt-library.md   # как пользоваться библиотекой YouMind
  youmind-prompts/            # 15k промтов по категориям (JSON)
nano-banana-pro/              # 70 рецептов (vendored awesome-nanobanana-pro, MIT)
seedance-2.0/                 # vendored seedance-2.0 v6.7.0 (MIT): GUIDE'ы, схемы, evals, примеры
scripts/                      # поиск по библиотекам (Node, без зависимостей)
tests/                        # тесты скриптов
docs/changelog.md
```

## Скрипты

Все — чистый Node, без `npm install`. Нужны, чтобы не грузить многомегабайтные JSON в контекст.

```bash
node scripts/search-nbp-recipes.mjs --query "product photography" --limit 3
node scripts/search-nbp-recipes.mjs --category "Interior Design" --full
node scripts/search-gpt-image-cases.mjs --id 17
node scripts/search-youmind-prompts.mjs --query "neon poster" --category poster-flyer
node scripts/search-youmind-prompts.mjs --categories
node scripts/update-youmind-prompts.mjs   # обновить снапшот YouMind
```

У каждого есть `--help`.

## Установка

Глобально для Claude Code:

```bash
git clone https://github.com/ZAURAN/ZAURAN-AI-CREATIVE.git ~/.claude/skills/zauran-ai-creative
```

Перезапустить Claude Code. Вызов: `/zauran-ai-creative …` или любая просьба про AI-картинку/видео/промт — скилл триггерится по описанию.

Obsidian-заметки для learning capture опциональны; пути настраиваются в `references/knowledge-routing.md`.

## Ограничения

- Скилл **не публикует, не платит, не отправляет** ничего третьим лицам без явного разрешения.
- Если модель или интерфейс не может выполнить требование (например, «4K» словом в промте) — говорит об этом до генерации и предлагает проверяемый маршрут.
- Ничего не додумывает: людей, руки, упаковку, текст, бренды, новую комнату или сюжетный бит — только по основанию из брифа.

## Лицензии вендоренных частей

- `nano-banana-pro/` — [ZeroLu/awesome-nanobanana-pro](https://github.com/ZeroLu/awesome-nanobanana-pro), MIT.
- `seedance-2.0/` — [Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0) v6.7.0, MIT.
- `references/youmind-prompts/` — YouMind-OpenLab, MIT.
- `references/gpt-image-2-cases.json` — MIT, см. `references/gpt-image-2-LICENSE.txt`.

Полные тексты — в `ATTRIBUTION.md` / `LICENSE` внутри соответствующих папок.
