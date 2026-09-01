# Seedream 5.0 (Pro / Lite) — рабочая инструкция

Используй этот документ, когда генерация или редактирование изображения идет на Seedream 5.0 Pro или Seedream 5.0 Lite (ByteDance Seed, а также хосты вроде Runway, fal и других интеграций).

Не применяй файл к видео и к другим image-моделям. Для GPT Image действует `gpt-image-2.md`, для Nano Banana Pro — заметка `02 · Nano Banana Pro (Gemini 3 Pro Image).md`, для видео — `seedance-2.5.md`, `minimax-h3.md` и `video-and-continuity.md`.

Промт для Seedream — это компактный визуальный бриф: что за картинка, в каком порядке важны ее части и что менять нельзя. Модель понимает развернутый естественный язык, референсы, пространственное редактирование, мультиязычный текст и плотные верстки.

Не обещай пользователю контрол, которого нет в его интерфейсе. Количество референсов, размеры и соотношения, маска или регион, слои и поле negative prompt зависят от хоста и варианта модели. Проверь доступное в UI/API до того, как рекомендовать настройку, и не переноси лимиты Pro на Lite и наоборот.

## 1. Сначала определи маршрут

- **Генерация** — исходного кадра нет, все создается из текста.
- **Редакция** — есть базовое изображение, меняется обозначенная область.
- **Композиция по референсам** — два и более вложения, у каждого своя роль.
- **Текст и верстка** — постер, упаковка, вывеска, меню, инфографика, UI-концепт, перевод макета.
- **Комбинация** — например редакция макета с заменой текста на другом языке.

Задавай вопрос только если неизвестный выбор реально меняет картинку: какое вложение дает идентичность, а какое стиль; должен ли текст быть дословным; какой формат и соотношение сторон. В остальном бери сдержанный дефолт и назови его одной строкой.

## 2. Форма промта

Базовый порядок, когда нужна арт-дирекция:

```text
Субъект → локация → композиция → свет → стиль/медиум → технические ограничения
```

Это ориентир, а не жесткий формат. Простой иконке хватит субъекта, стиля и ограничений; кампании нужны все слои. Самое важное требование пользователя ставь первым: поздние детали не должны перебивать его.

| Слой | Что решаешь | Нужная точность |
| --- | --- | --- |
| Субъект | Кто или что герой кадра | Отличимая внешность, материал, действие, количество объектов |
| Локация | Где и когда | Среда, сезон/время, реквизит, глубина |
| Композиция | Что зритель видит первым | Кадрирование, ракурс, передний/задний план, позиции, кроп |
| Свет | Как читается форма и настроение | Направление, мягкость, контраст, цветовая температура, источники |
| Стиль | Какой медиум управляет результатом | Editorial photography, flat vector, ceramic stop-motion, ink drawing |
| Ограничения | Что дословно и что неизменно | Точный текст, позиция логотипа, запрет лишних объектов, формат выдачи |

Начинай с одного-двух предложений и добавляй атрибут только если без него результат будет неверным. Длинные списки камерных, качественных и эстетических тегов хуже управляемы, чем связное непротиворечивое описание.

Переводи оценку в визуальное решение:

| Расплывчато | Во что превратить |
| --- | --- |
| «Красивый закат» | Тип побережья, форма облаков, направление света, палитра, силуэт переднего плана, обработка экспозиции |
| «Люксовый продукт» | Герой-объект, материал, поверхность, свет, фон, объем воздуха, бренд-настроение |
| «Кинематографично» | Кадрирование, характер объектива, контраст, грейд, дымка, действие субъекта, источник света |
| «Профессионально» | Медиум и применение: e-commerce product photography, editorial portrait, transit wayfinding, museum poster |
| «Сделай реалистично» | Поведение материалов, тени, отражения, объектив и кадр, настоящий износ и текстура |

Не используй `4K`, `masterpiece`, `award-winning` вместо визуальной инструкции. Разрешение и соотношение задавай контролами хоста, а не словом в промте.

## 3. Паттерны сборки

### Портрет и персонаж

