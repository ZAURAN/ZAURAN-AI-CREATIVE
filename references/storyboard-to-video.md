# Product storyboard -> video

Используй этот документ для рекламных и product-раскадровок, технологических reveal, сборки продукта, вставки детали, one-shot роликов и промтов для Seedance/Kling/Veo/Sora-подобных видеомоделей.

## 1. Два обязательных артефакта

### Review board

Review board предназначена для человека. Для сложного 10–20-секундного product-shot обычно подходит одна landscape-доска `4 x 3` из 12 панелей:

- одинаковый размер панелей;
- чтение слева направо, сверху вниз;
- номер и короткое название сверху;
- одна техническая подпись снизу;
- стрелка только там, где без нее направление неочевидно;
- единый продукт, свет, среда и screen direction.

Это не универсальное требование. Простому действию достаточно 4–6 кадров; длинной истории нужны отдельные шоты. Не растягивай идею до 12 кадров ради шаблона.

### Clean generation pack

После утверждения board создай отдельную чистую версию для видеомодели:

- без стрелок и наконечников;
- без номеров, названий, подписей и рамок;
- без сетки, UI, курсоров и направляющих;
- без случайного текста;
- лучше отдельными clean keyframes, а не одной доской;
- те же crop, продукт, свет, материалы и состояния, что в утвержденной board.

Негатив `no arrows` не удаляет надежно стрелки, уже нарисованные в reference image. Видимый пиксель сильнее текстового запрета. Если чистые кадры нельзя подготовить, явно предупреди о риске до дорогой генерации.

## 2. Что делает кадр динамичным, а не плоским

В каждой панели используй минимум два, а лучше три плана:

1. foreground — край продукта, механизм, отражение или частица близко к линзе;
2. middle ground — главный объект и действие;
3. background — окружение, световые пути или удаленные детали.

Для глубины:

- строй диагональную композицию вместо постоянного фронтального центра;
- меняй масштаб естественно по траектории камеры;
- используй perspective convergence и near/far size difference;
- допускай мягкий foreground blur, сохраняя якорный объект резким;
- веди отражения и свет противоположно орбите для параллакса;
- используй один осмысленный camera path, а не набор несвязанных ракурсов;
- задавай speed ramp: ожидание -> ускорение -> пик действия -> торможение;
- motion blur разрешай фону, свету и быстрым механизмам, но не логотипу и не форме продукта.

Динамика должна происходить из камеры, физики и изменения состояния. Не заменяй ее стрелками, чрезмерными частицами, shake, случайным spin или световыми эффектами без причинной связи.

## 3. Контракт каждой панели

Для каждой панели зафиксируй:

- `STATE IN` — что уже существует и где находится;
- `ACTION` — одно главное действие;
- `CAMERA` — положение, объектив и одно движение;
- `DEPTH` — foreground / middle / background;
- `STATE OUT` — проверяемое конечное состояние;
- `LOCKED` — что не меняется;
- `NEXT` — физическая связь со следующим кадром.

Последовательность обязана показывать промежуточную физику. Для вставки детали нельзя перескакивать из `над слотом` сразу в `установлена`: покажи приближение, первый контакт, частичную вставку и состояние заподлицо.

## 4. Object ledger и запрет дубликатов

Перед генерацией запиши точное число якорей:

```text
OBJECT LEDGER
Processor: exactly 1; visible from 0.0s until enclosure; never duplicates.
Receiver/socket: exactly 1; empty before insertion; never resembles a second processor.
Phone: exactly 1; exterior identity remains unchanged.
```

Для одного объекта через несколько состояний используй причинные формулировки:

```text
The same single processor descends continuously into one visibly empty socket.
Show intermediate physical positions.
Once seated, nothing remains above the socket.
After enclosure, the processor never reappears.
```

Не описывай последовательные панели так, будто в каждой появляется новый экземпляр объекта. При конфликте сначала упрощай фазы и reference pack, а не наращивай общий negative list.

## 5. Reference map и brand-surface contract

Каждому референсу назначь одну главную роль и приоритет:

```text
@Image1 — clean storyboard/keyframes: sequence, camera, lighting only.
@Image2 — exact final-screen logo identity only.
@Image3 — exact product exterior and geometry only.
@Image4 — exact processor marking only.
```

Затем перечисли физические поверхности:

