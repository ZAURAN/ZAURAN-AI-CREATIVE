# ZAURAN AI CREATIVE

Набор скиллов для Claude Code (и совместимых агентов с поддержкой `SKILL.md`), который ведёт AI-видео и AI-картинку от идеи до готового файла. Три скилла в одном репо, общие модули драматургии, одна цепочка передачи.

```text
ТЗ → история и сценарий → план персонажей, локаций и предметов → выбранные промпты → генерация → QA
└── zauran-story-engine ──┘   └──── общий handoff ────┘   └────── zauran-ai-creative ──────┘
```

| Скилл | Папка | Что делает | Где заканчивается |
|---|---|---|---|
| **zauran-story-engine** | [`zauran-story-engine/`](zauran-story-engine/README.md) | Идея → инсайт → логлайн → `CANON.md` (вселенная) → паспорта героев → каркас и биты с таймингом → сцены (Goal / Obstacle / Tactic / Reversal / Value Shift) → шот-сценарий с обоснованным ритмом → диалог и VO без AI-slop. Серия эпизодов ведётся по хронологии из `STATE.md` / `TIMELINE.md` в папках, которые указывает пользователь. | Завершает сценарный этап и предлагает план визуальных материалов. Модельные промпты и генерацию выполняет производственный скилл. |
| **zauran-scene-director** | [`zauran-scene-director/`](zauran-scene-director/SKILL.md) | Готовый сценарий и фото → порядок кадров → камера и блокинг → Blender/3D Jutsu превиз → референсы для видео. | Сохраняет сценарий; передаёт постановку в модельный контракт zauran-ai-creative. |
| **zauran-ai-creative** | корень репо ([`SKILL.md`](SKILL.md)) | Готовый сценарий или бриф → план карточек и выбор элементов → гейт модели/среды перед промптами → креативное направление → раскадровка → промт под конкретную модель → генерация → проверка результата → выдача → запись выводов. | На готовом файле, проверенном по brief lock. |

Для производственного пакета или явного запроса PDF один человекочитаемый `READOUT_<проект>_vN.pdf` собирается общим скриптом (`zauran-story-engine/scripts/build-readout.py`). Короткие ответы, локальная разбивка и только промпт не требуют PDF; уже выбранный режим выдачи сохраняется до новой команды.

Передача между сценарным и производственным скиллами описана в [общем договоре](references/story-production-contract.md): исходное требование → постановка → промпт/монтаж → проверенный результат. Конфликт не отменяет требование; готовность промпта и проверка видео учитываются отдельно. В сохранённом проекте используется один живой STATE и единая таблица соответствия.

---

## zauran-scene-director

Постановка по существующему сценарию: отдельные роли персонажей, камеры, простые 3D-модели, анимация и чистые референсы для видеогенератора. Порядок показа следует сценарию; порядок производства учитывает зависимости. Готовые фотографии находятся через реестр проекта.

Скилл доступен в [`zauran-scene-director/SKILL.md`](zauran-scene-director/SKILL.md). Чтобы клиент обнаружил его отдельно, добавьте папку `zauran-scene-director` в свой каталог скиллов (копией или символической ссылкой). Для переносимой связки сохраните доступность двух соседних скиллов по их именам. Blender и MCP устанавливаются отдельно.

Пример вызова:

> `$zauran-scene-director Подготовь первый кадр сценария в Blender: камера, персонажи, простые модели и готовые фото для Seedance.`

Модуль Blender описывает прямую работу через bpy и MCP; модуль 3D Jutsu отделяет проверенные возможности от неподтверждённых шагов видеоурока. Запрос промпта не запускает платные генерации.

---

## zauran-story-engine

Сценарный движок. Подробно — [`zauran-story-engine/README.md`](zauran-story-engine/README.md).

