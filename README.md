# ZAURAN AI CREATIVE

Набор скиллов для Claude Code (и совместимых агентов с поддержкой `SKILL.md`), который ведёт AI-видео и AI-картинку от идеи до готового файла. Два скилла в одном репо, общие модули драматургии, одна цепочка передачи.

```text
идея → вселенная → герои → сценарий → шот-лист → VO   |   модель → промт → генерация → QA → выдача
└──────────────── zauran-story-engine ────────────────┘   └──────────── zauran-ai-creative ────────────┘
                                          handoff-пакет →
```

| Скилл | Папка | Что делает | Где заканчивается |
|---|---|---|---|
| **zauran-story-engine** | [`zauran-story-engine/`](zauran-story-engine/README.md) | Идея → инсайт → логлайн → `CANON.md` (вселенная) → паспорта героев → каркас и биты с таймингом → сцены (Goal / Obstacle / Tactic / Reversal / Value Shift) → шот-сценарий 1–3 с → диалог и VO без AI-slop. Серия эпизодов ведётся по хронологии из `STATE.md` / `TIMELINE.md` в папках, которые указывает пользователь. | На утверждённом сценарном пакете. Промты не пишет, модель не выбирает. |
| **zauran-ai-creative** | корень репо ([`SKILL.md`](SKILL.md)) | Бриф → гейт выбора модели и среды → креативное направление → раскадровка → промт под конкретную модель → генерация → проверка результата → выдача → запись выводов. | На готовом файле, проверенном по brief lock. |

Один человекочитаемый `READOUT_<проект>_vN.pdf` на выдачу собирается общим скриптом (`zauran-story-engine/scripts/build-readout.py`); `.md` остаются рабочими файлами для ИИ.

---

## zauran-story-engine

Сценарный движок. Подробно — [`zauran-story-engine/README.md`](zauran-story-engine/README.md).

- **STORY LOCK** + для серии **SERIES SCALE** (движок формата, оси вариативности, ≥5 локаций, типы хуков 0–2 с) — `references/story-routes.md`, `short-form-series.md`.
- **CANON.md** — правила мира (LOCKED / FLEX), локации, продукт, язык; **PASSPORT_<имя>.md** — визуальные инварианты + want/need/рана/тактики/речь.
- **Структура** — шесть каркасов с таймингами 15/30/60 с (Story Spine, Sparkline, Freytag, Monroe, Pixar rules, Hero's Journey), бюджет шотов 6/15/30/60 с, бит-лист.
- **Сцены** через `tig-scene-engine` с causal audit; **шот-сценарий** `SCRIPT_vN.md` с камерой из словаря, светом, инвариантами; **VO/диалог** с анти-slop lint RU/UA/EN.
- **Хранилище на диске** — `STATE.md`, `TIMELINE.md`, реестр путей, протокол продолжения серии (новая серия стартует из состояния прошлой, не с чистого листа).
- **Словарь** — ≈100 кино-терминов (движение камеры, крупность, ракурс, оптика, свет, композиция) с поиском `node zauran-story-engine/scripts/search-shot-vocabulary.mjs --query "orbit"`.
- **Handoff** — пакет `STORY_LOCK / STATE / CANON / PASSPORT / BEATS / SCRIPT / VO / REFERENCES` для производственного скилла.

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

**Правила выдачи промта** — всегда полный цельный промт; реестр требований `R1, R2, …` (`active | removed`); пересборка без потерь с отчётом «добавлено / изменено / удалено / без изменений»; версии в `PROMPT_vN.md`, каждая итерация начинается с чтения файла, не с памяти чата.

---

## Структура репо

```text
SKILL.md                      # zauran-ai-creative — точка входа, оркестрация производства
README.md
agents/openai.yaml
references/
  knowledge-routing.md        # что читать под какой тип задачи
  intake-and-brief.md         # бриф, гейт модели и среды
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

Чистый Node / Python, без установки зависимостей. У каждого есть `--help`.

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

Тесты: `node --test tests/<файл>.test.mjs` (на Windows — по файлам, не директорией).

## Установка

```bash
git clone https://github.com/ZAURAN/ZAURAN-AI-CREATIVE.git ~/.claude/skills/zauran-ai-creative
```

Второй скилл нужно подключить ссылкой на его папку (Claude Code ищет `SKILL.md` в `~/.claude/skills/<имя>/`):

```powershell
# Windows
cmd /c mklink /J "$env:USERPROFILE\.claude\skills\zauran-story-engine" "$env:USERPROFILE\.claude\skills\zauran-ai-creative\zauran-story-engine"
```

```bash
# macOS / Linux
ln -s ~/.claude/skills/zauran-ai-creative/zauran-story-engine ~/.claude/skills/zauran-story-engine
```

Перезапустить Claude Code. Вызов: `/zauran-story-engine …` для сценария, `/zauran-ai-creative …` для промта и генерации — или просто задача словами, скиллы триггерятся по описанию.

Внешние базы заметок не нужны — оба скилла самодостаточны. Личные папки подключаются, только если назвать их в чате.

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
