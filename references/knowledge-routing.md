# Маршрутизация базы знаний

## Источник знаний

Навык самодостаточен: все контракты моделей, методы и правила лежат в его reference-файлах. Внешняя база (Obsidian, Notion, папка заметок) **не требуется** и по умолчанию не ищется.

Если пользователь сам явно назвал папку с личными заметками и попросил её учитывать — прочитай оттуда только нужное; последний подтверждённый тест пользователя из такой папки выше общей документации. Если папка не названа — не спрашивай про неё и не сообщай о её отсутствии.

## Что читать

Всегда для нового креативного проекта:

- `references/intake-and-brief.md`

Для генерации или редактирования фото:

- `references/photo-and-storyboard.md`

Дополнительно для Nano Banana Pro (Gemini 3 Pro Image):

- `references/nano-banana-pro.md` — обязательная платформенная инструкция навыка: model ID `gemini-3-pro-image` и отличие от Nano Banana и Nano Banana 2, поля Interactions API (`response_format.aspect_ratio` / `image_size`) против legacy `generationConfig.imageConfig`, соотношения сторон, 1K/2K/4K и цены, лимиты референсов (14 вход, 6 объектов, 5 человек), пять элементов промпта и официальный порядок блоков, контракт текста в кадре, грамматика правки с preserve, grounding через Google Search, thinking, SynthID, preflight, таблица диагностики, список неподтверждённого, плюс маршрут к библиотеке рецептов и десять приёмов, подтверждённых корпусом.
- `nano-banana-pro/recipes.json` — 70 отобранных промтов сообщества (репозиторий `ZeroLu/awesome-nanobanana-pro`, MIT). Работай только через `node scripts/search-nbp-recipes.mjs --help`.
- `nano-banana-pro/AWESOME-NBP.md` — исходный файл на 102 КБ. Целиком не открывать; спонсорские блоки в начале и в конце — реклама, не знание.

Дополнительно для Seedream 5.0 (Pro / Lite):

- `references/seedream-5.md` — обязательная платформенная инструкция навыка: маршруты генерация/редакция/композиция по референсам/текст и верстка, порядок блоков промта, паттерны портрета, product hero, мультисубъектной сцены и иллюстрации, грамматика локальной правки и preserve-списки, роли референсов и identity block, слои, дословный текст, инфографика по утвержденным данным, мультиязычность, диагностика и preflight.

Дополнительно для GPT Image (gpt-image-2):

- `references/gpt-image-2.md` — обязательная платформенная инструкция навыка: 13 категорий задач, индекс 22 шаблонов, порядок блоков промта, контракт текста на изображении, роли референсов, лимиты размеров, антипаттерны по типам задач, preflight и QA.
- `references/gpt-image-2-templates.md` — детальные шаблоны с заполняемыми слотами; читай только нужный заголовок категории.
- `references/gpt-image-2-style-library.md` — краткий индекс шаблонов, таксономия styles/scenes и правила отбора.
- `references/gpt-image-2-cases.json` — корпус 523 кейсов. Не открывай файл целиком; запрашивай через `node scripts/search-gpt-image-cases.mjs --help`.

Дополнительно для подбора проверенного промта-донора (любая модель):

- `references/youmind-prompt-library.md` — маршрутизатор библиотеки YouMind: 11 категорий, структура записи, команды поиска, правила адаптации донора под бриф и платформенный контракт, атрибуция и обновление базы.
- `references/youmind-prompts/*.json` — корпус 15 373 промтов сообщества (~46 МБ). Никогда не открывай файлы целиком; работай только через `node scripts/search-youmind-prompts.mjs --help`. Свежесть — `node scripts/update-youmind-prompts.mjs --check`.

Для видео:

- `references/cinematic-orchestration.md` — обязательный маршрутизатор для сюжетного, персонажного, multi-character или кинематографического видео; связывает Scene Engine, Acting Task, Blocking Map и CINEDANCE с платформенными контрактами Seedance 2.5, Seedance 2.0, MiniMax H3 и Gemini Omni Flash.
- `references/seedance-2.5.md` — обязательная актуальная инструкция для Seedance 2.5: параметры, reference map, 30/180 секунд, timestamps, edit, extension, first/last frames и keyframes.
- `references/minimax-h3.md` — обязательная актуальная инструкция для MiniMax H3 / Hailuo H3: выбор режима T2VA/I2VA/FL2VA/L2VA/Ref2VA, строки выравнивания кадров, поля `integrated_multimodal_description`, `overall_soundscape` и `non_diegetic_music`, словарь камеры, диалог с `(S1)` и `<d>[Russian] ...</d>`, шесть секций Ref2VA и лимиты 4–15 секунд.
- `references/gemini-omni-flash.md` — обязательная актуальная инструкция для Google Gemini Omni Flash (`gemini-omni-1.1-flash`, GA 27.08.2026): выбор режима, пять элементов промпта DeepMind, continuity lock против самовольной нарезки на шоты, негативы формулировкой `No X`, тайминг и таймкод-блоки, мета-промптинг, жесткие лимиты (3–10 секунд строкой `"8s"`, только 16:9 и 9:16, 24 fps, 1080p и 4k это апскейл 720p), preflight, QA и диагностика. Оттуда маршрут по companion-файлам.
- `references/gemini-omni-flash-api.md` — Interactions API: model ID по площадкам, эндпоинты, полное тело запроса, `response_format` и `video_config.task`, части `input`, асинхронность и опрос, Files API, площадки, цены, коды ошибок.
- `references/gemini-omni-flash-media.md` — привязка медиа: теги `<FIRST_FRAME>` / `<LAST_FRAME>` / `<IMAGE_REF_N>` / `<VIDEO_REF_N>`, объявления `[# Sources ...]` и `[# References ...]`, правило нумерации `@ImageN`, интерполяция кадров, референсные видео, консистентность персонажа, сторибординг.
- `references/gemini-omni-flash-audio.md` — звук генерируется всегда и только текстом: диалог и подача, музыка и sync-to-beat, SFX и ambience, негативы, механика `strip-audio` при правке видео со звуком, голоса во Flow, дефект громкости 26 dB.
- `references/gemini-omni-flash-edit-extend.md` — разговорное редактирование (короткий промпт плюс `Keep everything else the same.`), два маршрута правки, расширение шагами по 10 секунд до 40, все ограничения расширения, экономика итераций.
- `references/gemini-omni-flash-vocabulary.md` — десять собственных терминов камеры Omni и полная общая таксономия Vertex (ракурсы, движения, оптика, свет, тон, стиль, амбиенс, время, монтажные термины), текст в кадре, что нельзя называть, физика, длина промпта.
- `references/gemini-omni-flash-failures.md` — тихий отказ HTTP 200 без видео, блокировки безопасности и подтвержденные обходы, латентность как диагностика, слабости модели, отличия сторонних врапперов, поведение стоимости, список параметров Veo, которых у Omni нет, 13 открытых пробелов и дефекты документации.

