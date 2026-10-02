# FLUX 3 Image — промпты, текст, референсы и layout

Проверено по официальной документации BFL 2026-10-02. Это контракт **FLUX 3 Image**, не FLUX 3 Video, FLUX.2 или Kontext. Настройки относятся к BFL API; врапперы проверяй отдельно. Примеры ниже авторские и не тестировались генерацией. Общие требования навыка сохраняются: английские инструкции, дословный копирайт на языке брифа, локации 21:9, карта лица для нового персонажа и выбранные границы генерации/QA.

## 1. Выбор формы промпта

| Задача | Форма |
| --- | --- |
| Новый кадр, портрет, предметка | Связное описание результата |
| Надпись, постер, упаковка | Описание плюс точные строки и типографика |
| Локальная правка | Целевой объект → изменение → сохраняемые детали |
| Несколько источников | Роль каждого входа плюс их отношения |
| Точная компоновка, панели, многосубъектная сцена | Caption плюс JSON-массив элементов в конце строки промпта |

Обычный промпт достаточен для большинства кадров; layout добавляй, когда расположение действительно важно. Не объявляй боксы гарантией точного положения: документация multi-reference называет размещение сильной подсказкой, допускающей выход объекта за пределы области. [Страница модели](https://bfl.ai/models/flux-3-image), [Multi-Reference Editing](https://docs.bfl.ai/guides/prompting_editing_multi_reference).

## 2. Структура генерации

Начинай с **типа изображения/medium → субъекта и действия → окружения → света → кадрирования и деталей**. Порядок — рабочая привычка, не жёсткая грамматика: важнейшее требование можно поставить первым. Описывай отношения: кто перед кем, куда смотрит, что держит. Короткая идея работает; расширяй только там, где нужен контроль. Конкретная фактура, источник света и ракурс полезнее цепочки `masterpiece`, `best quality`, `ultra-detailed`. Каждое предложение должно описывать видимый результат. [Building a Good Prompt](https://docs.bfl.ai/guides/prompting_unified_building).

Для фото задавай наблюдаемый эффект оптики/плёнки, а не только название камеры: размер плана, высоту камеры, глубину резкости, зерно, цветовой сдвиг. Свет описывай через источник, направление, мягкость, температуру и взаимодействие с материалами. HEX назначай конкретному объекту, чтобы цвет не распространился на всю сцену. [Style, Aesthetics & Text](https://docs.bfl.ai/guides/prompting_unified_style).

Авторский каркас; заполни нужные слоты и убери скобки:

```text
[Image type and medium]. [Subject, appearance and action]. [Setting and relationships]. [Light source, direction and quality]. [Framing, camera angle, focus and visible material detail]. [Palette]. [Exact approved text, placement and type, if needed].
```

Авторская предметка:

```text
Editorial product photograph of a matte forest-green ceramic coffee cup on a pale limestone table. The cup occupies the right third of the frame; the left half is a smooth cream background reserved for a headline added later. Soft window light falls from the left, revealing the ceramic texture and a gentle contact shadow. Eye-level framing, 85mm lens, shallow depth of field. Restrained forest-green and cream palette, clean unmarked surfaces.
```

## 3. Текст и макет

Каждую точную строку заключай в двойные кавычки, сохраняя регистр, пунктуацию и исходную письменность. Укажи место и типографику: размер относительно других строк, вес, serif/sans-serif, цвет, фактуру. Переносы можно задать `\n` внутри цитаты или словами; направление чтения указывай отдельно. Для плотного макета разбивай текст на блоки, каждому выделяй область. Короткая надпись не требует layout. Все строки проверяй по реальному результату, особенно мелкий текст. [Style, Aesthetics & Text](https://docs.bfl.ai/guides/prompting_unified_style).

Авторский постер:

```text
Flat graphic coffee shop poster on a warm ivory background. A forest-green illustration of an espresso cup sits in the lower third. At the top, centered large dark green serif capitals read "ТИХОЕ УТРО". Immediately below, smaller widely spaced sans-serif letters read "КОФЕ И РАЗГОВОРЫ". The design contains exactly these two text blocks. Generous margins, crisp edges and a restrained ivory-and-green palette.
```

## 4. Ограничения и реальные настройки

В BFL API FLUX 3 Image нет `negative_prompt`, `guidance`, `seed` и `prompt_upsampling`. Не добавляй эти поля из FLUX.2, локального workflow или другой модели. Для генерации заменяй отрицание конкретным желаемым видом: пустой пешеходный проход, однотонный фон, чистая немаркированная поверхность. Это не разрешает удалять пользовательское требование: перенеси его смысл в положительное описание. В правке команда удалить конкретный объект допустима. [Prompting Basics](https://docs.bfl.ai/guides/prompting_unified_basics), [Technical Parameters](https://docs.bfl.ai/guides/prompting_unified_technical).

| Поле BFL | Что учитывать |
| --- | --- |
| `prompt` | Связный текст; layout-строки, если нужны, добавляются в конец этого же prompt |
| `images` | До 10 референсов, каждый минимум 256×256 и максимум 16 MP |
| `aspect_ratio` | 15 фиксированных форматов от 21:9 до 9:21, либо auto |
| `resolution` | 768sq, 1k, 2k, 4k; 1k по умолчанию |

`auto` берёт формат первого референса; без изображений даёт 1:1. Для нового неквадратного кадра ставь формат явно. Для локации ставь 21:9 в настройках и английском описании. Черновик можно исследовать на 768sq, финал — на нужном разрешении. Смена разрешения запускает новую генерацию: композиция может измениться. Без seed повтор одного промпта тоже может дать другой результат. Проверяй фактические размеры ответа; слово 4K в тексте не задаёт разрешение. [Technical Parameters](https://docs.bfl.ai/guides/prompting_unified_technical).

Не придумывай API endpoint, model ID, поля маски или отдельный mode для генерации/правки. Для интеграции сверяй [актуальный API reference](https://docs.bfl.ai/api-reference/utility/generate-an-image-with-flux-3); если страница недоступна, обозначь неподтверждённые поля, а не достраивай их по памяти.

## 5. Редактирование и референсы

Для одной картинки точно выдели цель положением/внешностью, назови новое состояние и перечисли важные инварианты. Не переписывай целиком описание сцены ради перекраски. Несколько независимых изменений допустимы, если каждому задано место и ясно, что сохраняется. Для итераций удобнее один проверяемый смысловой блок за раз; это рабочий приём, не лимит модели. [Single-Reference Editing](https://docs.bfl.ai/guides/prompting_editing_single_reference).

Авторская правка:

```text
Change only the upholstery of the armchair beside the window to forest-green velvet, color #234A3B. Preserve its silhouette, seams, wooden legs, position and contact shadow. Preserve the room layout, neighboring furniture, camera angle and existing light.
```

Для нескольких входов обычный промпт BFL использует `image 1`, `image 2` по порядку `images`. Поставь базовую сцену первой, особенно при auto. Назначь роли: личность, продукт, материал, стиль, окружение; затем опиши масштаб, контакт, ориентацию и освещение. Если один источник поставляет несколько признаков, перечисли их явно, не позволяя ему молча переопределить остальные источники. [Multi-Reference Editing](https://docs.bfl.ai/guides/prompting_editing_multi_reference).

Авторское объединение двух загруженных изображений:

```text
Place the exact table lamp from image 2 on the left end of the wooden sideboard in image 1. Take only the lamp's shape, material and color from image 2. Match its scale, perspective and contact shadow to image 1. Preserve the room architecture, sideboard, framed artwork, camera and window light.
```

Во враппере с настоящими тегами используй его `@Тег`. Для прямого BFL составь карту «тег пользователя → позиция images» вне промпта. Нумерация обычного текста начинается с 1, внутренних ref_image — с 0; не смешивай их. Для layout используй только реально загруженные источники.

## 6. Layout: caption и элементы

Описание всего кадра сопровождается JSON-массивом элементов в конце **той же строки prompt**. Каждый элемент имеет `id`, `bbox`, `desc`; caption ссылается на каждый id в месте его появления. Бокс задаётся **[y_min, x_min, y_max, x_max]**, нормализованная сетка 0–1000 от верхнего левого угла. Не используй порядок x/y по привычке. Общий aspect_ratio должен соответствовать макету. Это отдельная схема, не JSON-caption Ideogram 4. [Страница FLUX 3 Image](https://bfl.ai/models/flux-3-image).

Иллюстративный авторский layout-промпт; координаты адаптируй к брифу:

```text
A flat portrait poster on an ivory background. The headline <headline_1> occupies the top band. The green cup illustration <cup_1> sits below it. The small footer <footer_1> is centered near the bottom. Clean graphic edges and generous margins.
[{"id":"headline_1","bbox":[60,100,220,900],"desc":"Large dark green serif capitals reading exactly \"ТИХОЕ УТРО\"."},{"id":"cup_1","bbox":[330,250,760,750],"desc":"A flat forest-green espresso cup illustration."},{"id":"footer_1","bbox":[850,120,930,880],"desc":"Small dark green sans-serif text reading exactly \"КОФЕ И РАЗГОВОРЫ\"."}]
```

Для переноса из доноров документация использует строки с `from: "ref_image_1"` (второй вход), `src_bbox` (область исходника), `tgt_bbox` (место результата) и `desc`. Ссылки в caption имеют форму `<ref_image_0>` и `<id>`. Измеряй боксы по своим изображениям; примерные координаты не становятся универсальной раскладкой. Полный контракт операций move/remove/replace сверяй по [Layout prompts](https://docs.bfl.ai/guides/prompting_layout) и [Bounding boxes](https://docs.bfl.ai/flux_3/flux3_image_bounding_boxes) перед сборкой сложного edit-record. [Multi-Reference Editing](https://docs.bfl.ai/guides/prompting_editing_multi_reference).

## 7. Диагностика и выдача

| Наблюдение | Следующая правка |
| --- | --- |
| Кадр слишком широкий | Поставь субъект и нужный размер плана раньше окружения |
| Добавился реквизит | Конкретизируй видимые поверхности и состав сцены |
| Перепутались доноры | Проверь images, роли и различие image 1/ref_image_0 |
| Текст съехал | Выдели регион и типографику; при необходимости отдельный бокс |
| Цвет распространился на другие детали | Привяжи HEX к однозначно названному объекту |
| Финал не совпал с черновиком | Учти новую генерацию при смене разрешения; используй правку принятого кадра, когда нужна преемственность |

Это способы диагностики, не доказанные причины каждого сбоя. Перед выдачей сверь модель/среду, язык инструкций, копирайт, роли, соответствие caption/ids, координаты и настройки. Только промпт не заказывает генерацию. Результат проверяй по брифу; быстрый режим без проверки основного навыка остаётся приоритетным. Не объявляй pixel-perfect сохранение или читаемый текст подтверждёнными до осмотра.

## 8. Источники и границы переноса

Правила связаны с первоисточниками выше. Вход: [FLUX Prompting Guide](https://docs.bfl.ai/guides/prompting_summary). Официальный [black-forest-labs/skills](https://github.com/black-forest-labs/skills) полезен для изучения, но его README на дату проверки содержит много FLUX.2 и FLUX 3 Video. Не переносить их seed, режимы, таймкоды, аудиополя и JSON-схемы в FLUX 3 Image. Новые версии и хосты требуют сверки актуального контракта; установка внешних скиллов и генерация не выполняются автоматически ради написания промпта.
