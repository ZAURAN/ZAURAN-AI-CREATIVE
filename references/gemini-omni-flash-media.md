# Gemini Omni Flash — привязка медиа: кадры, референсы, теги

Companion к `gemini-omni-flash.md`. Как объяснить Omni, для чего служит каждое загруженное изображение или видео. Ошибка здесь — самая частая причина жалоб «он проигнорировал мой референс» и «он взял фото персонажа как первый кадр».

## 1. Два механизма

**Позиционный** — порядок частей в `input`. Два изображения плюс описание перехода = интерполяция первый→последний кадр. Два изображения плюс описание сцены = референсы субъектов. Модель выводит сама.

**Теговый** — явные метки внутри строки промпта. Используй их всегда, когда медиа больше двух единиц или когда роли не очевидны из предложения.

**Связь с правилом `@Тег` навыка:** внутри промпта Omni понимает только официальные метки ниже. Теги пользователя (`@Шот с норм лицом`) перечисляй в сопроводительном списке ролей **вне промпта**, сопоставляя их меткам. Это то же исключение, что действует для Ref2VA в MiniMax H3.

## 2. Простые теги — рекомендованная Google форма

| Тег | Значение | Пример |
|---|---|---|
| `<FIRST_FRAME>` | это изображение — стартовый кадр | `<FIRST_FRAME> a woman is walking` |
| `<LAST_FRAME>` | это изображение — финальный кадр перехода. **Обязательно вместе с `<FIRST_FRAME>`** | `<FIRST_FRAME> <LAST_FRAME> a woman is walking` |
| `<IMAGE_REF_N>` | это изображение — референс, **N считается с 0** | `in the style of <IMAGE_REF_0> a woman <IMAGE_REF_1> is walking` |
| `<VIDEO_REF_N>` | это видео — референс персонажа/объекта, **N считается с 0** | `the person in <VIDEO_REF_0> is playing the violin` |

Пример Google на шесть референсов, теги плюс таймкоды:

```text
[0-3s] A studio fashion sequence. Starting with woman <IMAGE_REF_0>, she is holding <IMAGE_REF_1>
[3-6s] Then we see the man <IMAGE_REF_2> holding <IMAGE_REF_3>
[6-10s] And finally another woman <IMAGE_REF_4> who is holding <IMAGE_REF_5> while walking.
```

Проверенная в cookbook привязка «персонаж↔аксессуар», которая, по отчёту, связала каждую пару правильно **без смешения личностей**:

```text
In a single unbroken scene around a twilight campfire in a forest:
<IMAGE_REF_0> is wearing <IMAGE_REF_5>,
<IMAGE_REF_2> is wearing <IMAGE_REF_3>,
and <IMAGE_REF_4> is wearing <IMAGE_REF_1>.
They smile happily together as embers float into the evening sky.
```

## 3. Правило нумерации, которого нет в прозе Google

Из собственного `generate_video.py` Google:

```python
img_start_num = (2 if last_frame and last_frame != first_frame else 1) if first_frame else 0
ref_parts.append(f"<IMAGE_REF_{idx}>@Image{img_start_num + idx + 1}")
```

- `<IMAGE_REF_N>` считается **с 0 и только по референсным изображениям**.
- `@ImageN` считается **с 1 и по всем изображениям в массиве `input`, включая кадры-якоря**.

То есть при наличии первого и последнего кадра `<IMAGE_REF_0>` соответствует `@Image3`. Если пишешь объявления `@ImageN` вручную — не забудь посчитать кадры.

Порядок частей, который всегда отправляет скрипт Google: первый кадр → последний кадр → референсные изображения → исходное/расширяемое видео → референсные видео → **текст последним**. Когда тегов в промпте нет, скрипт подставляет их сам: расширение получает `[# Sources <VIDEO_0>@Video1]`, first+last получает `<FIRST_FRAME> <LAST_FRAME> `, только first — `<FIRST_FRAME> `.

## 4. Синтаксис явного объявления

Для сложных случаев с несколькими ролями. **Объявляй в начале промпта.**