Дополнительно для линии Seedance 2.0 и для моделе-независимых режиссёрских методов:

- `references/seedance-2.0.md` — маршрутизатор вендоренного пакета `seedance-2.0/` (внешний `seedance-20` 6.7.0, MIT): граница «2.0 — это не 2.5», условия загрузки, карта 28 под-скиллов и ~60 reference-файлов, список принятых моделе-независимых методов и список того, что из пакета не брать.
- `seedance-2.0/ROOT.md` — вход в сам пакет: operating loop, fast lane, гейты, таблица маршрутизации. Дальше только нужные `seedance-2.0/skills/<имя>/GUIDE.md` и `seedance-2.0/references/*.md`. Пакет целиком не открывать.
- Оттуда же берутся (пути от корня навыка): `seedance-2.0/references/directors-read.md` (режиссёрский разбор перед сюжетным промтом), `seedance-2.0/references/reference-transfer-contract.md` (один владелец на каждое измерение референса), `seedance-2.0/references/retake-protocol.md` (экономика итераций), `seedance-2.0/references/sequence-project-state.md` и `seedance-2.0/references/continuation-handoff.md` (состояние многоклиповой работы), `seedance-2.0/references/anti-slop-lexicon.md` и `seedance-2.0/references/vocab/ru.md` (точная производственная лексика), `seedance-2.0/references/failure-atlas.md` (симптом → причина → одна правка), `seedance-2.0/references/filter-vocab.md` и под-скиллы `seedance-filter` / `seedance-copyright` (безопасный и IP-safe рерайт).

Условные кинематографические модули:

- `references/tig-scene-engine.md` — писать или аудировать драматическую сцену/sequence; проверять Goal, Obstacle, Tactic, Reversal и Value Shift.
- `references/tig-acting-task.md` — строить актёрскую задачу для диалога, реакции, слушания, живых глаз и исправления плоской/переигранной игры.
- `references/tig-blocking-map.md` — создавать staging reference и connector при точном multi-character blocking, смене мест, поз, gaze и trajectory.
- `references/cinedance-v4.md` — собирать production-ready current-shot prompt для Seedance/Higgsfield и чинить нестабильную генерацию.
- `references/cinedance-optics.md` — выбирать FOV и защищать lens behavior.
- `references/cinedance-blocking.md` — фиксировать first frame, spatial blocking, gaze/body orientation, cut format и continuity.
- `references/cinedance-physics-lighting.md` — фиксировать физику, свет, handheld, диалог/audio и hierarchy референсов.

При конфликте актуальные mode, limits, parameters и reference contract определяет платформенный файл выбранной модели: `seedance-2.5.md` для Seedance 2.5, `minimax-h3.md` для MiniMax H3, `gemini-omni-flash.md` для Gemini Omni Flash, `gpt-image-2.md` для GPT Image, `nano-banana-pro.md` для Nano Banana Pro и `seedream-5.md` для Seedream 5.0. CINEDANCE определяет режиссуру видимого шота. Не переноси структуру промпта Seedance в H3 или в Omni и обратно: формат полей и лимиты у моделей разные. Отдельно: не переноси на Omni параметры Veo (`generate_videos`, `duration_seconds`, `negative_prompt`, `person_generation`, `generate_audio`, LRO-опрос) — у Omni их нет, он работает через Interactions API. Вендоренный пакет `seedance-2.0/` стоит ниже платформенных файлов навыка: его длительности, лимиты, разрешения, model ID, цены и наборы режимов действуют только для линии Seedance 2.0 и не переносятся ни на одну другую модель. Переносимо из него только моделе-независимое ремесло. Последнее прямое указание пользователя и утвержденный brief lock всегда выше всех файлов.

## Правила чтения

1. Сначала прочитай пользовательские файлы и текущий чат, затем общие заметки.
2. Не загружай все заметки без необходимости.
3. Последняя явная правка пользователя важнее старой заметки.
4. Запись журнала считается подтвержденной только если в ней указан реальный результат; иначе это гипотеза.
5. Если в проектной папке есть отдельный `AGENTS.md`, прочитай и соблюдай его до любых изменений.

## Фиксация выводов

После фактической проверки кратко зафиксируй результат в проектной папке (`NOTES.md` или рядом с `PROMPT_vN.md`). Во внешнюю базу пиши только если пользователь явно попросил.
