# Seedance 2.5 — рабочая инструкция

Используй этот документ для Dreamina Seedance 2.5: text-to-video, multimodal reference, first/last frame, keyframes, storyboard, video editing, extension и длинных роликов. Источники: официальные `Dreamina Seedance 2.5 User Guide` и `Dreamina Seedance 2.5 Prompt Guide` (обновления 31 июля и 4 августа 2026).

## 1. Сначала выбери режим

- **Text-to-video:** сюжет задается текстом; референсов нет.
- **Multimodal reference:** изображения, видео и аудио задают конкретные роли.
- **First frame / first-and-last frames:** первый кадр фиксирует старт; последний — финал.
- **Keyframes / storyboard:** несколько кадров задают порядок состояний, композицию и движение.
- **Video editing:** исходное видео — единственный master; меняется только явно заданная область.
- **Video extension:** новый сегмент продолжается после последнего кадра или до первого кадра исходника.
- **Ultra Long Video:** история длительностью до 180 секунд; проектируй ее как сцены и стадии.

Не смешивай режимы неявно. В начале промпта назови задачу и роль master-материала.

## 2. Подготовь материалы

Технические пределы Seedance 2.5:

- до 50 материалов суммарно;
- до 30 изображений, каждое не больше 4K;
- до 10 видео, суммарно не более 30 секунд;
- до 10 аудиоклипов, суммарно не более 30 секунд;
- для video editing рекомендуется source video короче 20 секунд и 1–5 reference images.

Рекомендуемые устойчивые диапазоны:

- 1–8 разных субъектов в image references;
- 1–5 субъектов в video references, по 5–10 секунд на субъект;
- только релевантные диалоги, тембр, ambience или музыка в audio references;
- разные виды одного субъекта лучше передавать отдельными изображениями, а не коллажем.

Больший объем допустим, но снижает стабильность. Не загружай материал без функции.

## 3. Назначь роль каждому референсу

Каждый файл упомяни в промпте и задай, что именно брать и что игнорировать:

```text
REFERENCE MAP
@Image 1 defines <Character A>'s facial features and hairstyle. Do not use its background.
@Image 2 defines <Character A>'s clothing only.
@Video 1 defines the motion, camera path and pacing only. Do not copy its character identity.
@Audio 1 defines <Character A>'s voice and delivery only. Do not add its background music.
```

Для нескольких сцен сначала создай именованные профили субъектов, затем для каждой сцены перечисли только нужные материалы. Цель — помочь модели выбрать правильные референсы для текущей сцены, а не показать все материалы одновременно.

Не полагайся на подписи внутри изображений. Текстовый `@Image N` / `@Video N` / `@Audio N` mapping обязателен.

## 4. Базовая формула промпта

Официальное ядро:

```text
Subject + Action or Event + Scene and Environment + Visual Style + Camera Movement/Cut + Audio
```

Для production-задачи пиши в таком порядке:

1. `GENERATION GOAL` — тип видео и одна фраза о главном событии.
2. `REFERENCE MAP` — роль и исключения каждого материала.
3. `SUBJECT PROFILES / OBJECT LEDGER` — идентичность и точное число якорей.
4. `INITIAL STATE` — видимое состояние в начале.
5. `TIMELINE / STAGES` — последовательные интервалы или стадии.
6. `END STATE` — проверяемая финальная композиция.
7. `MAINTAIN CONSISTENCY` — только глобальные инварианты.
8. `AUDIO` — диалог, язык, тембр, ambience, SFX, BGM или явное отсутствие музыки.

Параметры, доступные в интерфейсе/API, не дублируй в художественном тексте без необходимости.

## 5. 30 секунд и timestamp-контроль

Для нескольких событий разбивай ролик на последовательные стадии. В каждой стадии должны быть:

```text
[Stage N | 0–8 seconds]
Initial/continued state: <что уже существует и не меняется>.
Primary event: <одно главное изменение>.
End state: <что непосредственно видно в конце стадии>.
```

Правила тайминга:

- интервалы последовательны и не пересекаются;
- timestamp — бюджет события, а не гарантированный монтажный кадр;
- допустимы `0–3 seconds`, `At 5 seconds`, `Three seconds after...`;
- не требуй невозможную частоту вроде «три действия за одну секунду»;
- слишком мало содержания дает модели лишнюю свободу, слишком много вызывает пропуски и лишние cuts;
- переход между стадиями наследует положение людей, ownership реквизита, screen direction и состояние сцены.

