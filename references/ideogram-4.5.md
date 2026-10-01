# Ideogram 4.5 — генерация, текст и редактирование

Проверено по документации 2026-10-02. Технические параметры ниже относятся к **Runware**; для Ideogram.ai, прямого Ideogram API и других хостов проверяй собственный контракт. Все примеры здесь авторские; их генерация не тестировалась. Основные правила скилла сохраняются: английские инструкции для изображений, точный текст на языке брифа, локации 21:9 и старт нового персонажа с карты лица.

## 1. Выбери маршрут

| Задача | Маршрут |
| --- | --- |
| Новое изображение, постер, упаковка, рекламный макет | Ideogram 4.5, текстовый промпт |
| Перенос предмета или атрибутов референсов, новый формат кадра | Ideogram 4.5 с референсами |
| Локальная ретушь, новая расцветка, цепочка правок с сохранением окружения | Ideogram 4.5 Precise Edit |
| Прямая локальная открытая Ideogram 4 | Отдельный JSON-контракт, §7 |

Обычная 4.5 перерисовывает кадр при редактировании; Precise Edit восстанавливает неизменённые пиксели из исходника. Это заявленное поведение, а не подтверждение конкретного результата. Precise Edit требует исходник и не заменяет генерацию с нуля или изменение формата холста. [Reference editing](https://runware.ai/docs/models/ideogram-4-5/guides/reference-editing).

## 2. Генерация и композиция

Порядок описания: **назначение/формат → субъект → окружение → размещение → свет → камера/стиль**. Пустое место задавай конкретно: где оно, какую долю занимает и как выглядит. Для копирайта, добавляемого позднее, оставляй пространство без генерируемого текста. Подробный готовый бриф обычно веди с Magic Prompt off; короткую идею можно исследовать с auto/on/off. Переписывание способно добавлять незаданные детали. Размер и качество выбираются реальными настройками. [Prompting](https://runware.ai/docs/models/ideogram-4-5/guides/prompting).

Каркас; заполни нужные слоты и убери служебные скобки:

```text
[Deliverable and placement]. [Subject, appearance, materials and action]. [Setting]. [Position, framing and relationships]. [Empty region, its share and appearance, if needed]. [Approved copy and its location, if needed]. [Lighting, palette and camera or illustration style]. [Brief-specific constraints].
```

Авторский product hero:

```text
Commercial product photograph for a horizontal 16:9 website banner. A matte ivory reusable coffee cup with a brushed steel lid stands on a pale limestone counter in the right third of the frame. The left 45% is an uninterrupted warm cream wall, empty for copy to be added later. Soft window light from the left, a subtle contact shadow beneath the cup, natural material textures. Eye-level camera, 85mm lens, shallow depth of field. No printed text, logos, people or additional products.
```

## 3. Текст, типографика и макет

Каждую точную строку заключай в двойные кавычки и назначай ей место, размер, вес, тип шрифта и регистр. Блоки описывай в порядке чтения, каждому выделяй регион и собственную иерархию. При фиксированном копирайте исключай дополнительные строки. Длинной строке выделяй больше места или задавай утверждённые переносы; большие абзацы лучше верстать после генерации. Для кириллицы и других письменностей сохраняй исходные символы, при необходимости указывай направление чтения. Палитру можно описать именами цветов и HEX. Проверяй пунктуацию, цифры, переносы и логотипы: инструкция не гарантирует правильного написания. [Text and design](https://runware.ai/docs/models/ideogram-4-5/guides/text-and-design).

Авторский постер:

```text
Minimal portrait 4:5 coffee shop poster on a warm cream background. A small dark brown illustration of an espresso cup sits in the lower third. At the top, the exact headline "SLOW MORNINGS" appears in large bold dark brown serif capitals, centered on two lines: "SLOW" above "MORNINGS". Below the headline, place "COFFEE & CONVERSATION" in smaller letter-spaced sans-serif capitals. Strong contrast, generous margins, restrained cream and espresso-brown palette. Render only the specified words, with no additional text, logos or decorative badges.
```

Авторская точная замена текста:

```text
Replace the top headline with the exact text "ТИХОЕ УТРО". Keep its existing position, alignment, color and serif style; adjust only its size if needed to fit inside the current headline area. Preserve the illustration, background and all other text. Keep everything else in the image exactly the same.
```

Перевод и дословная замена — разные поручения. Для утверждённого перевода передавай готовые строки; не поручай самостоятельно менять смысл слогана, цену или контакты. [Text and localization](https://runware.ai/docs/models/ideogram-4-5-precise-edit/guides/text-localization).

## 4. Референсы и привязка

В обычной 4.5/Runware первое изображение в `inputs.referenceImages` — исходник: `image 1`; доноры — `image 2` и далее по фактическому порядку. Назначай каждому конкретный переносимый атрибут и место назначения. Максимум пять изображений с исходником; при маске — четыре. С референсами `settings.magicPrompt` не передавай. При обычной правке без маски задавай поддерживаемый размер, сохраняющий формат; при маске `width`/`height` опускай. Масочный результат ограничен 2048 px по длинной стороне. [Reference editing](https://runware.ai/docs/models/ideogram-4-5/guides/reference-editing).

В Precise Edit исходник находится отдельно в `inputs.seedImage`: называй его `the source image`. Для единственного донора используй `the reference image`; для нескольких — `reference image 1`, `reference image 2` по порядку массива доноров после проверки контракта среды. Не называй единственный донор `image 2` по аналогии с обычной 4.5. Проверяй доступные подписи в текущем хосте.

Во враппере с реальными тегами используй точные `@Тег`; для Runware сопоставляй теги полям и порядку загрузки в карте ролей вне промпта. Не придумывай метки `<IMAGE_REF_N>` и отсутствующие вложения.

Авторский перенос продукта для обычной 4.5/Runware, загружены два изображения:

```text
Place the exact ceramic table lamp from image 2 on the empty desk surface at the right side of image 1. Preserve the lamp's silhouette, proportions, glaze color and base design. Match its scale, perspective, contact shadow and reflections to the desk and existing room light. Keep the room, furniture, camera position and all other objects in image 1 unchanged.
```

Авторская правка Precise Edit с исходником и одним донором материала:

```text
In the source image, change only the armchair upholstery to match the forest-green velvet swatch in the reference image. Transfer only the swatch's color and material texture. Preserve the armchair's shape, seams, wooden legs, position and contact shadow. Preserve the room, neighboring objects, camera and lighting. Keep everything else in the image exactly the same.
```

## 5. Precise Edit: цепочка и маска

Один раунд — одна проверяемая смысловая правка: **изменение → цель → сохранение остального**. После принятия используй принятый результат как следующий исходник; отклонённую версию в цепочку не включай. Сохраняй исходник и промежуточные `imageUUID`/файлы для отката. Черновик можно проверять на low/very_low; финальную правку повторяй на high от того же исходника, а не от чернового результата. Глобальную смену света делай после локальных правок. На Runware результат ограничен 2048 px по длинной стороне; больший исходник уменьшается. [Iterative editing](https://runware.ai/docs/models/ideogram-4-5-precise-edit/guides/iterative-editing).

Маска совпадает с размером исходника: белый направляет правку, чёрный сохраняет; нужны обе области. Серые значения округляются, мягкую растушёвку не обещай. Маска — направляющая, а не точный контур. Выделяй целевой предмет с уместным запасом, учитывая контактную тень и защищённые соседние детали. С маской Precise Edit принимает до трёх дополнительных референсов. [Masked edits](https://runware.ai/docs/models/ideogram-4-5-precise-edit/guides/masked-edits).

## 6. Проверенные поля Runware

| Поле | Обычная 4.5 | Precise Edit |
| --- | --- | --- |
| `model` | `ideogram:4.5@0` | `ideogram:4.5@precise-edit` |
| `positivePrompt` | Текст, 1–10000 символов | Текст правки, 1–10000 символов |
| Исходник | Первый в `inputs.referenceImages` для правки | Обязательный `inputs.seedImage` |
| Доноры | До четырёх после исходника; до трёх с маской | До четырёх в `inputs.referenceImages`; до трёх с маской |
| Маска | `inputs.maskImage`, размер первого изображения | `inputs.maskImage`, размер `seedImage` |
| `settings.magicPrompt` | auto/on/off, только T2I | Не переносить из T2I |
| `settings.quality` | T2I: low/medium/high; edit: также very_low | very_low/low/medium/high |

Для T2I выбирай поддерживаемую пару `width`/`height`: например 1024×1024 для черновика, 2048×2048 для финала. Перечень размеров сверяй в текущем API, особенно для обязательных локаций 21:9. Размеры редактирования без маски проверяй отдельно от T2I presets; не ограничивай их молча списком генерации. Не назначай CFG, steps, negativePrompt и поля других моделей без подтверждения хоста. При расхождении сводной схемы и руководства сверяй конкретный режим перед вызовом. [4.5 API](https://runware.ai/docs/models/ideogram-4-5), [Precise Edit API](https://runware.ai/docs/models/ideogram-4-5-precise-edit).

Для позы можно назначить скелетный референс отдельным донором; его роль ограничена позой, не личностью или стилем. Положение кистей, выражение лица и смысл жеста допиши словами; порядок входов и масштаб скелета сверяй по [Pose control](https://runware.ai/docs/models/ideogram-4-5/guides/pose-control).

## 7. Ideogram 4 JSON — отдельная версия

Открытый репозиторий описывает **Ideogram 4**, обученную на структурированных JSON captions; это не подтверждает обязательность JSON для 4.5. Для прямой локальной 4 передавай JSON либо результат её Magic Prompt:

- `high_level_description` — замысел;
- `style_description` — стиль: либо `photo` с `medium: "photograph"`, либо `art_style`; порядок ключей зависит от варианта;
- обязательный `compositional_deconstruction`: сначала `background`, затем `elements`;
- элементы `obj`/`text`; у текста отдельные `text` и `desc`;
- необязательный `bbox`: **[y_min, x_min, y_max, x_max]**, координаты 0–1000 от верхнего левого угла;
- HEX — uppercase `#RRGGBB`; канонический порядок ключей; сериализация Python — `separators=(",", ":")`, `ensure_ascii=False`.

Точную схему бери из [официального prompting.md](https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md), системные промпты — из [magic_prompt_system_prompts](https://github.com/ideogram-oss/ideogram4/tree/main/src/ideogram4/magic_prompt_system_prompts). Локальный Magic Prompt отличается от production-версии Ideogram.ai.

[cocktailpeanut/ideoprompt](https://github.com/cocktailpeanut/ideoprompt) преобразует описание в JSON для **4** локально на Qwen3: ограничение декодирования грамматикой, нормализация и проверка AJV. Полезен как пример системного промпта и валидатора. Поддержка 4.5 не заявлена; автоматически устанавливать его ради обычного промпта 4.5 не нужно.

## 8. Диагностика и выдача

Рабочие способы диагностики, а не доказанные причины каждого сбоя:

| Наблюдение | Следующая правка |
| --- | --- |
| Нет места под копирайт | Укажи регион, его долю и однородный фон |
| Добавились незаданные слова/предметы | Проверь Magic Prompt; перечисли допустимые строки и ограничения |
| Надпись не помещается | Дай больше места или утверждённые переносы; не сокращай текст самовольно |
| Перенеслись лишние признаки донора | Сузь его роль до атрибута; проверь порядок вложений |
| Перекраска изменила окружение | Проверь маршрут Precise Edit, preserve-список и маску |
| Результат меньше исходника | Проверь лимит хоста и маршрут получения высокого разрешения |

Перед выдачей проверь версию/среду, наличие вложений, точные строки, роли и настройки. Если заказан только промпт — верни один полный английский промпт и настройки отдельно, без генерации. Если заказан результат — осмотри текст, геометрию и сохранённые детали по брифу. Быстрый режим «без проверки» основного навыка сохраняет приоритет. Не объявляй успешную кириллицу, пиксельную неизменность или печатное разрешение без проверки.

## 9. Источники и обновление

Источники приведены рядом с правилами. Дополнительно: [официальная страница Ideogram 4.5](https://ideogram.ai/models/4.5) показывает возможности и демонстрации; она не заменяет контракт хоста. Её демонстрация высокого разрешения не отменяет лимит Runware.

При смене версии/хоста или перед API-интеграцией обнови параметры по первоисточнику. Не выдавай ограничения Runware за универсальные ограничения модели и не переключайся с 4.5 на 4 только из-за готового JSON-примера.
