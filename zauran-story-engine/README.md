# zauran-story-engine

Сценарный движок для AI-видео. Ведёт историю от идеи до утверждённого пакета: логлайн → вселенная (`CANON.md`) → паспорта героев → структура и биты с таймингом → сцены (Goal / Obstacle / Tactic / Reversal / Value Shift) → шот-сценарий с обоснованным ритмом → диалог и VO → handoff в [`zauran-ai-creative`](../SKILL.md), который уже пишет промты под модели и генерирует.

Режим определяется запросом: быстрый ответ в чате, разработка или производственный пакет. Новая явная правка пользователя обновляет канон. Сохранённые версии не перезаписываются; конфликты требований получают blocked.

Граница: этот скилл **не пишет промпты под модели** и не выбирает модель генерации. После утверждения сценария видео он переходит к плану персонажей, локаций и предметов по [общему протоколу](../references/script-to-assets.md); модельные промпты и генерацию выполняет `zauran-ai-creative`. При запросе «только сценарий» этот переход не навязывается.

## Что внутри

| Файл | Что |
|---|---|
| `SKILL.md` | Инструкция скилла |
| `../references/script-to-assets.md` | Общий план карточек, выбор целей для промптов, стабильные ID, единый STATE и зависимости версий |
| `references/genre-promises.md` | Восемь жанров, тон/формат/аудитория и проверка причинности |
| `references/film-donors-study.md` · `film-scene-studies.md` · `film-speech-studies.md` | Проверенные наблюдения из локальной коллекции; выбранные сцены 17 рабочих фильмов и границы ASR |
| `references/screenwriting-craft.md` | Тема через поступок, выбор героя, поворот сцены, подтекст и проходы редакции; ссылки на изученные источники |
| `references/story-routes.md` | Бриф истории, STORY LOCK, режимы, контрольные точки, инсайт и логлайн, director's review, запреты |
| `references/drama-audiovisual-analysis.md` | Анализ изображения и звука, уровни доказательств, таймкоды и перенос в постановку |
| `references/vertical-drama.md` | Движок драмы, локальный результат эпизода, типы концовок и реестр раскрытий |
| `references/mydrama-study.md` | Что реально изучено на My Drama; каталог и ограниченная выборка эпизодов/тизеров |
| `references/short-form-series.md` | Серия для TikTok/Reels/Shorts: тип связи эпизодов, SERIES SCALE, содержательная вариативность без квот локаций и каста, приёмы удержания как гипотезы |
| `references/story-bible.md` | Шаблон `CANON.md`: утверждённые правила и осознанные ограничения, §3a оси вариативности, локации, персонажи, продукт, язык, таймлайн; LOCKED/FLEX |
| `references/character-passport.md` | Шаблон `PASSPORT_<имя>.md`: визуальные инварианты + want/need/рана/тактики/речь |
| `references/structure-and-beats.md` | Выбор каркаса, бюджет шотов 6/15/30/60 с, бит-лист, тест структуры |
| `references/scene-to-shotlist.md` | Сцена через Scene Engine, шаблон `SCRIPT_vN.md`, «вместо → писать», continuity |
| `references/dialogue-and-vo.md` | VO с режиссурой, правила диалога, анти-slop lint RU/UA/EN, регистры |
| `references/shot-vocabulary.json` | ≈100 кино-терминов с «что делает / когда / сила» (из личной базы Notion) |
| `references/storyboard-templates.md` | Ч/б раскадровка, character turnaround sheet, продукт 7 панелей |
| `references/project-vault.md` | Папка проекта на диске: `STATE.md`, `TIMELINE.md`, эпизоды, версии, протокол продолжения серии по хронологии |
| `references/human-readout.md` | Один `READOUT_<проект>_vN.pdf` для человека/клиента; .md — для ИИ; сборка `scripts/build-readout.py` |
| `references/handoff-to-production.md` | Пакет файлов и контракт ролей референсов для производственного скилла |
| `references/learning-loop.md` | Журнал `NOTES.md` и предложения улучшений |
| `references/donors/storytelling-frameworks.md` | Story Spine, Sparkline, Freytag, Monroe, Pixar rules, Hero's Journey с таймингами (CC BY 4.0, Serge Shima) |
| `scripts/search-shot-vocabulary.mjs` | Поиск по словарю |

```bash
node scripts/search-shot-vocabulary.mjs --query "orbit"
node scripts/search-shot-vocabulary.mjs --cat "Свет" --power Сильно
node scripts/search-shot-vocabulary.mjs --cats
node --test tests/search-shot-vocabulary.test.mjs
python -m unittest discover -s tests -p "test_*.py"
```

## Установка

Папка скилла = `zauran-story-engine/` этого репо. Для Claude Code — junction/symlink в `~/.claude/skills/zauran-story-engine`:

```powershell
cmd /c mklink /J "$env:USERPROFILE\.claude\skills\zauran-story-engine" "$env:USERPROFILE\.claude\skills\zauran-ai-creative\zauran-story-engine"
```

Модули драматургии (`tig-scene-engine`, `tig-acting-task`, `tig-blocking-map`) живут в `../references/` соседнего скилла. Если пакет отсутствует, доступны компактные проверки в scene-to-shotlist и screenwriting-craft.

PDF-сборщик требует Python с markdown и Chrome/Edge/Chromium; поддерживает --browser и --timeout. Выводит текст и таблицы; изображения заменяет подписями. Существующий PDF не перезаписывается.

## Лицензии доноров

См. `references/donors/LICENSES.md`.