Для ролика до 180 секунд сначала составь scene map, затем отдельный stage-план для каждой сцены. Не превращай 180 секунд в один неструктурированный промпт.

## 6. First frame, last frame и keyframes

В multimodal reference mode можно явно назначить кадры без отдельного режима:

```text
@Image 1 is the first frame. It defines the opening composition, subject positions, poses, prop state, scene and camera direction.
@Image 2 is the last frame. It defines the ending composition, subject positions, poses, prop state, scene and camera direction.
@Image 3 defines <specific identity/material> only. It must not replace the compositions defined by @Image 1 or @Image 2.

Starting from @Image 1, <one continuous event>. Reach @Image 2 naturally.
Maintain continuity in <identity, clothing, object count, ownership, layout and camera direction>.
```

- Описывай первый и последний кадры отдельно; не пиши только `@Images 1 and 2 are first and last`.
- Оба кадра должны иметь одинаковый aspect ratio; иначе финал может растянуться.
- Output aspect ratio наследуется от первого изображения; duration задается отдельно.
- Дополнительные references дополняют только назначенные атрибуты и не перезаписывают композиции якорных кадров.
- Boundary frames должны визуально стыковаться, но не обязаны быть pixel-identical.

Для последовательности:

```text
Use @Image 1 through @Image N as keyframes in this order.
@Image 1 defines <state 1>.
@Image 2 defines <state 2>.
...
Connect the key states through continuous physical actions without duplicating subjects.
```

Отдельные clean keyframes обычно надежнее одной grid-board. Если используется storyboard grid, она должна быть простой; composition, shot size, camera movement и action все равно опиши текстом. Аннотированную review board не передавай как generation reference.

## 7. Video editing

Исходное видео объяви единственным master. Aspect ratio и приблизительная длительность наследуются автоматически и отдельно не задаются; возможна разница до ~0,3 секунды из-за обработки boundary frames.

```text
[EDIT GOAL]
Edit @Video 1. @Video 1 is the sole source and editing master.

[EDIT SCOPE]
Only from <time range>, <add/remove/replace/adjust> <object, region or audio category>.

[LOCKED]
Preserve <identity, face, clothing, position, size, motion, camera, cuts, event order, unedited objects and audio categories> from @Video 1.
```

Для замены фона зафиксируй silhouette субъекта и occlusion. Для audio edit назови speaker/категорию, точное изменение и звуки, которые нужно сохранить. Локальная правка не разрешает перестройку остального ролика.

## 8. Video extension

Для forward extension первый кадр нового сегмента продолжает последний кадр source video. Для backward extension последний кадр нового сегмента соединяется с первым кадром source video.

```text
@Video 1 is the source video to extend forward.
Extend @Video 1 forward. The first frame of the extended segment directly continues from the last frame of @Video 1.
Maintain <pose and orientation, prop position, background layout, camera composition, lighting and motion direction> at the boundary.
Then, <new action/event/camera/audio>.
Keep each subject as the same continuous instance; do not duplicate, split or change its number of parts.
```

Дополнительные материалы могут дополнять identity, clothing, prop или audio, но не имеют права перезаписывать boundary frame исходного видео. Для backward extension также запрети преждевременное появление объектов, которые в source video возникают позже.

Официальный workflow поддерживает extension отдельных видео до 30 секунд за операцию и повторные продолжения до 60 секунд; Ultra Long Video — отдельный режим до 180 секунд. Проверяй фактические возможности текущего интерфейса перед обещанием результата.

## 9. Audio и текст

- Явно указывай speaker, реплику, язык и характер подачи.
- Если язык критичен, повтори требование естественного произношения и запрет смешения языков.
- Разделяй dialogue, voice/timbre, ambience, SFX и BGM.
- Для ролика без музыки укажи `no background music`; для ролика без титров — `no subtitles or on-screen text`.
- При audio editing сохраняй lip sync и названные категории звука.
- Не проси модель генерировать точный брендовый текст там, где надежнее добавить его на посте.

## 10. Что поддерживает Seedance 2.5

При наличии соответствующего UI/model endpoint можно использовать:

- timestamp text control;
- pure audio driving;
- удаление/замену BGM при сохранении других звуков;
- локальное video editing и edit with marks;
- subject/background replacement;
- perspective modification;
- voice/timbre reference и multi-person reference;
- green-screen editing;
- Clay Renderer / blockout reference для camera path, staging и motion trajectory;
- seamless transition между двумя видео;
- multi-grid storyboard;
- Ultra Long Video до 180 секунд.