```text
[# Sources <FIRST_FRAME>@Image1]                              первое изображение = стартовый кадр
[# Sources <FIRST_FRAME>@Image1 <LAST_FRAME>@Image2]          первое = старт, второе = финал
[# Sources <FIRST_FRAME>@Image1 <LAST_FRAME>@Image1]          одно изображение с обеих сторон → ЗАЦИКЛЕННОЕ ВИДЕО
[# Sources <FIRST_FRAME>@Image1] [# References <IMAGE_REF_0>@Image2]
[# Sources <VIDEO_0>@Video1]                                  основное исходное видео для правки
[# Sources <PREVIOUS_VIDEO>@Video1]                           видео предыдущего хода, для расширения
[# References <IMAGE_REF_0>@Image1]
[# References <IMAGE_REF_1>@Image2]
[# References <IMAGE_REF_0>@Image1 <IMAGE_REF_1>@Image2]
[# References <VIDEO_REF_0>@Video1]
[# References <IMAGE_REF_0>@Image1 <VIDEO_REF_0>@Video1]
```

Затем усиль естественным языком **в конце** промпта:

- стартовый кадр → `Use this image as the starting frame.`
- зацикливание → `Use this image as the first frame and the last frame.`
- референсные изображения → `Use the given image(s) as references for video generation. The images should not be used as literal initial frames.`
- референсные видео → `Use the given video(s) as references. Do not use them as a source for video editing.`

Два разобранных примера Google:

```text
[# Sources <FIRST_FRAME>@Image1] [# References <IMAGE_REF_0>@Image2] a woman <IMAGE_REF_0> is walking. Use Image1 as the starting frame. Use Image2 as a reference for the video generation.
```

```text
[# References <IMAGE_REF_0>@Image1 <VIDEO_REF_0>@Video1] The woman in <VIDEO_REF_0> is playing the violin shown in <IMAGE_REF_0>. Use Video1 as a character reference and Image1 as an object reference.
```

## 5. Референс ≠ первый кадр

Самое непонимаемое поведение модели. Cookbook Google дословно:

> *«In Reference-to-Video workflows, the provided image is **not** used as the literal starting frame. Instead, the model extracts the subject, character identity, or artistic composition and embeds it into a completely different environment or camera perspective.»*

Инструментированный тест подтверждает: референсный кадр плюс запрос орбиты дал того же субъекта и тот же верстак, но сдвинутую камеру и исчезнувшее окно. **`<IMAGE_REF_N>` задаёт личность и стиль, но не фиксирует пиксели.** Нужен буквальный стартовый кадр — только `<FIRST_FRAME>`.

## 6. Интерполяция первого и последнего кадра

```python
interaction = client.interactions.create(
    model="gemini-omni-1.1-flash",
    input=[
        {"type": "image", "data": first_frame_b64, "mime_type": "image/jpeg"},
        {"type": "image", "data": last_frame_b64,  "mime_type": "image/jpeg"},
        {"type": "text",  "text": "A smooth cinematic transition from a lush green forest at sunrise to a snowy forest under a starry night sky."}
    ],
)
```

По release notes интерполяция использует задачу `image_to_video` и **до 2 изображений**.

Как это писать, по DeepMind: *«Clearly define what is in your initial frame, specify the exact camera movement or transition path that takes place in between, and state precisely what the final frame should reveal.»* Их пример:

```text
A close-up low-angle shot of a stylish drummer in a beige suit playing a red drum kit in a grand hall transitions as the camera whip-pans to the side, revealing an older saxophonist playing alongside a ballet dancer spinning in a white outfit under soft purple stage lights. One continuous shot, no jump cuts.
```

Обрати внимание на continuity lock в конце — Google добавляет его почти к каждому опубликованному примеру со сложным движением. Копируй эту привычку.

Одно изображение в обеих ролях → **зацикленный** клип.

## 7. Референсные видео

- Идеально ~**3 секунды** каждое, до **3 клипов**. Гайд Google говорит «maximum», собственный скилл Google говорит *«though longer videos are fine»* и *«though more can also be used»* и никогда не блокирует. Считай 3×3 с надёжным диапазоном; на Vertex 3 видео — жёсткая спецификация.
- **Звук в референсном видео игнорируется.**
- **Ссылаться и рассуждать сразу по нескольким видео не поддерживается** — Google предупреждает, что это *«may result in degraded model performance or unexpected outputs»*. Допуск на 3 клипа — про внешность, а не про кросс-видео рассуждение.
- Референсные видео лучше всего работают именно с внешностью (likeness).

