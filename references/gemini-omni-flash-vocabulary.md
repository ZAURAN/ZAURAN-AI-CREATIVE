# Gemini Omni Flash — словарь камеры, света и стиля

Companion к `gemini-omni-flash.md`. Два уровня. **Собственный словарь Omni крошечный** — десять терминов. Большая таксономия ниже взята из **общего** Vertex-гайда по видеопромптам, который покрывает Omni и Veo вместе, но сам оговаривается, что часть продвинутых ракурсов и объективов «не поддерживается официально».

## 1. Уровень 1 — собственный словарь Omni (prompt guide DeepMind)

Эти десять — единственные термины камеры, которые Google называет поимённо **именно для Omni**:

| Назначение | Термины |
|---|---|
| Непрерывность | `one continuous shot` · `oner` |
| Неподвижная камера | `static` · `locked off` · `fixed` |
| Движение | `push in` · `punch in` · `dolly zoom` |
| Характер камеры | `natural smartphone zoom` · `film camera` · `webcam style` |

Плюс формулировки из собственных примеров Google: `continuous smooth shot` · `Continuous, unbroken handheld shot` · `A drone shot of a mountain landscape at sunrise` · `A smooth cinematic transition` · `the camera pans across the mountains` · `In a single continuous shot` · `No scene cuts` · `whip-pans` · `snap-zoom` · `360-degree orbital rotation` · `optical dolly-zoom`.

**Словаря оптики в материалах, посвящённых именно Omni, нет вообще.** Понимает ли Omni термины объективов из уровня 2 — не проверено.

Рамка, которая управляет всем: *«With Veo, you need to share precise instructions to get the best results. But with Gemini Omni, you don't have to be as prescriptive with your prompt.»* Задавай эффект, детали модель разрешит сама.

**Связь с CINEDANCE.** `cinedance-optics.md` даёт дерево решений по FOV и языковые блоки — используй его, чтобы **выбрать** оптику осмысленно, но в промпт Omni выноси результат уровнем 1, а не полным телефото-стеком, рассчитанным на Seedance. Если сцена требует именно оптического описания, бери его из уровня 2 и держи в голове оговорку Google.

## 2. Уровень 2 — общий Vertex-гайд (Omni + Veo)

Применяй, когда уровня 1 не хватает. Оговаривай: сам гайд предупреждает, что часть терминов официально не поддержана и надёжность может плавать.

### Ракурсы камеры

| Термин | Эффект | Пример Google |
|---|---|---|
| Eye-level shot | нейтрально, на уровне человека | `eye-level shot of a woman sipping tea.` |
| Low-angle shot | сила, внушительность | `low-angle tracking shot of a superhero landing.` |
| High-angle shot | малость, уязвимость | `high-angle shot of a child lost in a crowd.` |
| Bird's-eye / top-down | как карта | `bird's-eye view of a bustling city intersection.` |
| Worm's-eye view | высота, величие | `worm's-eye view of towering skyscrapers.` |
| Dutch / canted angle | тревога, дезориентация | `dutch angle shot of a character running down a hallway.` |
| Close-up | плотно, обычно лицо | `close-up of a character's determined eyes.` |
| Extreme close-up | одна мелкая деталь | `extreme close-up of a drop of water landing on a leaf.` |
| Medium shot | по пояс, стандарт диалога | `medium shot of two people conversing.` |
| Full shot / long shot | в полный рост | `full shot of a dancer performing.` |
| Wide / establishing shot | субъект в среде | `wide shot of a lone cabin in a snowy landscape.` |
| Over-the-shoulder | `over-the-shoulder shot during a tense negotiation.` | |
| Point-of-view | `POV shot as someone rides a rollercoaster.` | |

### Движения камеры