```text
BRAND-SURFACE CONTRACT
Processor surface: Intel only; Jupiter forbidden.
Phone rear body: Apple only; Intel/Jupiter forbidden.
Phone display: Jupiter only; Intel forbidden.
```

Для каждого знака зафиксируй:

- точную форму и число элементов;
- ориентацию и направление градиента;
- допустимую перспективу и отражения;
- разрешенный носитель;
- момент появления и исчезновения;
- места, где знак запрещен.

Если логотип на storyboard неточен, отдельный identity-reference должен иметь явный приоритет. Не проси модель одновременно копировать branding из board и заменять его текстовым описанием без такого приоритета.

## 6. Структура видеопромта

Пиши в порядке:

1. `FORMAT` — длительность, aspect ratio, resolution, one-shot или монтаж.
2. `REFERENCE ROLES AND PRIORITY` — что брать и что игнорировать из каждого файла.
3. `OBJECT LEDGER` — точное количество якорей.
4. `BRAND-SURFACE CONTRACT` — какой логотип где живет.
5. `START STATE` — первый реальный кадр.
6. `CAMERA PATH` — одно связное движение и screen direction.
7. `TIMELINE PHASES` — 4–6 фаз с диапазонами времени.
8. `END STATE` — точная финальная композиция и короткое удержание.
9. `STRICT NEGATIVES` — только самые вероятные и проверяемые ошибки.

Для 15 секунд разумный ритм product insertion:

```text
0.0–3.0   reveal / macro orbit
3.0–5.0   product and empty receiver reveal
5.0–7.5   alignment, contact and continuous insertion
7.5–10.5  lock, activation and enclosure
10.5–13.2 product lift / rotation
13.2–15.0 final display or approved end state; last 0.5s stable
```

Таймкоды задают причинный ритм, а не двенадцать жестких склеек. В одном непрерывном шоте явно запрети cuts, teleportation и reversal только один раз, затем опиши физическую траекторию.

## 7. Как писать negatives

Negative list не должен быть длиннее режиссуры. Сначала устрани причину из референсов и positive prompt.

Приоритетные негативы для product-shot:

- no duplicated anchor object;
- no stacked parts;
- no object remaining after enclosure;
- no arrows, captions or storyboard UI;
- no geometry drift or changing product identity;
- no logo on an unauthorized surface;
- no mirrored/rotated/missing logo elements;
- no morphing, melting or impossible intersections;
- no random text or extra props.

Не повторяй один запрет десятью синонимами, если исходный reference по-прежнему показывает нежелательный объект.

## 8. Частые дефекты и причина

| Дефект | Вероятная причина | Исправление |
|---|---|---|
| Стрелки в видео | Стрелки присутствуют пикселями на board | Создать clean generation pack; не лечить только negative prompt |
| Деталь накладывается на копию | Приемник похож на деталь; панели описаны как отдельные сцены | Показать пустой receiver, object ledger, одну непрерывную вставку |
| Логотип меняется | Board и identity-reference конфликтуют | Назначить отдельный reference и явный priority |
| Логотип на неправильной поверхности | Не задан brand-surface contract | Перечислить разрешенные и запрещенные носители |
| Кадры плоские | Одинаковый масштаб, фронтальная камера, нет планов | Добавить foreground, диагональ, parallax и camera arc |
| Ролик дергается | Каждый storyboard frame описан как отдельный шот | Сгруппировать board в 4–6 временных фаз |
| Финал продолжает меняться | Нет точного END и hold | Описать финальную геометрию и удерживать 0.5–1.0 с |

## 9. QA после генерации

Проверь видео целиком и contact sheet каждые 0.5–1.0 секунды:

1. Число якорных объектов в каждом кадре соответствует ledger.
2. Нет стрелок, подписей, рамок и storyboard UI.
3. Приемник пуст до контакта и не похож на дубликат детали.
4. Контакт и вставка имеют видимые промежуточные состояния.
5. После установки над receiver ничего не остается.
6. После закрытия скрытая деталь не появляется снова.
7. Геометрия продукта не дрейфует.
8. Каждый логотип находится только на разрешенной поверхности.
9. Логотипы совпадают с identity-reference по форме, ориентации и цвету.
10. Финальное состояние удерживается и не превращается в случайный wallpaper/UI.

При дефекте меняй один блок: reference hygiene, object ledger, brand contract, camera/timing или end state. Не переписывай все одновременно.
