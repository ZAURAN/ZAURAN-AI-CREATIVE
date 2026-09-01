# Gemini Omni Flash — редактирование и расширение

Companion к `gemini-omni-flash.md`. Отличительная сила Omni — разговорное редактирование. Правила промптинга здесь **инвертируются** относительно генерации: коротко лучше, чем подробно.

## 1. Редактирование — правила Google дословно

> Simple prompts work best for video editing. Overly descriptive prompts can lead to unintended changes.

Собственные примеры правок Google — обрати внимание, насколько они короткие:

```text
Make this video anime
Put a fashionable hat on this person
Change the lighting to be more dramatic
Change the text on the sign to say "Omni Flash"
```

> When editing a specific aspect of the video, include **"Keep everything else the same"** to maintain visual consistency.

Пары avoid/simplify от Google:

| Avoid | Simplify to |
|---|---|
| `In the video of the man sitting on the sofa, please add a small black cat that runs from the right side of the screen, jumps onto his lap, and then he starts to stroke its head while looking down.` | `Add a cat that jumps onto his lap, he begins to pet it. Keep everything else the same.` |
| `Please remove the cell phone that the person is holding in their hand and fill in the background so it looks like they are just holding their hand empty.` | `Make the phone invisible. Keep everything else the same.` |
| `In the video showing the silver car driving down the road, please replace the silver paint with a metallic blue shade while making sure…` | `Change the car color to metallic blue. Keep everything else the same.` |

Заметь вторую пару: **«make it invisible» вместо «remove and inpaint»** — это собственная формулировка Google для удаления.

`Keep everything else the same.` — самая ценная фраза во всём корпусе: к ней независимо сходятся все источники. Для нескольких правок сразу — нумерованный список плюс одно предложение о сохранении.

**Связь с LOCKED / EDITABLE навыка.** Общее правило раздела 5 SKILL.md разделяет зоны на `LOCKED` и `EDITABLE`. У Omni это выражается так:

- `EDITABLE` → короткая фраза правки: `Change [X].`
- `LOCKED` → `Keep everything else the same.` плюс, при риске, точечное перечисление: `Do not change the character's face, outfit, or lighting.`

Не переноси в промпт Omni секционный блок `LOCKED:` / `EDITABLE:` — модель ждёт связную фразу, а не заголовки.

**Меняй одну переменную за ход.** Одновременная смена персонажа, локации, ракурса, стиля и погоды — названная причина дрейфа личности.

## 2. Что редактируется разговором

Из гайда DeepMind, каждое продемонстрировано:

- **Объекты** — `Change the butterfly to a bee.` → `Change the bee into a small swarm of fireflies.`
- **Камера** — `Change the camera angle to be over the violinist's shoulder.` · `Change the camera angle, a close-up on his shoes, quickly tilting up to medium shot, then widening.`
- **Действие и синхронизация** — `The lights of the apartments start turning on in sync with the music.`
- **Сложное добавленное движение** — `Edit this keeping everything the same. Add animated motion effects coming out of the skateboard.`
- **Стиль** — anime, claymation, watercolour; `Remake this video in anime aesthetic. Keep everything else the same.`
- **Субъекты** — `Change the ships to be made from white origami paper.` · `Change the astronaut to a sea anemone.` · `Change the small ships to stingrays.`

## 3. Два маршрута редактирования

**Маршрут 1 — с сохранением состояния, по видео, сгенерированному моделью. Работает во всех регионах.**

```python
res1 = client.interactions.create(model="gemini-omni-1.1-flash", input="A woman playing violin outdoors.")
res2 = client.interactions.create(
    model="gemini-omni-1.1-flash",
    previous_interaction_id=res1.id,
    input="Make the violin invisible."
)
```

Google: *«Each turn in the conversation produces a new video. The model understands context from prior turns, letting you make incremental changes like adjusting lighting, and swapping backgrounds, without re-describing the entire scene.»*

Требует, чтобы `store` остался по умолчанию — при `store=false` видео недоступно для правки через `previous_interaction_id`.

**Маршрут 2 — своё видео через Files API.**

```python
video_file = client.files.upload(file="Video.mp4")
while video_file.state == "PROCESSING":
    time.sleep(10); video_file = client.files.get(name=video_file.name)

interaction = client.interactions.create(
    model="gemini-omni-1.1-flash",
    input=[
        {"type": "video", "uri": video_file.uri, "mime_type": "video/mp4"},
        {"type": "text",  "text": "When the person touches the mirror, make the mirror ripple beautifully like liquid, and the person's arm turns into reflective mirror material"}
    ],
)
```

Загружаемое видео должно быть **≤ 10 секунд**. Google поставляет `prep_video.py` для обрезки и нормализации (максимум 1280×720 для ландшафта / 720×1280 для портрета, пропорциональное масштабирование, обрезка по таймкоду, опциональная смена fps).

**Маршрут 2 заблокирован регионально** — см. ниже.

## 4. Правка, привязанная к событию

Правку можно повесить на действие, а не на таймкод, за два хода:

```text
Ход 1: A person stands in front of a mirror. At 0:05, she touches the mirror then she does it again at 0:07, 0:08 and 0:09
Ход 2: The style of the video changes every time the person touches the mirror
```

## 5. Расширение