| Термин | Значение | Пример |
|---|---|---|
| Static / fixed | без движения | `static shot of a serene landscape.` |
| Pan (left/right) | поворот по горизонтали с точки | `slow pan left across a city skyline at dusk.` |
| Tilt (up/down) | поворот по вертикали с точки | `tilt down from the character's shocked face to the revealing letter in their hands.` |
| Dolly (in/out) | камера физически приближается/удаляется | `dolly out from the character to emphasize their isolation.` |
| Truck (left/right) | движение вбок параллельно субъекту | `truck right, following a character as they walk along a busy sidewalk.` |
| Pedestal (up/down) | движение по вертикали с сохранением перспективы | `pedestal up to reveal the full height of an ancient, towering tree.` |
| Zoom (in/out) | меняется фокусное, камера стоит | `slow zoom in on a mysterious artifact on a table.` |
| Crane shot | вертикальные или размашистые дуги | `crane shot revealing a vast medieval battlefield.` |
| Aerial / drone shot | большая высота, плавный полёт | `Sweeping aerial drone shot flying over a tropical island chain.` |
| Handheld / shaky cam | реализм, непосредственность, тревога | `handheld camera shot during a chaotic marketplace chase.` |
| Whip pan | очень быстрый смазанный поворот, переход | `whip pan from one arguing character to another.` |
| Arc shot | круговая траектория вокруг субъекта | `arc shot around a couple embracing in the rain.` |

### Оптика и оптические эффекты

| Термин | Эффект | Пример |
|---|---|---|
| Wide-angle lens | широкий угол, подчёркнутая перспектива | `wide-angle lens shot of a grand cathedral interior, emphasizing its soaring arches.` |
| Telephoto lens | узкий угол, сжатая перспектива, изоляция | `telephoto lens shot capturing a distant eagle in flight against a mountain range.` |
| Shallow depth of field | узкая плоскость фокуса, боке | `portrait of a man with a shallow depth of field, their face sharp against a softly blurred park background with beautiful bokeh.` |
| Deep depth of field | всё в фокусе | `landscape scene with deep depth of field, showing sharp detail from the wildflowers in the immediate foreground to the distant mountains.` |
| Lens flare | блики от яркого источника | `cinematic lens flare as the sun dips below the horizon behind a silhouetted couple.` |
| Rack focus | перевод фокуса между планами в одном кадре | `rack focus from a character's thoughtful face in the foreground to a significant photograph on the wall behind them.` |
| Fisheye | сильная бочкообразная дисторсия | `fisheye lens view from inside a car, capturing the driver and the entire curved dashboard and windscreen.` |
| Vertigo / dolly zoom | тележка едет в одну сторону, зум одновременно идёт в **противоположную** — в этом весь механизм; субъект остаётся того же размера, фон растягивается | `vertigo effect (dolly zoom) on a character standing at the edge of a cliff, the background rushing away.` |

### Свет

- **Естественный** — `soft morning sunlight streaming through a window` · `overcast daylight` · `moonlight`
- **Искусственный** — `warm glow of a fireplace` · `flickering candlelight` · `harsh fluorescent office lighting` · `pulsating neon signs`
- **Кинематографический** — `rembrandt lighting on a portrait` · `film noir style with deep shadows and stark highlights` · `high-key lighting for a bright, cheerful scene` · `low-key lighting for a dark, mysterious mood`
- **Эффекты** — `volumetric lighting creating visible light rays` · `backlighting to create a silhouette` · `golden hour glow` · `dramatic side lighting`

### Тон и настроение

`Happy/joyful` bright, vibrant, cheerful, uplifting, whimsical · `Sad/melancholy` somber, muted colors, slow pace, poignant, wistful · `Suspenseful/tense` dark, shadowy, quick cuts, unease, thrilling · `Peaceful/serene` calm, tranquil, soft, gentle, meditative · `Epic/grandiose` sweeping, majestic, dramatic, awe-inspiring · `Futuristic/sci-fi` sleek, metallic, neon, technological, dystopian, utopian · `Vintage/retro` sepia tone, grainy film, эстетика эпохи («1950s Americana», «1980s vaporwave») · `Romantic` soft focus, warm colors, intimate · `Horror` dark, unsettling, eerie — помни про контент-фильтры

### Художественный стиль