Пример Google с тремя референсными видео и тремя изображениями персонажей:

```text
Use the three uploaded videos of dancers and replace them with the provided characters. Have them perform their individual dances from the reference videos, all together in the large, open space from the provided image.
```
```text
The dog character dog.png should do the classical dance from dance3.mp4. The octopus octo.png should do the hip hop dance from dance1.mp4, and the bear bear.png should do the breakdance from dance2.mp4. The final result should be one continuous shot with no scene cuts.
```

## 8. Сколько референсных изображений — честно не разрешено

Четыре цифры, ни одна не авторитетна для Gemini API: проза cookbook говорит до 5; собственный пример гайда Omni использует 6; model card Vertex — максимум 10 на промпт; один хост — 7. `generate_video.py` Google **не проверяет количество изображений вообще**. Совет практиков — держаться **2–3**, чтобы личности не усреднялись.

Не называй пользователю жёсткий лимит. Говори: 6 продемонстрировано самим Google, больше ~3 начинает смешивать.

## 9. Консистентность персонажа — три маршрута

1. **Внутри одного клипа** — привязка `<IMAGE_REF_N>` / `<VIDEO_REF_N>`, как в примере с костром.
2. **Между ходами** — `previous_interaction_id`. Google: *«The model maintains full state context, applying targeted modifications while preserving visual continuity.»* Работает и **между моделями**: `id` интеракции изображения Nano Banana можно передать прямо в Omni как `previous_interaction_id`, без извлечения байтов.
3. **В Flow** — именованные персонажи: `@` плюс имя в поле промпта, `@me` для собственного аватара. Пример: `@CaptainZoro walking through a futuristic city.` Рекомендации Flow: *«provide subject or product references on a plain or segmented background»* и *«Your text prompt should complement, not contradict, your visual inputs.»*

Полевые identity lock, которые по отчётам практиков работают:

```text
Use the uploaded image as the character identity reference. Preserve the face, hairstyle, glasses, clothing, body proportions.
Keep the same character identity in every shot. Keep the same clothing color, hairstyle, face, and glasses.
```

и на ходе правки: `Do not change the character's face, outfit, or lighting.`

Дрейф ожидаем примерно после четырёх шотов; давай референс на каждый шот.

## 10. Сторибординг как референс

Отдельный механизм из гайда DeepMind — подать изображение раскадровки:

```text
Show me in this story. Follow the story exactly in order starting top left. Entire story in 10 seconds. Cinematic
```

Связка с навыком: если раскадровка идёт в видеогенератор, действует общее правило `storyboard-to-video.md` — готовь отдельно `review board` и `clean generation pack`. Стрелки, подписи и рамки, уже нарисованные на борде, negative prompt не уберёт, а у Omni негативного поля вообще нет.

## 11. Перенос стиля с референсного видео

```text
Create a four-part stylistic progression of the video reference that begins with a vibrant colored crayon aesthetic, featuring rich, waxy, textured strokes and playful, hand-drawn character designs against a backdrop of heavily granulated paper. Transition seamlessly into a graphite pencil sketch on textured paper, utilizing cross-hatching, varying line weights, and a 12fps "line boiling" effect to emphasize a hand-drawn feel. Next, morph into a hyper-realistic 3D translucent glass style, characterized by complex light refractions, caustic patterns, and soft internal glows within a minimalist studio setting. Conclude the sequence with a tactile risograph print look, applying a limited three-color palette, grainy halftone textures, and intentional registration overlays for a retro, mechanical finish.
```

Простой перенос стиля DeepMind формулирует одной строкой: попроси применить новый стиль — anime, claymation, watercolour — сохранив исходное движение и детали.

## 12. Запрещённое медиа

- Загрузка и редактирование изображений с **определёнными узнаваемыми людьми** — блок глобально.
- Загрузка и редактирование изображений с **несовершеннолетними** — блок в EEA, Швейцарии и Великобритании.
- **Видео с YouTube** как источник — не поддерживается.
- **Аудиореференсы** — в API не поддерживаются (существуют только в Flow и приложении Gemini).