- **Книжные инструменты** — [67 рабочих карточек](zauran-story-engine/references/book-methods.md) по Труби, Макки, Эгри и Снайдеру: применение, ограничения, оригинальные примеры и глава-источник. Авторские положения отделены от адаптации к коротким сериалам; 22 или 15 этапов не навязываются каждому выпуску. Оба предоставленных источника Макки — ознакомительные фрагменты.
- **STORY LOCK** + для серии **SERIES SCALE** (движок формата, содержательные оси вариативности без квот локаций и каста) — `references/story-routes.md`, `short-form-series.md`.
- **CANON.md** — правила мира (LOCKED / FLEX), локации, продукт, язык; **PASSPORT_<имя>.md** — визуальные инварианты + want/need/рана/тактики/речь.
- **Структура** — шесть каркасов с таймингами 15/30/60 с (Story Spine, Sparkline, Freytag, Monroe, Pixar rules, Hero's Journey), бюджет шотов 6/15/30/60 с, бит-лист.
- **Сцены** через `tig-scene-engine` с causal audit; **шот-сценарий** `SCRIPT_vN.md` с камерой из словаря, светом, инвариантами; **VO/диалог** с анти-slop lint RU/UA/EN.
- **Хранилище на диске** — `STATE.md`, `TIMELINE.md`, реестр путей, протокол продолжения серии (новая серия стартует из состояния прошлой, не с чистого листа).
- **Словарь** — ≈100 кино-терминов (движение камеры, крупность, ракурс, оптика, свет, композиция) с поиском `node zauran-story-engine/scripts/search-shot-vocabulary.mjs --query "orbit"`.
- **Жанры** — проверки восьми жанров, сценарные и визуальные наблюдения из 17 рабочих фильмов; готовые субтитры и локальный ASR отделены от непрерывного просмотра и зрительской статистики.
- **Handoff** — точные версии `STORY_LOCK / STATE / CANON / PASSPORT / BEATS / SCRIPT / VO / REFERENCES`, затем [общий протокол карточек](references/script-to-assets.md). После утверждения сценария видео скиллы выделяют элементы, переиспользуют референсы, составляют `ASSET_PLAN` / `ASSET_REGISTER` и предлагают, для чего писать промпты. Запрос «только сценарий» сохраняет свою границу; утверждение сценария само по себе не запускает платные генерации.

## zauran-ai-creative

Производственный оркестратор. Не «генератор промтов» — останавливается на промте только если попросили именно промт.

**Изображения**
- **Nano Banana Pro** (Gemini 3 Pro Image) — 5-элементная структура промта + 70 community-рецептов (`nano-banana-pro/`).
- **GPT Image** (gpt-image-2) — категории/шаблоны, порядок `сцена → субъект → детали → ограничения`, 523 кейса.
- **Seedream 5.0 Pro/Lite** — порядок `субъект → локация → композиция → свет → стиль → ограничения`, правка `change only …` + preserve.
- **Библиотека YouMind** — 15 373 промта по 10+ категориям как «донор формы».

**Видео**
- **Seedance 2.5 / Higgsfield** — один production-ready промт по CINEDANCE V4 (оптика, блокинг, физика, свет) + Scene Engine + Acting Task + Blocking Map.
- **Seedance 2.0** (Dreamina, Jimeng, CapCut, Doubao, Ark, BytePlus, fal) — вендоренный пакет `seedance-2.0/`: Director's Read, состояние секвенции, retake-протокол, анти-слоп, словари ru/zh/ja/ko/es.
- **MiniMax H3** (Hailuo H3) — клип 4–15 с: таймлайн, lip sync, диегетика, ambience, музыка в официальных полях.
- **Gemini Omni Flash** — клип 3–10 с со звуком, first/last frame, `<IMAGE_REF_N>`, разговорная правка, расширение до 40 с, continuity lock.

**Как работает**
1. Контекст из `references/knowledge-routing.md`, чата, вложений, файлов проекта.
2. Бриф по 1–3 вопроса; обязательные гейты — **модель** (только нужная группа: изображение или видео, рекомендуемая первой) и **среда генерации** (API / Flow / canvas / fal / веб-интерфейс).
3. **BRIEF LOCK** перед дорогой генерацией.
4. **Референсы как контракт** — одна роль на референс, `@Тег` дословно, brand-surface contract.
5. Промт по reference-файлу конкретной модели; кинематографические модули — только нужные по `cinematic-orchestration.md`.
6. **QA результата, а не намерения** — открыть файл, сверить с brief lock, не считать готовым, пока файл не существует и не проверен.
7. **Learning capture** в `NOTES.md` проекта.

Быстрый режим точечной правки: «без проверки / сразу отдай» → один запуск, без QA, ссылка на файл.

**Правила выдачи промпта** — полный цельный текст; устойчивые ID требований с областью сцены/шота и статусами `active | blocked | removed`. Неразрешённый конфликт допускает только явно обозначенный черновик, не готовый к запуску промпт. Версии в `PROMPT_vN.md`; каждая итерация начинается с чтения файла и сверки исходных требований.

**Локальные книги** — опубликованные карточки работают без полных текстов. Пользовательские PDF/FB2, извлечения и каталог в `zauran-story-engine/library/` не входят в репозиторий и исключены через `.gitignore`. Если локальная библиотека подготовлена, `python zauran-story-engine/scripts/read-book.py --list` показывает источники, а `--book <ID> --section <Sxxx>` читает выбранный раздел. Без библиотеки скилл использует карточки с указанными границами изученного материала.

---

## Структура репо

```text
SKILL.md                      # zauran-ai-creative — точка входа, оркестрация производства
README.md
agents/openai.yaml
references/
  knowledge-routing.md        # что читать под какой тип задачи
  intake-and-brief.md         # бриф, гейт модели и среды
  script-to-assets.md         # общий переход от сценария к карточкам и выбранным промптам
  story-production-contract.md # сохранение требований, режимы выдачи и сквозная сверка
  photo-and-storyboard.md · video-and-continuity.md · storyboard-to-video.md · qa-and-delivery.md
  cinematic-orchestration.md  # маршрутизация CINEDANCE / Tig-модулей
  cinedance-*.md              # оптика, блокинг, физика/свет
  tig-scene-engine.md · tig-acting-task.md · tig-blocking-map.md   # общие для обоих скиллов
  nano-banana-pro.md · gpt-image-2*.md/json · seedream-5.md
  seedance-2.5.md · seedance-2.0.md · minimax-h3.md · gemini-omni-flash*.md
  youmind-prompt-library.md · youmind-prompts/
nano-banana-pro/              # 70 рецептов (vendored, MIT)
seedance-2.0/                 # vendored seedance-2.0 v6.7.0 (MIT)
scripts/ · tests/             # поиск по библиотекам, тесты (Node, без зависимостей)
docs/changelog.md

zauran-story-engine/          # второй скилл
  SKILL.md · README.md · agents/openai.yaml
  references/
    story-routes.md · short-form-series.md · story-bible.md · character-passport.md
    structure-and-beats.md · scene-to-shotlist.md · dialogue-and-vo.md
    project-vault.md · human-readout.md · handoff-to-production.md · learning-loop.md
    storyboard-templates.md · shot-vocabulary.json
    donors/storytelling-frameworks.md · donors/LICENSES.md
  scripts/search-shot-vocabulary.mjs · scripts/build-readout.py
  tests/
```

## Скрипты

Поисковые скрипты используют стандартный Node.js. PDF-сборщик требует Python, пакет `markdown` и Chrome/Edge/Chromium; поддерживает `--browser` и `--timeout`, не перезаписывает готовые PDF. У скриптов есть `--help`.

```bash
# zauran-ai-creative
node scripts/search-nbp-recipes.mjs --query "product photography" --limit 3
node scripts/search-gpt-image-cases.mjs --id 17
node scripts/search-youmind-prompts.mjs --query "neon poster" --category poster-flyer
node scripts/update-youmind-prompts.mjs

# zauran-story-engine
node zauran-story-engine/scripts/search-shot-vocabulary.mjs --query "orbit"
node zauran-story-engine/scripts/search-shot-vocabulary.mjs --cats
python zauran-story-engine/scripts/build-readout.py --help
```

Тесты поиска: `node --test tests/<файл>.test.mjs` (на Windows — по файлам, не директорией). Тесты PDF-сборщика: `python -m unittest discover -s zauran-story-engine/tests -p "test_*.py"`.

## Установка для коллеги и его AI-агента

Отправьте коллеге [ссылку на репозиторий](https://github.com/ZAURAN/ZAURAN-AI-CREATIVE). Он может передать своему агенту этот запрос:

```text
Установи три связанных скилла из https://github.com/ZAURAN/ZAURAN-AI-CREATIVE:
zauran-ai-creative (корень), zauran-story-engine и zauran-scene-director.
Прочитай раздел установки README. Определи каталог скиллов моего клиента,
сохрани структуру репозитория и подключи две вложенные папки как отдельные скиллы.
Не перезаписывай существующие установки и настройки без проверки.
Проверь все три SKILL.md и объясни, как их вызвать.
Blender, MCP и платные сервисы пока не устанавливай и не запускай.
```

### Инструкция агенту-установщику

1. Определи клиент и его фактический каталог скиллов. Для Codex в этой схеме используется `$CODEX_HOME/skills`, при незаданном CODEX_HOME — `~/.codex/skills`; для Claude Code — `~/.claude/skills`. Учитывай явный путь пользователя.
2. Проверь три целевых имени до записи. При существующей установке проверь remote, локальные изменения и цель ссылок. Не удаляй папки и не клонируй поверх них. Обновление существующей установки — отдельный режим ниже.
3. Склонируй весь репозиторий в `<skills>/zauran-ai-creative`. Не скачивай только SKILL.md: нужны references, scripts и вложенные модули.
4. Подключи `<skills>/zauran-story-engine` к `<skills>/zauran-ai-creative/zauran-story-engine`, а `<skills>/zauran-scene-director` — к `<skills>/zauran-ai-creative/zauran-scene-director`. Windows: directory junction; macOS/Linux: symbolic link. Ссылки сохраняют общие относительные зависимости и единую обновляемую копию.
5. Проверь, что по всем трём путям читается SKILL.md и его frontmatter name совпадает с именем скилла. Проверь общие references в корне клона и ресурсы вложенных скиллов. При переходах через `../` разрешай фактическую цель junction/symlink.
6. Предложи проверить доступность скиллов в следующем ходе клиента; если список не обновился — перезапустить клиент. Не объявляй обнаружение клиентом проверенным только по наличию папок.

Получившаяся структура:

```text
<skills>/
  zauran-ai-creative/                 # git clone всего репозитория
    SKILL.md
    references/
    zauran-story-engine/SKILL.md
    zauran-scene-director/SKILL.md
  zauran-story-engine/                # ссылка на вложенную папку
  zauran-scene-director/              # ссылка на вложенную папку
```

### Windows / PowerShell — новая установка

Требуется Git. По умолчанию пример устанавливает в Codex; для Claude Code замените присваивание `$skillsRoot` на `Join-Path $env:USERPROFILE '.claude/skills'`. Выполняйте блок целиком: он останавливается, если хотя бы одно целевое имя уже существует.

```powershell
$ErrorActionPreference = 'Stop'
$skillsRoot = if ($env:CODEX_HOME) {
    Join-Path $env:CODEX_HOME 'skills'
} else {
    Join-Path $env:USERPROFILE '.codex/skills'
}
$skillNames = @('zauran-ai-creative', 'zauran-story-engine', 'zauran-scene-director')
foreach ($name in $skillNames) {
    $target = Join-Path $skillsRoot $name
    if (Get-Item -LiteralPath $target -Force -ErrorAction SilentlyContinue) {
        throw "Уже существует: $target. Сначала проверь текущую установку."
    }
}
New-Item -ItemType Directory -Path $skillsRoot -Force | Out-Null
$repoRoot = Join-Path $skillsRoot 'zauran-ai-creative'
git clone https://github.com/ZAURAN/ZAURAN-AI-CREATIVE.git $repoRoot
if ($LASTEXITCODE -ne 0) { throw 'Git clone завершился с ошибкой.' }
foreach ($name in @('zauran-story-engine', 'zauran-scene-director')) {
    New-Item -ItemType Junction -Path (Join-Path $skillsRoot $name) -Target (Join-Path $repoRoot $name) | Out-Null
}
foreach ($name in $skillNames) {
    $entry = Join-Path (Join-Path $skillsRoot $name) 'SKILL.md'
    if (-not (Test-Path -LiteralPath $entry -PathType Leaf)) { throw "Нет файла: $entry" }
    Write-Output "Установлен: $entry"
}
```

### macOS / Linux — новая установка

Требуется Git. Для Claude Code замените строку `skills_root=...` на `skills_root="$HOME/.claude/skills"`.

```bash
(
set -eu
skills_root="${CODEX_HOME:-$HOME/.codex}/skills"
for name in zauran-ai-creative zauran-story-engine zauran-scene-director; do
    if [ -e "$skills_root/$name" ] || [ -L "$skills_root/$name" ]; then
        echo "Уже существует: $skills_root/$name. Проверь текущую установку." >&2
        exit 1
    fi
done
mkdir -p "$skills_root"
git clone https://github.com/ZAURAN/ZAURAN-AI-CREATIVE.git "$skills_root/zauran-ai-creative"
for name in zauran-story-engine zauran-scene-director; do
    ln -s "$skills_root/zauran-ai-creative/$name" "$skills_root/$name"
    test -f "$skills_root/$name/SKILL.md"
done
test -f "$skills_root/zauran-ai-creative/SKILL.md"
)
```

### Обновление

В папке клона сначала проверь `git remote -v` и `git status --short`. Если это нужный репозиторий и нет локальных изменений, выполни `git pull --ff-only`. При изменениях или расхождении истории сохрани их и разберись с конфликтом; не применяй reset/clean автоматически. Ссылки обновятся вместе с клоном. В старой установке из двух скиллов добавь только недостающую ссылку `zauran-scene-director`, проверив её путь.

### Как пользоваться

В Codex вызывайте скилл через `$имя`, в Claude Code — `/имя`. Можно также описать задачу обычными словами. Примеры для Codex:

```text
$zauran-story-engine Разбери сценарий в папке моего проекта. Содержание не меняй.

$zauran-ai-creative По этому сценарию найди готовые фото и составь список недостающих референсов. Пока только план.

$zauran-scene-director Подготовь первый кадр в Blender: кто где находится, камера, движение и какие фото загрузить в Seedance. Пока только постановка и промпт.

$zauran-scene-director Продолжи со следующего незавершённого кадра по STATE проекта.
```

Укажите папку своего проекта и сценарий при первом обращении. Изображения коллеги, исходный сценарий и состояние проекта не входят в установку скиллов: их нужно предоставить отдельно. Скилл читает доступные файлы, а не получает память чужого чата.

Как связка работает:

1. **Story Engine** фиксирует сценарий, персонажей, события и речь. Готовый клиентский сценарий сохраняется в порученных границах.
2. **AI Creative** находит или готовит лица, костюмы, локации и предметы, ведёт реестр версий фото. Перед модельным промптом использует выбранную модель и среду.
3. **Scene Director** разбивает действия на кадры, определяет роли каждого персонажа, положения, взгляды, контакты, камеру и движения. Порядок показа сохраняет сценарий; подготовка может идти по зависимостям.
4. При запросе 3D-постановки создаётся превиз в Blender или 3D Jutsu. Для финального видео используются подходящие чистые изображения и ролик постановки; подписанная карта не становится стартовым кадром автоматически.
5. Состояние сохраняется в проектном STATE и связанных производственных файлах. Команда «что дальше» продолжает этот план. «Напиши промпт» выдаёт текст, «сгенерируй» поручает генерацию в указанном объёме.

### Blender и MCP — отдельно от скиллов

Для сценария и промптов Blender не нужен. Для создания `.blend` нужен установленный Blender; для управления открытой сценой — работающий коннектор, например [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp). Агент может также запускать локальные bpy-скрипты отдельным процессом Blender.

Чтобы подключить MCP, отдельно поручите агенту:

```text
Установи и настрой ahujasid/blender-mcp для моего клиента и Blender.
Проверь текущую официальную инструкцию, сохрани существующие настройки,
подключи аддон и проверь get_scene_info на моей открытой сцене.
Не запускай платные генерации и не закрывай несохранённую сцену.
```

Плагин Higgsfield не обязателен для локального Blender MCP. Подписка на чат не оплачивает внешнюю генерацию Seedance/Higgsfield и других сервисов. Ключи, аккаунты, доступ к моделям и необходимые приложения настраиваются отдельно; установка скиллов их не создаёт и не переносит с компьютера автора.

Внешние базы заметок не нужны. Для поисковых утилит нужен Node.js, для PDF — зависимости из раздела «Скрипты»; они не обязательны для простого ответа в чате.

## Ограничения

- Не публикуют, не платят, не отправляют ничего третьим лицам без явного разрешения.
- Не додумывают героев, руки, упаковку, текст, бренды, локации, сюжетные биты — только по основанию из брифа или плана серии.
- Если модель или интерфейс не может выполнить требование — говорят до генерации и предлагают проверяемый маршрут.

## Лицензии вендоренных частей

- `nano-banana-pro/` — [ZeroLu/awesome-nanobanana-pro](https://github.com/ZeroLu/awesome-nanobanana-pro), MIT.
- `seedance-2.0/` — [Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0) v6.7.0, MIT.
- `references/youmind-prompts/` — YouMind-OpenLab, MIT.
- `references/gpt-image-2-cases.json` — MIT, см. `references/gpt-image-2-LICENSE.txt`.
- `zauran-story-engine/references/donors/storytelling-frameworks.md` — Serge Shima, [smixs/creative-director-skill](https://github.com/smixs/creative-director-skill), CC BY 4.0.

Полные тексты — в `ATTRIBUTION.md` / `LICENSE` / `donors/LICENSES.md` внутри соответствующих папок.