Описывай приметы идентичности только там, где нужна повторяемость. Не перечисляй каждую черту лица, если персонаж не переиспользуется.

```text
Editorial half-length portrait of a woman in her late fifties with silver locs and a calm, direct expression, wearing a navy canvas apron. She stands behind a wooden morning-market stall, with crates of produce softly out of focus behind her. Warm early sunlight from the right, relaxed documentary-commercial photography, natural skin texture, 85 mm portrait framing.
```

### Product hero

Зафиксируй объект, логотип, расположение, поведение материала и поверхность. Реквизит держи подчиненным продукту.

```text
Premium e-commerce hero image of a frosted-glass skincare bottle with a brushed gold cap, centred on pale travertine. The label faces the camera and remains sharp and legible. A single white peony and soft fabric shadows sit behind it, out of focus. Soft morning window light from the left, subtle glass reflections, clean warm-ivory palette, restrained luxury product photography. No extra products or text.
```

### Несколько субъектов и действие

Называй субъектов по различимой примете и задавай их позиции и взаимодействие. «Два человека в кафе» не работает, когда важна расстановка.

```text
Wide horizontal editorial photo of a woman in a rust coat seated on the left side of a small café table, speaking to a man in a charcoal jacket seated on the right. A ceramic cup sits between them in the foreground. The woman is in sharp focus; the man and street outside the window are softly blurred. Overcast daylight, candid documentary photography, muted autumn palette.
```

### Иллюстрация и concept art

Сначала объяви медиум, потом набирай атмосферу.

```text
Hand-painted gouache illustration of a night train crossing a high stone viaduct above a foggy valley. The train's warm windows form the primary light source; distant moonlight cools the hills behind it. Wide composition, simplified layered shapes, visible brush texture, restrained deep-blue and amber palette.
```

### Движение внутри статики

Назови и движущийся элемент, и то, что обязано остаться резким.

```text
Fine-art black-and-white photo of a ballet dancer mid-pirouette on an empty stage. Her face and raised arm remain crisp while the spinning white skirt has intentional circular motion blur. One overhead spotlight creates a pool of light on the dark wooden floor; deep surrounding shadows, long-exposure dance photography.
```

### Камера, цвет и материалы

Камерную подсказку давай только когда она дает видимый результат; обычно хватает одной-двух:

- **Кадр:** macro, close-up, waist-up, full-length, aerial, wide establishing shot.
- **Точка съемки:** eye level, three-quarter product view, top-down flat lay, low angle, front-facing orthographic.
- **Фокус:** shallow depth of field, deep focus, focus on the foreground label.
- **Фотографический характер:** high-key studio, documentary street photograph, medium-format portrait, long-exposure blur.