> With Gemini Omni 1.1 Flash you can extend videos with prompts like, `"Extend this video"` or `"The scene continues"`. You can extend videos by 10s, up to a total length of 40s.
>
> Omni creates an extension that keeps video, motion, characters and audio coherent by using the **last 10s of your original video as context. Some of the final frames in your input video will be edited** to make the transition seamless.

Окно контекста в 10 секунд — это то, что добавила версия 1.1; предыдущая модель смотрела только на **последнюю секунду**.

Минимальный вызов:

```python
interaction = client.interactions.create(
    model="gemini-omni-1.1-flash",
    input=[
        {"type": "video", "uri": video_file.uri, "mime_type": "video/mp4"},
        {"type": "text",  "text": "Continue the scene."}
    ],
)
```

Многоходовый вариант: `previous_interaction_id=turn1.id` плюс `"Continue the shot: the car turns smoothly onto a scenic coastal bridge at twilight as distant lighthouses begin to glow."`

Расширение с вводом нового персонажа — тег референса прямо внутри промпта расширения:

```python
input=[
    {"type": "video", "uri": video_file.uri,    "mime_type": "video/mp4"},
    {"type": "image", "uri": character_img.uri, "mime_type": "image/png"},
    {"type": "text",  "text": "Extend this video: have the character shown in <IMAGE_REF_0> enter the scene and wave."}
],
```

Более длинная версия, дополнительно фиксирующая камеру:

```text
[0-10s] The single continuous tracking shot continues unbroken from the exact same camera perspective behind the car. The silver sports car gently slows down as it approaches the shoulder of the road. Ahead on the roadside, the traveler shown in <IMAGE_REF_0> with her yellow backpack comes into view standing by the railing and waves cheerfully.
```

## 6. Правила промптинга расширения

- **Опиши звук**, особенно если он меняется: `The music continues into the chorus`
- **Скажи, продолжается сцена или идёт склейка**: `Show the same characters in the next scene`
- **Используй референсы** для точности или ввода новых персонажей: `The person shown in the reference image enters the scene` · `The dog in the reference video <VIDEO_REF_0> jumps onto the sofa`
- **`0s` = начало продлённой части**, а не всего ролика. При расширении 10-секундного клипа `After 2s cut to a new scene with the same characters` сработает на 12-й секунде абсолютного времени.
- Префикс, который использует сам Google: `Continue the video.`

Собственные промпты расширения Google, дословно:

```text
Camera slowly pulls out, forgotten dusty catacombs, dramatic music score.
Continue the video. Execute a cinematic optical dolly-zoom shot. The camera dollies forward while simultaneously zooming out, keeping the character's frozen shocked face locked at the exact same size. The long corridor of stone pillars in the background dramatically stretches and deepens with intense optical perspective distortion. Clean architecture, continuous unbroken shot.
Continue the video. The camera executes a fast mechanical snap-zoom directly into the character's wide eyes. Stylized cinematic camera control.
Continue the video. Time completely freezes into a static moment: the character, their windblown coat. The camera performs a smooth, high-speed 360-degree orbital rotation around the frozen character, showcasing dramatic 3D depth and parallax across the colonnade. Flawless continuity.
```

Каждый заканчивается формулой continuity. Копируй эту привычку.

## 7. Ограничения расширения — все

- **Длительность**: загружаемое видео для расширения ≤ 10 с (кроме многоходового режима по видео, сгенерированному моделью).
- **Только в хвост**: дописывается в конец. Нельзя дописать в начало и нельзя вставить в середину.
- **Диалог в загруженном видео**: **нельзя** расширить загруженное видео, где кто-то говорит, добавив новый диалог. Работает, если персонаж молчит либо промпт не добавляет реплик.
- **Многоходовая речь**: генерация речи **поддерживается** при расширении ранее сгенерированного видео через `previous_interaction_id`.
- **`task="extend"`**: только если промпт сам по себе не сработал. Накладывает жёсткие ограничения — **отключает мультимодальные референсы** и несовместим с `previous_interaction_id`. При его использовании опускай `aspect_ratio`, он наследуется от источника.
- **Регион**: расширение и редактирование **загруженного** видео недоступно в **EEA, Швейцарии, Великобритании — и, по собственному скиллу Google, части штатов США**. Редактирование и расширение видео, **сгенерированного моделью**, работает везде.
- **Flow вообще не умеет расширять клипы Omni** — «You can currently only extend Veo generated videos». Заявлено как «coming soon».

## 8. Звук на правках

Редактирование видео со звуком **сохраняет и адаптирует** этот звук. Чтобы пересоздать звук с нуля, аудиопоток нужно вырезать до загрузки — см. `gemini-omni-flash-audio.md`. Промптом это не достигается.

## 9. Экономика итераций

- **Правка дороже генерации.** Кредиты Flow: генерация 10 с = 30, **правка** = 40, потому что правка переобрабатывает каждый кадр против существующего клипа. **Несколько свежих дублей часто дешевле одного цикла «сгенерировал → правлю итеративно».** Уточнение: это сравнение генерации и **правки** — **расширение является свежей генерацией**, обусловленной последними 10 секундами, и биллится как генерация собственной длины, а не как правка.
- Контекст многоходового режима неглубокий — примерно **3 правки** в Flow до потери контекста.
- Черновики в **360p**, апскейл победителя.
- Стоп-лосс: если 10–15 вариаций не дали результата, пересматривай замысел, а не подкручивай формулировки.