Не утверждай, что функция доступна в конкретном аккаунте или API, пока не увидел ее в текущем интерфейсе/документации endpoint.

## 11. QA перед и после генерации

Перед отправкой:

- у каждого материала есть одна явная роль и exclusions;
- каждый субъект назван одинаково во всех сценах;
- object ledger и ownership не противоречат таймлайну;
- интервалы последовательны и не перегружены;
- first/last frames имеют одинаковый aspect ratio;
- edit scope отделен от locked content;
- extension начинается или заканчивается точным boundary state;
- audio categories не конфликтуют;
- negatives короткие и проверяемые.

После генерации проверь весь ролик и contact sheet:

- правильные референсы в каждой сцене;
- identity, clothing, object count и ownership;
- наблюдаемые end states стадий;
- continuity на границах и screen direction;
- camera path, cuts и длительность;
- диалог, язык, lip sync, ambience, SFX и BGM;
- отсутствие случайных субтитров, текста и дубликатов;
- фактический aspect ratio, duration, resolution и файл.

При дефекте меняй один блок: reference map, subject profile, stage/end state, camera, edit scope, boundary contract или audio.

## 12. CN-режим: китайский промт

Seedance тренирован в основном на китайских парах текст-видео; правильно построенный китайский промт понимается не хуже английского, а на плотных описаниях действия и тонких формулировках часто точнее. Дефолт скилла остается английским. Включай CN-режим только если: пользователь явно попросил китайский; донор-промт пользователя на китайском и он просит его развить; генерация идет в китайском интерфейсе (即梦 Jimeng / Dreamina CN).

### Правило одного языка

- Весь промт на одном языке. Смешение CN+EN внутри художественного текста — главный источник дрейфа; не переводи половину блоков.
- Латиница остается для технических констант и меток: `2.39:1`, `RED`, `4K`, `fps`, `50mm`, `@Image N` / `@Тег` — метки референсов не переводить, писать точно как в UI хоста.
- Язык диалога задавай отдельным явным предложением: `台词为中文普通话，发音自然，不混入其他语言` или `全片无台词`. Язык промта не обязан совпадать с языком реплик.
- Не калькируй английские идиомы дословно — бери устойчивые формулы из глоссария ниже; машинный подстрочник модель понимает хуже родного английского.

### Порядок блоков CN-промта

Та же логика, что в разделе 4, с проверенными китайскими заголовками:

```text
场景背景        — тип видео, одна фраза о главном событии (= GENERATION GOAL)
激活参考        — роль и исключения каждого материала (= REFERENCE MAP);
                  формула: 参考图只控制X，不控制Y
主体设定        — идентичность, точное число якорей (= SUBJECT PROFILES / OBJECT LEDGER)
风格            — стиль, палитра, экспозиция
摄影机与镜头     — камера, оптика, характер движения
首帧与空间调度   — первый кадр и мизансцена (= INITIAL STATE + blocking)
格式模式        — число шотов, общая длительность, монтажный ритм
动作时间轴       — таймлайн: 镜头N——X.X至Y.Y秒——содержание; между шотами N秒切
表演任务        — актерские задачи: 动机/目标/战术, «功课在眼里，不演情绪»
物理            — физика: вес, инерция, взаимодействия, затухание
声音            — звук: диалог/язык, ambience, SFX, BGM или 无音乐
禁止            — негативы (= negative list)
```

Финальные состояния шотов и глобальные инварианты (END STATE, MAINTAIN CONSISTENCY) не выделяй отдельными заголовками — вписывай внутрь 动作时间轴 (последняя фраза шота) и 激活参考/主体设定, как в нативных CN-промтах.

### Глоссарий устойчивых формул

Кадрирование и композиция:

| EN | CN |
|---|---|
| wide shot / full shot | 远景 / 全景 |
| medium shot | 中景 |
| medium close-up | 近景 |
| close-up | 特写 |
| extreme close-up | 大特写 |
| low angle | 低角度（仰拍） |
| ground-level angle | 贴地极低角度 |
| high angle | 高角度（俯拍） |
| eye level | 与人齐高 / 平视 |
| over-the-shoulder | 过肩镜头 |
| POV | 主观视角 |
| foreground / deep background | 前景 / 画面深处 |
| screen-left / screen-right | 画左 / 画右 |
| depth staging | 纵深调度 |
| centered composition | 居中构图 |
| frame edge | 画面边缘 / 画框上缘 |

