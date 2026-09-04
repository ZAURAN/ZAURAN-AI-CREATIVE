# zauran-story-engine

Сценарный движок для AI-видео. Ведёт историю от идеи до утверждённого пакета: логлайн → вселенная (`CANON.md`) → паспорта героев → структура и биты с таймингом → сцены (Goal / Obstacle / Tactic / Reversal / Value Shift) → шот-сценарий 1–3 с → диалог и VO → handoff в [`zauran-ai-creative`](../SKILL.md), который уже пишет промты под модели и генерирует.

Граница: этот скилл **не пишет промты под модели** и не выбирает модель. Он заканчивается на сценарии.

## Что внутри

| Файл | Что |
|---|---|
| `SKILL.md` | Инструкция скилла |
| `references/story-routes.md` | Бриф истории, STORY LOCK, режимы, контрольные точки, инсайт и логлайн, director's review, запреты |
| `references/short-form-series.md` | Серия для TikTok/Reels/Shorts: движок формата vs декорация, SERIES SCALE (оси вариативности, 10 эпизодов, ≥5 локаций), типы хуков 0–2 с, тест серии, рационализации |
| `references/story-bible.md` | Шаблон `CANON.md`: правила мира (не клетка), §3a оси вариативности, локации, персонажи, продукт, язык, таймлайн; LOCKED/FLEX |
| `references/character-passport.md` | Шаблон `PASSPORT_<имя>.md`: визуальные инварианты + want/need/рана/тактики/речь |
| `references/structure-and-beats.md` | Выбор каркаса, бюджет шотов 6/15/30/60 с, бит-лист, тест структуры |
| `references/scene-to-shotlist.md` | Сцена через Scene Engine, шаблон `SCRIPT_vN.md`, «вместо → писать», continuity |
| `references/dialogue-and-vo.md` | VO с режиссурой, правила диалога, анти-slop lint RU/UA/EN, регистры |
| `references/shot-vocabulary.json` | ≈100 кино-терминов с «что делает / когда / сила» (из личной базы Notion) |
| `references/storyboard-templates.md` | Ч/б раскадровка, character turnaround sheet, продукт 7 панелей |
| `references/project-vault.md` | Папка проекта на диске: `STATE.md`, `TIMELINE.md`, эпизоды, версии, протокол продолжения серии по хронологии |
| `references/handoff-to-production.md` | Пакет файлов и контракт ролей референсов для производственного скилла |
| `references/learning-loop.md` | Журнал `NOTES.md` и промоут паттернов |
| `references/donors/storytelling-frameworks.md` | Story Spine, Sparkline, Freytag, Monroe, Pixar rules, Hero's Journey с таймингами (CC BY 4.0, Serge Shima) |
| `scripts/search-shot-vocabulary.mjs` | Поиск по словарю |

```bash
node scripts/search-shot-vocabulary.mjs --query "orbit"
node scripts/search-shot-vocabulary.mjs --cat "Свет" --power Сильно
node scripts/search-shot-vocabulary.mjs --cats
node --test tests/search-shot-vocabulary.test.mjs
```

## Установка

Папка скилла = `zauran-story-engine/` этого репо. Для Claude Code — junction/symlink в `~/.claude/skills/zauran-story-engine`:

```powershell
cmd /c mklink /J "$env:USERPROFILE\.claude\skills\zauran-story-engine" "$env:USERPROFILE\.claude\skills\zauran-ai-creative\zauran-story-engine"
```

Модули драматургии (`tig-scene-engine`, `tig-acting-task`, `tig-blocking-map`) живут в `../references/` соседнего скилла и не дублируются.

## Лицензии доноров

См. `references/donors/LICENSES.md`.
