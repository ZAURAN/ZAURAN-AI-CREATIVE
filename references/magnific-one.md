# Magnific One — модельный контракт и практические примеры

Проверено: 14 октября 2026. Среда: Magnific Image Generator / Spaces. Версия памятки: 1.

Это авторская памятка по официальным источникам, а не перевод документации целиком. Подтверждённые возможности отделены от рекомендаций для RolsBet. Генерации на Magnific One в рамках этой проверки не запускались; примеры ниже ещё не прошли визуальное тестирование.

## Область применения в навыке

Читай этот файл при выборе Magnific One для генерации, редакции или подготовки промпта. Magnific One — отдельная модель; слово «Magnific» само по себе может обозначать площадку с Seedream или другой моделью либо апскейлер и не определяет выбор.

Общие правила языка, реестра требований, полной выдачи и QA из SKILL.md сохраняются. Пиши английский промпт естественным языком, указывай каждое требование один раз. Компактность не разрешает убирать активные требования. При адресной правке уже выданного промпта сохраняй неизменённые блоки по общему правилу; при переносе на Magnific One можно пересобрать структуру и убрать повторы, сверив все требования.

Подтверждённые возможности ниже привязаны к дате проверки. Не выдумывай внутренний model ID, API-поля, цены или доступные настройки. При изменившемся интерфейсе проверяй официальные ссылки в конце файла.

Разделы с RolsBet — пример конкретного проекта, не глобальные настройки навыка. Не переносить автоматически быка, палитру, форму, надпись, возрастной футер или 55% свободного поля в чужие задачи. Это непроверенные генерацией примеры, не доказанные рецепты.

## 1. Подтверждённые возможности

Magnific One самостоятельно разворачивает запрос в производственный промпт, учитывая референсы и стиль. Достаточно описать задачу обычным языком.

| Параметр | Что указано в документации |
|---|---|
| Draft | Сетка из 4, 8 или 16 вариантов для поиска направления |
| Final | Финальное изображение; переход из Draft может изменить детали и композицию |
| Качество | High по умолчанию; Max требует больше времени и кредитов |
| Разрешение | 2K или 4K; квадрат в режиме 4K — 2880 × 2880, не 4096 × 4096 |
| Референсы | До 5; авторы рекомендуют начинать с двух |
| Точность | Нет гарантии точного текста, логотипа, геометрии предмета и размещения |
| MCP | Доступен; Draft и Brand Kit пока доступны только в приложении |