Движение камеры:

| EN | CN |
|---|---|
| locked / static camera | 机位固定 |
| slow push-in | 缓慢推近 / 极缓推近 |
| pull-back | 缓慢拉远 |
| dolly / slider move | 滑轨移动 |
| lateral tracking | 滑轨横移 |
| pan / tilt | 左右摇镜 / 上下摇镜 |
| follow shot | 跟拍 |
| crane up/down | 升降镜头 |
| motorized, uniform, precise | 电动机械运动，匀速精确 |
| one continuous take | 全程一镜 / 一镜到底 |
| handheld shake (запрет) | 手持晃动 |
| zoom (запрет) | 变焦 |
| slow motion (запрет) | 慢动作 |
| speed ramp (запрет) | 变速 |

Оптика:

| EN | CN |
|---|---|
| anamorphic 2x widescreen | 2倍变形宽银幕 |
| wide-open aperture | 大光圈全开 |
| shallow depth of field | 浅景深 |
| oval bokeh | 椭圆焦外 / 椭圆光斑 |
| cat-eye bokeh at edges | 边缘猫眼光斑 |
| chromatic aberration | 色差 |
| low-contrast filter | 低反差滤镜 |
| soft focus | 柔焦 |
| motion smear / ghosting | 拖影 |
| lens flare | 镜头眩光 |
| vignette | 暗角 |
| focal length / 50mm lens | 焦距 / 50毫米镜头 |

Свет и экспозиция:

| EN | CN |
|---|---|
| pre-dawn cold blue-grey | 黎明前的冷蓝灰 |
| golden hour | 黄金时刻 |
| underexposed by 1.5 stops | 欠曝一档半 |
| deep blacks with retained texture | 黑位深沉但保留质感 |
| natural warm skin tones | 肤色自然温暖 |
| low saturation | 低饱和 |
| practical light source | 现场实际光源 |
| sodium streetlight | 钠黄路灯 |
| rim light | 轮廓光 |
| backlight / top light | 逆光 / 顶光 |
| soft light / hard light | 柔光 / 硬光 |
| blown highlights (запрет) | 亮处发白失去细节 |

Физика и движение:

| EN | CN |
|---|---|
| real weight and momentum | 真实的重量与惯性 |
| ground fog drifting | 晨雾贴地流动 |
| breath vapor | 呼吸的白雾 |
| oscillation decays and stops | 摇晃衰减、逐渐停止 |
| constant pace / cadence | 步频稳定 / 匀速 |
| fabric behavior | 衣料的真实垂坠与摩擦 |
| splash / debris kicked up | 带起泥点 / 溅起水花 |

Тайминг и монтаж:

| EN | CN |
|---|---|
| Shot N — X to Y seconds | 镜头N——X.X至Y.Y秒 |
| cut at N seconds | N秒切 |
| hard cut / flash cut | 硬切 / 闪切 |
| cut to black | 切黑 |
| hold one beat / freeze | 定格一拍 |
| at 5 seconds | 第5秒 |
| in the last two steps | 最后两步 |

Негативы (блок 禁止 — конкретные существительные, формулы 无X / 不使用X / 绝不X / 非X):

| EN | CN |
|---|---|
| no subtitles / on-screen text | 无字幕、无画面文字 |
| no watermark / logo / UI / border | 无水印、无Logo、无UI、无边框 |
| no music | 无音乐 |
| no dialogue | 无台词 |
| no slow motion | 不使用慢动作 |
| no handheld shake | 无手持晃动 |
| no lens flare / streaks / starburst | 无镜头眩光、无横向光条、无星芒 |
| no plastic skin | 无塑料感皮肤 |
| not animation / not game CG | 非动画、非游戏CG |
| eyes never dead-blank | 绝不僵死呆滞、绝不空洞发直 |

### QA для CN-промта

Дополнительно к разделу 11 проверь:

- весь художественный текст на одном языке, ни одного случайного английского фрагмента внутри CN-блоков;
- технические метки (`@Image N`, соотношения, модели камер) не переведены;
- язык диалога задан явно отдельным предложением или стоит 无台词;
- негативы собраны в один блок 禁止 и используют формулы 无X/不使用X/绝不X, а не переводные «avoid…»;
- термины взяты из глоссария, а не подстрочник; сомнительный термин замени на описание видимого результата.
