# Пакет Seedance 2.0 (вендоренный)

Внутри навыка лежит полная копия внешнего пакета `seedance-20` — папка `seedance-2.0/`. Это отдельный корпус знаний по линии **Seedance 2.0** плюс набор моделе-независимых режиссёрских методов. Он ничего не заменяет в навыке: он подключается условно и стоит НИЖЕ платформенных файлов навыка.

Источник: `github.com/Emily2040/seedance-2.0`, релиз `6.7.0`, коммит `44b5149`, лицензия MIT (`seedance-2.0/LICENSE`), автор `Iamemily2050`. Вендорено 2026-09-01. Провенанс и что изменено при переносе — `seedance-2.0/ATTRIBUTION.md`.

## 1. Главное правило: 2.0 — это не 2.5

Пакет написан для **Seedance 2.0** и сам это декларирует: «This skill is for Seedance 2.0. A newer line exists and is out of scope».

Из пакета **НИКОГДА** не переносить в Seedance 2.5:

- длительности, лимиты кадров и ceiling'и референсов;
- разрешения, aspect, fps;
- model ID, эндпоинты, цены, названия площадок и их наборы режимов;
- утверждения «на этой площадке есть edit / extend / R2V».

Всё это для 2.5 определяет только `references/seedance-2.5.md`. При любом расхождении побеждает `seedance-2.5.md`.

Из пакета **можно и нужно** брать моделе-независимое ремесло: режиссура, драматургия, роли референсов, continuity, антислоп, диагностика брака, экономика итераций, языковой словарь. Числа не переносятся, ремесло переносится.

Та же граница действует для MiniMax H3, Gemini Omni Flash, GPT Image и Seedream 5.0: их параметры и формат полей владеют `minimax-h3.md`, `gemini-omni-flash.md`, `gpt-image-2.md`, `seedream-5.md`. Пакет 2.0 не имеет права переписывать ни одно их поле, тег или лимит.

Приоритет целиком: прямое указание пользователя → `BRIEF LOCK` → платформенный файл выбранной модели → `cinematic-orchestration.md` и её модули (CINEDANCE, Scene Engine, Acting Task, Blocking Map) → пакет `seedance-2.0/` → общие эвристики навыка → предположение агента.

## 2. Когда загружать

Загружай пакет условно, не по умолчанию:

- пользователь прямо работает на Seedance 2.0 / Dreamina / Jimeng / CapCut / Doubao / Volcengine-Ark / BytePlus / fal / router-площадках по линии 2.0 — тогда пакет становится основным платформенным источником для этой задачи;
- нужен один из принятых методов раздела 4 (Director's Read, reference authority, retake, sequence state, антислоп, failure atlas и т.д.);
- нужен профессиональный словарь камеры/света/движения на ru, zh, ja, ko, es, en;
- нужен разбор брака генерации, обход фильтра без потери замысла или IP-safe переписывание;
- нужна раскладка длинной истории на связанные клипы с состоянием проекта.

Не загружай пакет для чистой фотогенерации, для правки изображения и в быстром режиме точечной правки.

## 3. Карта пакета

Точка входа — `seedance-2.0/ROOT.md`: там operating loop, fast lane, гейты и таблица маршрутизации. Читай его первым, потом только нужные файлы по ссылкам.

Под-скиллы (`seedance-2.0/skills/<имя>/GUIDE.md`, файлы переименованы из `SKILL.md`, чтобы хост не подхватил их как отдельные навыки):

| Задача | Файл |
| --- | --- |
| Интервью и бриф, длинное / короткое | `seedance-interview`, `seedance-interview-short` |
| Сборка промпта, компактный промпт | `seedance-prompt`, `seedance-prompt-short` |
| Камера, свет, движение, VFX, стиль | `seedance-camera`, `seedance-lighting`, `seedance-motion`, `seedance-vfx`, `seedance-style` |
| Персонажи, identity lock, multi-character | `seedance-characters` |
| Аудио, диалог, липсинк, музыка | `seedance-audio` |
| Длинная история, связанные клипы | `seedance-sequence` |
| Продолжение, extend, ремонт хвоста | `seedance-continuation` |
| Брак генерации, диагностика | `seedance-troubleshoot` |
| Антислоп, чистка формулировок | `seedance-antislop` |
| Блокировки фильтра, безопасный рерайт | `seedance-filter` |
| IP, бренды, публичные лица, лайкнесс | `seedance-copyright` |
| Шаблоны и жанровые рецепты | `seedance-recipes` |
| API, площадки, batch, ComfyUI, пост | `seedance-pipeline` |
| Словари: en, ru, zh, ja, ko, es | `seedance-vocab-*` |
| Примеры на zh, ja, ko | `seedance-examples-*` |

Ключевые reference-файлы (`seedance-2.0/references/`):

- Режиссура и драматургия: `directors-read.md`, `directing-engine.md`, `directing-engine-genre-library.md`, `storytelling-framework.md`, `intent-vs-precision.md`.
- Кадр и грамматика: `cinematography-shot-language.md`, `multishot-grammar.md`, `event-density.md`, `2d-anime-grammar.md`, `dense-storyboard-mode.md`.
- Референсы: `reference-workflow.md`, `reference-transfer-contract.md`, `surface-prompt-profiles.md`.
- Секвенции и continuity: `sequence-project-state.md`, `continuation-handoff.md`, `shot-list-continuity.md`, `continuity-qc.md`, `sequence-worked-trace.md`.
- Качество и итерации: `retake-protocol.md`, `failure-atlas.md`, `anti-slop-lexicon.md`, `filter-vocab.md`, `eval-rubric.md`, `delivery-qc.md`, `field-observed-tips.md`.
- Модель и бюджет: `model-mechanics.md`, `capability-map.md`, `allocation-model.md`, `prompt-compiler.md`, `json-schema.md`, `quick-ref.md`.
- Пост и доставка: `audio-guide.md`, `audio-post-delivery.md`, `color-pipeline-aces.md`, `subtitles-localization.md`, `aspect-ratio-delivery.md`, `pro-filmmaking-standards.md`.
- Платформа 2.0 (только для 2.0): `api-status.md`, `api-workflow.md`, `platform-constraints.md`, `platform-surface-matrix.md`, `model-name-map.md`, `source-registry.md`, `research-2026-05-30.md`.
- Языки: `vocab/en.md`, `vocab/ru.md`, `vocab/zh.md`, `vocab/ja.md`, `vocab/ko.md`, `vocab/es.md`, `multilingual-community-examples.md`, `multilingual-native-review.md`, `interview-starters.md`.

Остальное: `seedance-2.0/schemas/` — JSON-схемы clip-contract, project-state, take-review, prompt-spec, generation-run; `seedance-2.0/examples/` — золотые промты и разобранная секвенция «airport arrival»; `seedance-2.0/evals/`, `seedance-2.0/data/` — рубрики и снимок сообщества; `seedance-2.0/scripts/extract_last_frame.py` — извлечение последнего кадра тейка (stdlib, запуск `python seedance-2.0/scripts/extract_last_frame.py <файл>`).

## 4. Методы, принятые в основной workflow

Эти методы моделе-независимы и применяются в навыке независимо от того, какая модель выбрана. Числа при этом всё равно берутся у платформенного файла модели.

1. **Director's Read перед любым сюжетным промптом** — `seedance-2.0/references/directors-read.md`. Для сюжетного, персонажного или перформанс-брифа заполнить внутренний режиссёрский разбор (драматическая функция, поворот, подавленное поведение, непереносимая деталь, отказ от штампа жанра) и перевести его в видимые носители: блокинг, взгляд, жест, работа с предметом, конечная точка камеры, мотивированный свет, реплика, тишина. Для утилитарного, packshot, абстрактного или VFX-брифа драму не выдумывать — записать утилитарное намерение и явный отказ. Это внутренний бриф, а не текст промпта. Встраивается перед шагом сборки промпта в `cinematic-orchestration.md`.

2. **Разрешение авторитета референсов по измерениям** — `seedance-2.0/references/reference-transfer-contract.md`, `seedance-2.0/references/reference-workflow.md`. Усиление существующего правила ролей: мало назначить роль — для каждой цели и каждого управляемого измерения (identity, одежда, продукт, среда, свет, движение, камера, тайминг, стиль, звук) назвать ровно одного владельца или пометить измерение неприменимым. Один референс может владеть несколькими измерениями; у измерения не может быть двух владельцев. Референс, не владеющий ничем, — убрать. Явно перечислить, что из каждого референса не переносится. Никогда не выводить авторитет из типа файла, порядка загрузки, имени файла или порядка упоминания. Синтаксис привязки при этом остаётся тот, что требует среда: `@Тег` по умолчанию, официальные метки `<Subject N>` / `<IMAGE_REF_N>` там, где их требует модель.

3. **Retake protocol — экономика итераций** — `seedance-2.0/references/retake-protocol.md`. Вернувшийся тейк сортировать: принять / чинить в посте / править edit'ом / перегенерировать / переписать промпт. Одна переменная на один ретейк. Встраивается в `qa-and-delivery.md` как правило безопасной итерации.

4. **Состояние проекта секвенции** — `seedance-2.0/references/sequence-project-state.md`, `seedance-2.0/references/continuation-handoff.md`, схема `seedance-2.0/schemas/project-state.schema.json`. Для многоклиповой работы держать состояние: канон персонажей и локаций, принятые тейки, наблюдаемое конечное состояние, глубина цепочки. Продолжение писать от наблюдаемого конца принятого тейка, который сверен с исходником. Отклонение не обновляет канон: сначала исправление или разрешённая новая сценарная версия по `story-production-contract.md`. `project-state.json` хранит оперативное состояние и связан с единственным живым STATE проекта; не является вторым сценарием. Промпт версионируется в `PROMPT_vN.md`, состояние секвенции — рядом в `project-state.json`.

5. **Правило ненаблюдённого** — `ROOT.md`, раздел intake. Никогда не утверждать, что видел, слышал, измерил или проверил то, что не открывал. Если тейк или референс недоступен для осмотра — сказать прямо, работать по описанию пользователя и пометить такие детали как со слов пользователя. Особенно важно для `observed end state` в продолжениях: выдуманное наблюдение портит канон всей секвенции.

6. **Антислоп и точный словарь** — `seedance-2.0/references/anti-slop-lexicon.md`, `seedance-2.0/references/vocab/ru.md` и остальные языки. Чистка пустых суперлативов, ватных прилагательных и слабых глаголов; замена на производственную лексику. Применять к финальному промпту на любой модели, но не вырезать негативы и детали, добавленные пользователем (реестр требований `R1…` в `SKILL.md` главнее).

7. **Filter-safe рерайт и IP-контур** — `seedance-2.0/references/filter-vocab.md`, `seedance-2.0/skills/seedance-filter/GUIDE.md`, `seedance-2.0/skills/seedance-copyright/GUIDE.md`. Когда промпт блокируется или содержит франшизу, бренд, публичное лицо или реальную персону — переписать безопасно, не теряя замысла. Не использовать для обхода защит там, где запрос действительно нарушает права.

8. **Failure atlas и диагностика** — `seedance-2.0/references/failure-atlas.md`, `seedance-2.0/skills/seedance-troubleshoot/GUIDE.md`. Симптом → корневая причина → одна правка. Дополняет разделы диагностики `cinematic-orchestration.md` и `qa-and-delivery.md`.

9. **Бюджет промпта** — `seedance-2.0/references/allocation-model.md`, `seedance-2.0/references/capability-map.md`, `seedance-2.0/references/model-mechanics.md`, `seedance-2.0/references/event-density.md`. Решать, куда промпт тратит точность, и не перегружать один клип количеством событий. Идея переносимая; конкретные ceiling'и — только для 2.0.

10. **Multi-shot грамматика и dense storyboard** — `seedance-2.0/references/multishot-grammar.md`, `seedance-2.0/references/dense-storyboard-mode.md`. Реальные монтажные стыки внутри одной генерации и плотная раскадровка. Полезно рядом с `storyboard-to-video.md`; лимит числа шотов внутри одной генерации берётся у платформенного файла модели.

11. **Пост и доставка** — `seedance-2.0/references/delivery-qc.md`, `seedance-2.0/references/audio-post-delivery.md`, `seedance-2.0/references/subtitles-localization.md`, `seedance-2.0/references/color-pipeline-aces.md`, `seedance-2.0/references/aspect-ratio-delivery.md`. Чек-листы финальной выдачи; дополняют `qa-and-delivery.md` для клиентской и рекламной работы.

## 5. Что из пакета не брать

- Числа, эндпоинты и model ID линии 2.0 — для любой другой модели.
- `seedance-2.0/references/agent-compatibility.md`, `seedance-2.0/references/progressive-disclosure.md`, `seedance-2.0/references/frontend-design-system.md`, `seedance-2.0/references/community-source-methodology.md`, `docs/` и CI-скрипты исходного репозитория — это обслуживание того репозитория, не креативная работа.
- Формат вывода и разговорный протокол пакета — у навыка свой: `BRIEF LOCK`, реестр требований `R1…`, правило полной выдачи промпта, быстрый режим точечной правки. Пакет их не отменяет.
- Соглашение `@Video1` / `@Image1` из пакета не заменяет `@Тег` пользователя. Теги вложений остаются как есть.

## 6. Правила чтения

0. Все пути вида `seedance-2.0/...` в файлах навыка даются от корня навыка, а не относительно текущего файла. Ссылки внутри самого пакета — относительные и рабочие.
1. Не открывать пакет целиком. Вход — `seedance-2.0/ROOT.md`, дальше по ссылкам только нужный файл.
2. Один под-скилл за раз; языковые словари грузить только по языку задачи.
3. Ссылки внутри пакета относительные и проверены; `SKILL.md` под-скиллов переименованы в `GUIDE.md`.
4. Если файл пакета противоречит платформенному файлу навыка — молча следовать файлу навыка и, если это влияет на результат, сказать об этом одной строкой.