Цвет описывай отношениями, а не только именами: «warm ivory against cool concrete», «a red accent in an otherwise desaturated scene». Материал описывай поведением: frosted glass, brushed metal, wet asphalt reflections, velvet nap, translucent fabric. HEX добавляй вместе с человеческим названием («#FF006E hot pink») и только для крупных плоскостей и графики — это приближение, а не гарантия печатного цвета.

## 4. Редакция

Порядок инструкции для правки:

```text
Базовое изображение → точное изменение → целевая область → список сохраняемого → визуальная интеграция
```

Изменение должно быть наблюдаемым. «Сделай лучше» — не бриф правки.

```text
Use the supplied image as the base. Change only the beige sofa upholstery to dark forest-green linen. Keep the sofa's shape, room layout, people, wall colour, camera angle, lighting direction, and all other objects unchanged. Preserve the existing shadows and perspective; show natural linen weave and subtle fabric creases.
```

Общая для навыка запись `LOCKED` / `EDITABLE` из `photo-and-storyboard.md` остается в силе: сначала защищенная область, потом новое состояние редактируемой. Для Seedream разворачивай `LOCKED` в явный preserve-список внутри самого промта.

Бери самый точный контрол, который реально есть у хоста:

| Доступный контрол | Как формулировать |
| --- | --- |
| Маска, лассо, кисть | Назови выбранную область и меняй только ее; явно сохрани все невыделенное |
| Bounding box или координаты | Укажи область по метке UI или координатам, затем содержимое, поля и масштаб |
| Клик по точке или объекту | Сошлись на объект по видимой примете: «the red backpack beside the chair» |
| Скетч поверх изображения | Скажи, что означает каждая пометка, где должен быть объект и надо ли убрать сами пометки |
| Регионального инструмента нет | Дай точное место плюс короткий preserve-список; при сносе выноси правку в отдельный проход |

Если маска уже поставлена, не переписывай в промте весь кадр заново — используй маску как границу и опиши только локальный итог.

Preserve-список бери адресно:

- **Человек:** форма лица, прическа, выражение, поза, одежда, украшения, текстура кожи.
- **Продукт:** силуэт, этикетка, положение логотипа, крышка/упаковка, пропорции, бренд-цвета.
- **Сцена:** композиция, кроп, ракурс, перспектива, направление света, глубина резкости, фоновые объекты.
- **Графика:** формулировки, иерархия, выравнивание, поля, типографика, иконки, палитра, направление чтения.

Не рассчитывай, что «оставь как было» само сохранит все перечисленное: называй то, что действительно нельзя менять.

| Задача | Формула |
| --- | --- |
| Убрать объект | «Remove only [object] from [location]. Reconstruct the exposed [surface] and shadows naturally. Keep [preserve list] unchanged.» |
| Заменить фон | «Replace only the background with [scene]. Preserve the person's face, clothing, pose, foreground edge, and original camera framing. Match the new background's light to the subject.» |
| Сменить материал | «Change only [object/region] from [old material] to [new material]. Preserve shape, scale, logo, placement, and existing lighting. Make reflections and shadows physically consistent.» |
| Перестилизовать | «Use Image 1 for content and composition. Apply only the brushwork, palette, and medium of Image 2. Keep [subjects/objects/crop] from Image 1.» |
| Ретушь | «Remove [specific imperfections] only. Preserve natural texture, identity, expression, proportions, and light; avoid excessive smoothing or deformation.» |
| Сменить глубину резкости | «Keep the composition unchanged. Make [foreground object] sharp and [background element] softly blurred, retaining the original light and colour.» |

После правки проверь снос по идентичности, логотипу, позе, кропу, тексту, перспективе, направлению света и нецелевым объектам. Следующий промт должен добавить только недостающую защиту — не подмешивай в тот же проход новый стиль.

## 5. Несколько референсов

Сначала выдай каждому вложению собственную непересекающуюся задачу. «Совмести эти изображения» без ролей не работает.

Роли: **база/композиция** (ракурс, кроп, размещение, архитектура), **идентичность** (лицо, прическа, пропорции), **объект/продукт** (конкретный предмет, одежда, логотип, текстура), **стиль** (палитра, мазок, фотографический характер), **верстка** (сетка, иерархия карточек, иконки, типографика).

Обязательно указывай, отдает референс только стиль или еще и содержание — иначе переносятся лишние объекты.

```text
Use Image 1 for the woman's facial identity and hairstyle, Image 2 for the ceramic honey jar, and Image 3 for the woven sun hat. Create a waist-up market portrait: she holds the jar at chest height and wears the hat. Use a sunlit wooden market stall with produce softly blurred behind her. Preserve the facial identity from Image 1 and the jar's label from Image 2. Match all elements in scale, perspective, soft morning light, and documentary commercial photography.
```

Именование референсов: дефолт навыка — теги `@Тег`. Индексацию `Image 1/2/3` используй, когда у вложений нет тегов или интерфейс сам нумерует загруженные картинки. Не смешивай обе схемы в одном промте.

Для серии держи неизменяемый **identity block** и повторяй его дословно, меняя только сцену, позу, гардероб и настроение:

```text
Identity block: A 32-year-old East Asian architect with a short blunt black bob, round tortoiseshell glasses, a small mole under the left eye, and a charcoal oversized blazer.
Scene variation: Walking across a rainy pedestrian crossing at dusk, holding a clear umbrella, three-quarter full-body framing, wet pavement reflections, candid editorial street photography.
```

Если источник истины — вложение, скажи это прямо: «Preserve the person's facial identity from Image 1», и не добавляй несовместимых новых примет.

Пространство описывай канвасом: левая треть / центр / правая треть; передний, средний, дальний план; за, перед, частично перекрыт; в правой руке, между ними на столе, над заголовком; масштаб — «product occupies 40% of frame height». В сложной сцене — одно отношение на предложение.

## 6. Слои и редактируемая выдача

Если хост дает разделение на слои, до генерации спроси, какие элементы нужны отдельно, и перечисли слои с порядком и перекрытием:

```text
Separate this poster into editable layers: background paper texture; headline and supporting typography; primary product bottle; flower props; cast shadows; and decorative line icons. Keep the final composite unchanged. Preserve the product label as part of the product layer and keep shadows on a separate layer with transparent surroundings.
```

Слои проси только под реальную задачу дальше по цепочке: передача в дизайн, независимый перевод, перекраска, композитинг. Если слоев в интерфейсе нет — описывай нужное разделение визуально и не обещай редактируемые файлы.

## 7. Текст, верстка и языки

Весь дословный текст на изображении бери в кавычки, укажи место, роль в иерархии, физическую поверхность и характер начертания.

```text
Vertical 4:5 public-transit safety poster. White background, black line icons, and a yellow warning band across the top. Headline at the top: "STAND CLEAR OF THE DOORS". Place three short safety steps below in a clean left-aligned grid, each paired with a black pictogram. Modern wayfinding typography, generous margins, high contrast, no other text.
```

Для вывески, этикетки, меню и упаковки называй поверхность: латунная табличка, витринная роспись, бумажный стакан, тиснёный картон, LED-панель. Держи копию короткой и всегда вычитывай результат: опечатки у image-моделей остаются возможны.

Порядок брифа для сложной графики:

```text
Формат и соотношение → назначение полосы → иерархия информации → секции и порядок чтения → изображения/иконки/графики → палитра → настроение типографики → ограничения
```

Для плотной верстки нумеруй информационные группы и описывай их взаимное расположение (шапка, левая колонка, центральный визуал, нижний сравнительный блок, футер). Не прячь важную копию внутри декоративного предложения.

Инфографику и UI-концепты Seedream **раскладывает по утвержденной информации, а не выясняет факты**. Все цифры, подписи, единицы и формулировки давай явно. Нет данных — запроси их или явно помечай верстку как иллюстративную с плейсхолдерами. Требуй `Do not invent any facts, statistics, dates, or extra labels`. UI описывай как концепт-картинку, а не работающее приложение.

Мультиязычность: Seedream 5.0 Pro официально поддерживает мультиязычный ввод и генерацию, включая русский. Сохраняй язык промта, который выбрал пользователь; переходи на английский только по его просьбе или если этого требует конкретный хост. Точный целевой текст все равно давай сам — перевод должен быть утвержден до генерации.

```text
Use the supplied medical poster as the base. Keep its palette, icons, photo, module structure, margins, and overall layout unchanged. Replace the English copy only with the following approved Russian text: "[exact text]". Retain the visual hierarchy. Do not change any image, icon, colour, or factual content.
```

При смешении систем письма указывай язык, место и направление чтения. Не заказывай неутвержденные длинные абзацы, юридический и медицинский текст и плотные таблицы без визуальной вычитки.

Бренд: цитируй копию дословно и называй место; для стабильного логотипа давай референс и требуй «preserve the original logo and label placement»; исключения формулируй явно — «no extra logo, badge, watermark, or promotional copy».

## 8. Диагностика

Найди одну самую заметную поломку и правь только ту инструкцию, которая ей управляет. Не добавляй пять новых модификаторов после каждого слабого результата — иначе непонятно, что помогло.

| Симптом | Пробел в промте | Точечная правка |
| --- | --- | --- |
| Стоковый безликий кадр | Общие прилагательные, нет решения по сцене и стилю | Замени «красиво/профессионально/кинематографично» локацией, светом, материалом, кропом и конкретным медиумом |
| Не тот главный объект | Субъект не назван или закопан в конец | Вынеси субъект и его неотчуждаемые признаки в первое предложение |
| Объекты сливаются | Не заданы пространственные отношения | Дай каждому важному объекту позицию, масштаб и одно ясное отношение |
| Продукт или логотип «плывет» | Нет источника истины и preserve | Приложи референс продукта и потребуй сохранить силуэт, этикетку, положение логотипа и пропорции |
| Лицо меняется между кадрами | Описание идентичности каждый раз новое | Повтори identity block дословно и приложи тот же референс |
| Правка задела лишнее | Широкая формулировка, нет preserve-списка | Скажи «change only …» и перечисли замороженные атрибуты |
| Добавленный объект выглядит наклеенным | Нет указаний по интеграции | Задай совпадение масштаба, перспективы, направления света, тени, отражения, текстуры и цветовой температуры |
| Текст неверный или пропал | Копия не в кавычках или верстка перегружена | Закавычь точную копию, сократи ее, задай место/поверхность/стиль и сделай проход вычитки |
| Слабая иерархия верстки | Компоненты перечислены без порядка чтения | Задай шапку, главный элемент, порядок секций, выравнивание, поля и визуальный вес |
| Цвет уезжает | Цвет назван приблизительно | Опиши цветовые отношения, для крупных плоскостей добавь HEX плюс человеческое название |
| Кадр плоский | У света нет направления и контраста | Назови источник, направление, мягкость, контраст и поведение теней |
| Промт противоречит сам себе | Слишком много несовместимых требований | Убери конкурирующие стили, второе время суток и несовместимые ракурсы |

Разбивай работу на последовательность, когда нужны одновременно строгая консистентность и несколько крупных изменений:

1. Зафиксируй идентичность субъекта/продукта и композицию.
2. Выбери удачный результат как новую базу.
3. Меняй по одной локальной вещи: сцена, материал, верстка.
4. Текст и мелкие детали правь последним отдельным проходом.

## 9. Preflight перед выдачей

- Одна главная визуальная цель ясна.
- У важных объектов есть количество и взаимное положение там, где это нужно.
- Свет и стиль не противоречат друг другу.
- Обязательные детали отделены от атмосферы.
- Дословный текст закавычен, его язык и направление чтения заданы.
- Чувствительные инварианты названы: идентичность, логотип, композиция, верстка.
- Ограничение «без лишнего текста и объектов» стоит обычным языком внутри брифа. Отдельный negative prompt добавляй только если у хоста есть документированное поле.
- Сгенерированные инфографика, продуктовое заявление, логотип, дата, карта или научный факт не выдаются как проверенные: либо утвержденные пользователем данные, либо явная пометка «иллюстративно».

## 10. Формат выдачи

Копируемый промт одним блоком, в таком порядке:

1. `Prompt` — полная инструкция генерации или редактирования.
2. `Suggested setup` — только реально полезные настройки: соотношение сторон, роли референсов, разрешение, отмеченная область. Не выдумывай флаги UI и параметры API.
3. `Preserve` — для правок и серий одной короткой строкой инварианты идентичности и верстки.

Не давай несколько альтернативных промтов, если пользователь не просил перебор направлений. На запрос доработки выдай минимальную адресную правку под названный дефект, а не переписанный промт.

Если пользователь явно просит payload API, JSON-промт или код — используй запрошенный формат и сначала уточни хост и вариант модели, когда важны поля и лимиты.

## Источники и границы

Дистиллировано из официального анонса Seedream 5.0 Pro и карточки модели ByteDance Seed, гайда Runway по Seedream 5.0 Pro и независимо протестированного гайда fal по Seedream 5.0 Lite; смежный локальный источник — навык `seedream-prompting` в `~/.codex/skills/seedream-prompting`.

Контролы платформы и варианты модели меняются. При конфликте с этим файлом приоритет у актуальной документации UI/API выбранного хоста, а выше нее — у последнего прямого указания пользователя и утвержденного brief lock.