- **Фотореализм** — `ultra-realistic rendering` · `shot on 8K camera`
- **Кинематограф** — `cinematic film look` · `shot on 35mm film` · `anamorphic widescreen`
- **Анимация** — `Japanese anime style` · `classic Disney animation style` · `Pixar-like 3D animation` · `claymation style` · `stop-motion animation` · `cel-shaded animation`
- **Художественные направления** — `in the style of Van Gogh` · `surrealist painting` · `Impressionistic` · `Art Deco design` · `Bauhaus aesthetic`
- **Конкретные образы** — `gritty graphic novel illustration` · `watercolor painting coming to life` · `charcoal sketch animation` · `blueprint schematic style`

### Амбиенс

- **Палитры** — `monochromatic black and white` · `vibrant and saturated tropical colors` · `muted earthy tones` · `cool blue and silver futuristic palette` · `warm autumnal oranges and browns`
- **Атмосфера** — `thick fog rolling across a moor` · `swirling desert sands` · `gentle falling snow creating a soft blanket` · `heat haze shimmering above asphalt` · `magical glowing particles in the air` · `subsurface scattering on a translucent object`
- **Фактуры** — `rough-hewn stone walls` · `smooth, polished chrome surfaces` · `soft, velvety fabric` · `dewdrops clinging to a spiderweb`

### Время

Темп `slow-motion` · `fast-paced action` · `time-lapse`. Эволюция `a flower bud slowly unfurling` · `ice melting` · `dawn breaking, the sky gradually lightening`. Ритм `pulsating light` · `rhythmic movement`.

### Монтажные термины

`match cut` · `jump cut` · `establishing shot sequence` · `montage` · `split diopter effect`

## 3. Текст в кадре

Google заявляет рендер текста как сильную сторону и даёт рецепты; **model card называет «rendering perfectly accurate text» известной слабостью**, а инструментированный тест показал, что логотипы и текст упаковки приходят правдоподобной кашей. **Побеждает model card.**

Практический коридор: **короткие английские строки в кавычках на плоской поверхности фронтально к камере.** Длинные строки, текст упаковки, логотипы, брендовые знаки и мелкие вывески в сцене вырождаются.

Собственные текстовые промпты Google:

```text
One word on the screen at a time: "did, you, know, that, Omni, can, do, awesome, text?" Each word appears for 1s with a different animated style. No dialogue.
There is a street sign that says: "This is an AI generation by Omni", there is a storefront that says: "All you need AI", there's a car with the number plate: "OMNI1.1"
word by word, one word on a the screen at a time: did, you, know, that, this, model, can, do, pretty, good, text!? each word appears with a different animated style, perfect pacing to a rhythm, sizzle reel.
```

Если текст будет появляться в кадре естественно — вывески, экраны — **задай, что именно на нём написано**, вместо того чтобы оставлять это на волю модели.

## 4. Что нельзя называть

- **Реальные публичные лица** — детерминированный блок, обходных формулировок нет. Описывай признаки: возрастной диапазон, телосложение, гардероб, волосы, выражение.
- **Именованное IP** — «Studio Ghibli style» → описывай вместо этого («hand-painted watercolour»).
- **Названия камер и брендов техники** — «DJI Mavic Pro» → нужный глагол движения.
- Практики сообщают, что **щит оригинальности** снижает ложные блокировки: `…not based on any existing franchise or real person.`

Для нескольких брендов и логотипов действует общее правило навыка про `brand-surface contract`: какой знак принадлежит какому физическому носителю и где он запрещён.

## 5. Физика

Называй механизм, а не настроение: `Water splashes realistically out of the glass with realistic droplet physics.` Проси **одно** физическое событие — инструментированные тесты показывают, что цепочки «столкновение и остановка» проваливаются и у Omni, и у Veo.

## 6. Длина промпта

Технический потолок огромен (контекст 1 048 576 токенов); практики советуют держаться **до ~50 слов на одну генерацию**. Собственные примеры Google — 30–80 слов на генерацию и 5–15 на правку. Не путай с мета-инструкцией `Be extremely detailed…`: она просит добавить деталей **модель**, это не разрешение писать 500 слов.
