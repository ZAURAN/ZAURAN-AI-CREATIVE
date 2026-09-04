# Шаблоны визуализации сценария

Три промта из личной базы пользователя (Notion «✍️ Промты», оценка ⭐⭐⭐). Модель-независимые по форме; под конкретную модель (Nano Banana Pro / GPT Image / Seedream) финальную сборку делает `zauran-ai-creative` по её контракту. Здесь — форма и правила заполнения.

## 1. Ч/б раскадровка со скетчами (6–9 кадров)

Зачем: препродакшен и согласование сцены с клиентом до дорогих генераций. Один лист — одна сцена.

Правила: заменить всё в квадратных скобках; описание персонажей копировать **одинаковым текстом** во все кадры; планы брать из `SCRIPT_vN.md`.

```text
black and white storyboard sheet, pencil sketch style, cinematic film storyboard, multiple panels layout (6-9 frames), rough hand-drawn graphite lines, visible sketch strokes, slightly messy artist lines, grayscale shading, no color

each panel contains a different shot of the same scene, consistent characters and environment across all frames

scene: [ОПИСАНИЕ СЦЕНЫ]

characters:
[ОПИСАНИЕ ПЕРСОНАЖЕЙ — одинаковое для всех кадров, из PASSPORT §A]

environment:
[ЛОКАЦИЯ — из CANON §4]

shots description:

frame 1: wide shot, establishing shot, [что происходит]
frame 2: medium shot, [действие]
frame 3: close-up, [деталь или эмоция]
frame 4: low angle shot, [усиление драматургии]
frame 5: over the shoulder shot, [перспектива]
frame 6: action shot, [движение или ключевой момент]
frame 7: behind shot, [вид сзади]
frame 8: focus shot, subject centered, [главный акцент]
frame 9: final cinematic frame, [финальный визуальный акцент]

add small technical captions under each frame (like "wide shot", "close-up", "over shoulder"), handwritten style

cinematic composition, film pre-production storyboard look, professional director sketch style

no color, no text except small shot labels, no watermark
aspect ratio 16:9
```

## 2. Character turnaround sheet

Зачем: визуальный паспорт героя (PASSPORT §G) — 3 вида в рост, 6 ракурсов головы, 6 деталей одежды. Дальше лист = референс роли «персонаж».

Правила: описание героя (возраст, пол, причёска, одежда, телосложение из PASSPORT §A) — в начало; соотношение 16:9 или 3:2, чтобы влезла сетка.

```text
[ОПИСАНИЕ ГЕРОЯ из PASSPORT §A]

A high-definition, clean, minimalist character design board / character turnaround reference sheet, set against a pure white background. The overall presentation should resemble a professional game art character modeling sheet, fashion design reference page, character design sheet, or character turnaround board. The layout should be neat and well-organized, with clearly divided information sections, a realistic and premium visual quality, consistent lighting, and strict character consistency throughout.

On the left side of the composition, show the character's full-body three-view turnaround, occupying the main visual area, including:
1. Front full-body standing pose
2. Left-side full-body standing pose
3. Back full-body standing pose

All three figures must be the exact same character, with identical facial features, hairstyle, clothing, body shape, and height proportions. The standing pose should feel natural, with both arms hanging naturally at the sides. This should be suitable as a character modeling reference. The camera angle should be eye level, with neutral studio lighting, no obstruction, no exaggerated perspective, and no complex background.

The right side of the composition should be divided into two sections:

In the upper-right section, place six headshot / head-angle reference images of the same character, arranged neatly to show different head perspectives, including:
- Front-facing portrait
- Slight downward angle showing the top of the head
- Back of the head / rear head view
- Left-side facial profile
- A near-side-angle comparison view
- 3/4 profile portrait

The head references should have clear facial features, visible hair parting, and consistent facial structure, making them suitable as head design references.

In the lower-right section, place six close-up detail images of the character, arranged into a clean grid, showing key design details, including:
- Close-up of the upper garment fabric texture
- Front close-up of the lower-body clothing
- Close-up of the hip / tailoring detail
- Close-up of the leg or skin texture detail
- Close-up of the eyes or facial feature details
- Full close-up of the shoes as a standalone item

All detail images must match the main character's outfit and appearance exactly. Materials should look realistic, and the details should be clean and precise, suitable as clothing and accessory modeling references.

Overall style requirements:
Minimalist, professional, realistic, unified, clean, and premium, similar to a character design board, fashion design reference sheet, 3D character modeling reference page, or character turnaround presentation board.
The character edges should be sharp, garment shapes should be clearly defined, hair strands should appear natural, skin should look refined, and material rendering should be accurate. The overall layout should have generous white space, as if it were made by a professional concept artist.
```

## 3. Студийная раскадровка товара — 7 панелей

Зачем: когда «герой» ролика — продукт. Одна картинка: hero-кадр сверху + сетка 2×3 (макро, логотип, масштаб, ритм, застывшее движение, силуэт). Даёт визуальный паспорт продукта для CANON §6.

Форма: из фото товара, ракурсы по словарю (`extreme close-up / macro`, `low angle`, `profile`, `fill the frame`). Полный текст промта — в Notion пользователя «Студийная раскадровка товара — 7 панелей»; при необходимости пользователь вставляет его сам, скилл здесь только маршрутизирует.
