# Контракт передачи

Полный ZAURAN-контракт — references/story-production-contract.md и references/script-to-assets.md в ZAURAN repo snapshot. Читать после materialize. Этот файл соединяет workflow, не отменяя исходный протокол.

## Проект и версии

Для существующего проекта сохранять его STATE и структуру. Для нового полного производства зафиксировать script/version, канон, assets, edit plan и status. Edit plan — внутренний промежуточный контракт, не готовый API движка.

```json
{"project_id":"video_001","script_version":"SCRIPT_v1","backend":"hypit","format":{"width":1080,"height":1920,"fps":30},"shots":[{"shot_id":"SHOT_01","beat_id":"BEAT_01","purpose":"Объяснить тезис","character_ids":["CHAR_01"],"asset_ids":["ASSET_01"],"visual_route":"code_motion","word_anchor":{"voice_version":"VO_v1","token_id":"TOKEN_18","status":"unresolved"},"source_refs":["SOURCE_01"],"approval_status":"draft","qa_status":"not_checked"}]}
```

Asset register хранит исходник и производные раздельно: stable ID, source/version, provider/model, параметры, размер/длительность/fps/alpha, стоимость при применимости, lineage, approval и measured QA. Персонаж ссылается на passport/костюм/reference. Утверждённое не автоматически проверено; успешный запуск не автоматически хороший результат.

## Речь, факты и графика

Повторяющиеся слова требуют speaker/voice version и уникального token ID. После правки текста или озвучки повторно измерить alignment и проверить missing/ambiguous anchors.

Каждая motion-вставка объясняет отношение, изменение или доказательство. Давать время для чтения, ограничивать конкуренцию элементов. Числа графиков и места карт брать из сохранённых данных; генеративная иллюстрация не заменяет факт.

Для HyperFrames-аудио в сохранённой версии сначала читать полный `skills/hyperframes-audio/references/attributes.md`: примеры в основном SKILL.md местами расходятся с этим контрактом. Audio attributes записывать в двойных кавычках, JSON-кавычки экранировать как `&quot;`, амперсанды как `&amp;`. Carve-helper не распознаёт одинарные кавычки и может перезаписать невидимую ему цепь. `data-fx-carve` всегда следует речи; поле `dynamic` игнорируется. Ручные FX-узлы не помечать `fromCarve`, сохранять их stable ID и учитывать разные часы автоматизации clip/bus. Эти сведения относятся к включённому snapshot; при другой версии сверять его реальный контракт.

## Персонажи и генерация

Production владеет model/environment gate и model-specific prompting. Story/character/staging передают ТЗ и канон. Проверять настоящую поддержку references, transparency, negative prompts и seeds; не имитировать unsupported fields. Сохранять результаты и provenance.

Генерировать требуемые элементы; титры, диаграммы и простые движения можно рендерить кодом. Перед мультсерией проверить дизайн, ракурсы/эмоции и continuity. Утверждённый паспорт не менять из-за эстетики шаблона без авторизации.

## Вырезки

Полные BACKGROUND_REMOVAL.md и scripts/remove_background.py сохранены в database snapshot. Для фото сравнить подходящие rembg/BiRefNet; отдельно проверить лицензию весов RMBG. SAM2 segmentation/tracking не равен аккуратному alpha matting. Покадровая фото-модель может мерцать.

Сохранять исходник; подготовить новый alpha-capable output. Проверять волосы, мягкие края, стекло и отверстия на светлом/тёмном фоне, straight/premultiplied alpha. Обычный H.264 не сохраняет прозрачность промежуточных слоёв. Не заменять обычную вырезку генеративным редизайном объекта.

## Проверка результата

Сохранять обязательные измерения и review выбранного workflow. Для MP4 измерить файл и просмотреть репрезентативные/проблемные кадры; проверить текст/safe zones, звук, temporal consistency, смысл, claims и формат. Для проекта проверить материалы, зависимости, реальный backend и воспроизводимый запуск.

План, код, проект и ролик — разные deliverables. Если запрошен ролик, схема не завершает задачу. Если запрошен сценарий, запуск генераций не входит автоматически. Недостающий ZIP/инструмент/ассет обозначать конкретно.