Источник: [Magnific One — документация модели](https://www.magnific.com/ai/docs/magnific-one).

## 2. Что советует официальный prompting guide

Начинайте с типа изображения: фотография, иллюстрация, 3D или постер. Затем задавайте героя и действие. Каждое требование формулируйте один раз: повторения могут привести к пропуску деталей. Вместо общей оценки качества описывайте наблюдаемые материалы и свет. Точный текст заключайте в кавычки.

Обычные референсы определяют содержание. Вкладка Style предназначена для визуального языка; поддерживает 1–5 изображений и работает в Draft и Final. Не путайте источник внешности героя с источником стилистики. Официальный гайд также показывает адресные правки света и композиции с перечислением сохраняемых свойств.

Источник: [Magnific One — официальный prompting guide](https://www.magnific.com/prompts/magnific-one).

## 3. Brand Kit для RolsBet

Brand Kit подключается к Magnific One в Final. Его можно сформировать из PDF, изображений, ZIP, публичного сайта или текстового описания; затем проверить предложенные правила и тестовые изображения. В Spaces используется отдельный узел Brand Kit. Коррекции могут становиться постоянными правилами набора: не записывайте туда временное решение одного поста.

Загрузка файлов шрифтов пока не поддерживается: типографику задают текстовыми правилами или через PDF. Точные значения цвета, шрифт и позиционирование не гарантированы. CMYK и Pantone не поддерживаются. Для точного завершения документация предлагает Auto Layers и Designer либо собственные инструменты.

Источник: [Brand Kit — официальная документация](https://www.magnific.com/ai/docs/brand-kit).

Ниже — проектные правила из нашего ТЗ, не универсальные настройки модели:

- Палитра: #000000, #111111, #C90025, #83001C, текст #F1F1F1.
- Золото преимущественно на фирменном мяче.
- Fira GO Heavy для заголовков, Inter Regular для вспомогательного текста.
- Оригинальные знаки без придуманной геометрии и дополнительных спонсоров.
- Чёрная шерсть, ткань и фон должны различаться по материалу и освещению.
- Конкретная форма определяется текущим референсом. Для этого анонса она чёрная с красными деталями, а не красная.
- Поза спотыкающегося быка и левое поле 55% — правила этого макета, не всего бренда.

## 4. Рабочая структура промпта

Это моя рекомендуемая структура для наших задач, а не обязательный синтаксис Magnific:

1. **Результат:** что создаём, для какой площадки, какой формат.
2. **Референсы:** какой файл отвечает за внешность, одежду, предмет или композицию.
3. **Действие и эмоция:** что происходит в этот единственный момент.
4. **Композиция:** масштаб, позиция, место под текст, допустимые перекрытия.
5. **Материалы и свет:** только особенности, которые важны для результата.
6. **Текст:** точные строки, иерархия и размещение.
7. **Ограничения:** несколько актуальных запретов, без повторов.

У модели нет установленного здесь лимита «идеальных слов». Короткий промпт полезен, пока не теряет обязательные требования. Сокращаем повторы и общие эпитеты, а не идентичность, мяч или действие.

### Шаблон для заполнения

```text
Create a [medium] for [purpose], in [aspect ratio].
Use the attached [reference description] for [specific role].
Show [subject] at the moment when [action], with [visible expression].
Place [subject group] in [area and scale]. Reserve [area] for [text or negative space].
Use [materials, palette and lighting].
Include exactly “[approved copy]” in [position and hierarchy].
Preserve [critical properties]. Exclude [task-specific unwanted elements].
```

Это шаблон, а не готовый к запуску промпт: заполните скобки и удалите строку текста, если надписей не требуется.

## 5. Референсы и теги

Не считайте написанное имя файла доказательством того, что генератор получил картинку. Сначала подключите изображение к узлу/генерации, затем проверьте, что оно отображается во входных референсах.

Для нашего проекта распределение ролей такое:

| Файл / подпись | Роль | Что не переносить |
|---|---|---|
| ЭМОЦИИ | Морда, рога, причёска, глаза | Весёлую улыбку, если нужна реакция на падение |
| карта_перса_тело | Телосложение, пропорции | Красное бельё и статичную позу |
| форма | Дизайн полного комплекта | Коллаж и увеличенные вставки ткани |
| мяч | Фирменный предмет | Фон исходного изображения |
| сцена | Базовый кадр для редакции | Ошибки, которые прямо поручено исправить |

Не подключайте все пять автоматически. Для новой сцены обычно нужны внешность, форма и мяч; карту тела добавляем, если внешность не показывает пропорции. Для правки хорошей сцены сама сцена уже несёт большую часть информации.

В Spaces официально поддерживаются @упоминания узлов в поле Prompt. Изображения подключаются ко входу Reference. Названия @форма и @мяч — имена ваших узлов, а не специальные команды модели. Вводите @ и выбирайте соответствующий узел; подпись на скриншоте сама по себе не подтверждает подключение. Это функция среды Spaces, а не доказательство универсального синтаксиса самой модели. Не переносите без проверки токены других моделей вроде <IMAGE_REF_1>, --cref или числовые веса. Источники: [Image nodes](https://www.magnific.com/ai/docs/image-nodes), [Text nodes](https://www.magnific.com/ai/docs/text-nodes).

Примеры ниже используют имена узлов нашего проекта. Перед запуском подключите соответствующие изображения и вставьте реальные упоминания. В другом интерфейсе без узлов нужно адаптировать привязку к его фактическим входам.

## 6. Пример: наш анонс с быком и текстом

Авторский пример для Magnific One, ещё не протестирован. Подключите @ЭМОЦИИ, @карта_перса_тело, @форма и @мяч. Установите квадрат в контроле формата.

```text
Create a square 1:1 football campaign poster in cinematic stylized 3D for RolsBet.

Use @ЭМОЦИИ for the bull’s facial identity, @карта_перса_тело for muscular proportions, @форма for the black jersey, shorts and socks with red trim and existing branding, and @мяч for the black-and-gold football. Do not copy the reference sheets, interface, jewelry or casual clothing.

Show the instant the bull unexpectedly stumbles: the ball rolls slightly forward beneath one boot, which still touches its upper surface; his other boot stays planted, its knee bending as his torso tips backward and sideways. His hands react to catch his balance. He looks startled and concerned, with slightly widened eyes, raised brows and a small open mouth, not smiling. Keep his gaze toward the viewer. No completed fall or injury.

Keep the full bull-and-ball group in the rightmost 40% of the image, occupying roughly two-thirds of the image height. Include the entire horns, hands, boots and ball. Reserve the left 55% for typography, with no limb or object crossing into it. Use a continuous near-black stadium background, subdued green turf at the bottom, and blurred floodlights confined to the far right. The camera stays level.

Place the exact headline on the left with these line breaks:
“ALL UNDER
CONTROL.
ALMOST.”
Use large, left-aligned Fira GO Heavy-style lettering. The first two lines are #F1F1F1; “ALMOST.” is #C90025 with a small extra gap above it. Set the small readable footer “18+ · Play responsibly.” at bottom-left in Inter Regular-style lettering. Keep generous outer margins.

Soft neutral light reveals the face and fabric; restrained red rim light separates black fur and clothing from the background. Preserve the kit design, natural material textures and the ball’s visible mark facing the viewer, clear of the boot. Ground both ball and supporting boot with contact shadows. No additional copy, sponsors, characters, casino props, smoke, sparks or watermark.
```

Слова «style lettering» здесь намеренны: это запрос внешнего вида, не подтверждение использования настоящего файла шрифта. Для точной брендовой выдачи надписи и логотипы проверяются и при необходимости заменяются в редакторе.

## 7. Пример: исправить только эмоцию

Прикрепите удачный кадр как @сцена. Это самостоятельный промпт локальной правки, а не дополнение, которое надо склеивать с длинным генерационным описанием.

```text
Edit only the bull’s facial expression in @сцена. Replace the happy toothy grin with a restrained startled reaction to losing his footing: slightly widened eyes, eyebrows raised with a little inward tension, neutral mouth corners and a small parted mouth. Keep him recognizable, without panic or an exaggerated grimace.

Preserve his facial anatomy, fur, horns and hairstyle. Keep the body pose, clothing, football, all text, camera, composition, lighting and background unchanged. Do not add or remove anything.
```

## 8. Пример: освободить место под будущую вёрстку

Этот пример предназначен для исходника без надписей, подключённого как @сцена. Он не должен случайно удалять уже согласованную типографику.

```text
Recompose the text-free image @сцена as a square advertising background. Scale down the entire bull-and-football group and place it fully within the rightmost 40% of the canvas, with its total height around two-thirds of the frame. Keep the full horns, hands, boots and ball visible. Bring the balancing gesture inward enough that no limb crosses into the left area.

Leave the left 55% clear for later typography: a continuous, low-contrast near-black stadium background, without bright lights or pitch markings behind the future text. Keep the turf along the bottom. Preserve the bull’s identity, startled expression, stumbling action, black-and-red kit, football design and lighting character. Rebuild consistent ground contact and shadows after repositioning. Generate no text or placeholder boxes.
```

## 9. Как исправлять типичные ошибки

Практические гипотезы для этой серии; не результаты сравнительного теста модели.

| Проблема | Что проверить | Следующая правка |
|---|---|---|
| Бык радуется | Не осталось ли «confident smile», «cheerful», «grin» в промпте или правилах? | Описать нейтральные уголки рта, небольшое раскрытие глаз и убрать противоречивую улыбку |
| Нет места слева | Размер всей группы, а не только центра тела | Уменьшить быка вместе с мячом; ограничить руку и ногу правой областью |
| Форма красная | Не осталось ли старого описания красной футболки? | Сделать фото формы единственным источником её дизайна |
| Бык выглядит позирующим | Действие описано как статичная нога на мяче | Указать, что мяч сдвигается, корпус реагирует, колено сгибается |
| Теряется внешность | Смешаны роли стиля, персонажа и одежды | Вернуть одну явную роль каждому изображению |
| Портится логотип | Генерация перерисовывает мелкий знак | Заменить оригинальным ассетом после выбора сцены |
| Слишком тёмный герой | Чёрная шерсть, форма и фон сливаются | Разделить их мягким светом и различием материалов |

Не меняйте одновременно эмоцию, ракурс, стиль, форму и фон при исправлении одного дефекта. Если композиция уже подходит, защищайте её явно; если её нужно изменить, не добавляйте противоречивое «keep all positions unchanged».

## 10. Приёмка и границы знания

Перед запуском: проверить выбранную модель, реальные вложения, роли файлов, текущую версию формы, нужную эмоцию и точные строки текста. Проценты размещения являются пожеланием к композиции, а не координатной маской.

После результата: осмотреть лицо, число конечностей, контакт бутсы и мяча, оригинальность знаков, фактическое место под текст, орфографию и размер изображения. Для мобильной читаемости посмотреть уменьшенную копию. Визуальный результат важнее того, насколько хорошо сформулирован промпт.

В этой памятке НЕ подтверждены: внутреннее устройство модели; универсальная грамматика тегов вне Spaces; отдельные параметры negative prompt, seed, CFG и steps для Magnific One; точный токен-лимит; гарантированная воспроизводимость; пиксельно неизменная редакция; качество кириллицы. Отсутствие подтверждения не означает отсутствие функции. Общая документация Spaces перечисляет Seed, Negative Prompt и Guidance Scale, но доступность зависит от модели: используйте их только при наличии в текущем интерфейсе Magnific One. Не переносите настройки Seedream или апскейлера Magnific на эту модель автоматически. Источник: [настройки Image nodes](https://www.magnific.com/ai/docs/image-nodes).

## 11. Источники и обновление

Проверенные официальные страницы:

1. [Модель, режимы и ограничения](https://www.magnific.com/ai/docs/magnific-one).
2. [Авторский prompting guide Magnific](https://www.magnific.com/prompts/magnific-one).
3. [Brand Kit](https://www.magnific.com/ai/docs/brand-kit).
4. [Image nodes — подключения, @упоминания, модель-зависимые настройки](https://www.magnific.com/ai/docs/image-nodes).
5. [Text nodes — упоминания узлов](https://www.magnific.com/ai/docs/text-nodes).

При изменении интерфейса сначала перепроверьте режимы, входные референсы и Brand Kit по этим страницам. Этот файл не обновляется автоматически. Результаты собственных тестов следует записывать отдельно с исходным промптом, вложениями, режимом и итоговым изображением; текущие примеры не объявлять проверенными до генерации.
