# Gemini Omni Flash — API, параметры, площадки

Companion к `gemini-omni-flash.md`. Всё здесь — из официальной документации Google, REST-референса `ai.google.dev/api/interactions-api`, исходников SDK `google-genai` и исполняемого скилла Google `gemini-omni-flash-api`. Где источники расходятся, назван победитель и причина.

## 1. Model ID — ловушка именования

| Площадка | ID |
|---|---|
| Gemini API, GA | `gemini-omni-1.1-flash` |
| Gemini API, preview | `gemini-omni-flash-preview` — **выводится из эксплуатации 30.09.2026** |
| Vertex / Gemini Enterprise Agent Platform, актуальный | `gemini-omni-1.1-flash-preview` |
| Vertex, старый | `gemini-omni-flash-preview` (только text→video, editing и 720p) |

Каждый Vertex-ID несёт суффикс `-preview`. Голая строка `gemini-omni-1.1-flash` существует **только в Gemini API** и на Vertex вернёт `model_not_found`.

С model card: вход Text / Image / Video (≤10 с для правки и расширения); выход Video; контекст 1 048 576 токенов в Gemini API против max input 131 072 / max output 57 920 на Vertex — это **разные площадки**, обе цифры верны там, где опубликованы. Выход 3–10 с, 360p/720p/1080p/4K, 24 FPS.

## 2. Эндпоинт — только Interactions API

| Операция | Вызов |
|---|---|
| Create (Gemini API) | `POST https://generativelanguage.googleapis.com/v1beta/interactions` |
| Retrieve | `GET https://generativelanguage.googleapis.com/v1beta/interactions/{id}` |
| Cancel | `POST .../interactions/{id}/cancel` |
| Delete | `DELETE .../interactions/{id}` |
| Create (Vertex) | `POST https://aiplatform.googleapis.com/v1beta1/projects/{PROJECT}/locations/global/interactions` |
| Retrieve (Vertex) | `POST .../interactions/{ID}` с пустым телом `-d ""` — именно POST, не GET |
| List (Vertex) | `GET .../interactions?page_size=&page_token=` (по умолчанию 10, максимум 500) |

Авторизация: Gemini API — `?key=$API_KEY` либо заголовок `x-goog-api-key`. Vertex — `Authorization: Bearer $(gcloud auth print-access-token)`.

Vertex работает **только в регионе `global`**. Регионального `us-central1-aiplatform` для Omni нет — этот хост только для Veo.

`ai.google.dev/api/interactions` **отдаёт 404**; настоящий референс лежит по `/api/interactions-api`. Из-за этой битой ссылки легко ошибочно заключить, что параметра `duration` не существует.

Отдельно: Omni до сих пор **отсутствует в таблице «Supported models & agents»** обзора Interactions API — эта страница устарела и не авторитетна. Не «проверяй» поддержку Omni по ней: Interactions API — единственный способ вызвать эту модель.

## 3. SDK

```python
from google import genai
client = genai.Client()                                              # Gemini API
client = genai.Client(vertexai=True, project=..., location="global") # Vertex
interaction = client.interactions.create(...)
client.interactions.get(id) / .cancel(id) / .delete(id)
```

```javascript
import { GoogleGenAI } from '@google/genai';
const ai = new GoogleGenAI({});
const interaction = await ai.interactions.create({ ... });
```

**Фиксируй `google-genai >= 2.19.0`** — собственный скилл Google требует именно эту версию ради клиента `interactions` и полной конфигурации разрешения. Python **≥ 3.10**. Общий обзор Interactions API называет порог 2.3.0 — он для семейства API, не для Omni.

Переменные окружения на Vertex, по примерам Google:

```bash
export GOOGLE_CLOUD_PROJECT=...
export GOOGLE_CLOUD_LOCATION=global
export GOOGLE_GENAI_USE_ENTERPRISE=True
```

Именно `GOOGLE_GENAI_USE_ENTERPRISE`, а не прежняя `GOOGLE_GENAI_USE_VERTEXAI`.

Защита в SDK: `ValueError`, если передать одновременно `generation_config`+`agent`, `generation_config`+`agent_config`, `model`+`agent` или `model`+`agent_config`.

## 4. Тело запроса

Верхний уровень:

| Поле | Тип | Примечание |
|---|---|---|
| `model` | string | обязательное |
| `input` | string \| Content \| Content[] \| Step[] | обязательное |
| `previous_interaction_id` | string (`v1_...`) | многоходовое состояние; хранит видео без повторной загрузки |
| `response_format` | object (Gemini API) / **массив** (Vertex) | см. ниже |
| `generation_config` | object | содержит `video_config` |
| `background` | bool | асинхронный режим |
| `store` | bool | по умолчанию `true`; при `store=false` видео **нельзя** редактировать позже через `previous_interaction_id` |
| `stream` | bool | SSE |
| `labels` | dict | пользовательские метаданные |
| `webhook_config` | object | колбэк по завершении, альтернатива опросу |
| `safety_settings` | array | есть в схеме, но обзор Interactions API says кастомные safety settings не поддерживаются — для Omni не проверено |
| `system_instruction`, `tools` | — | **Omni не учитывает** |
| `response_mime_type`, `response_modalities` | — | **устарели** |

Рекомендация Google по производительности, дословно: *«Set `background=false`, `store=false`, and `stream=false` for faster, synchronous unary generation.»* Но помни о цене `store=false` выше: если планируется итерация — не трогай `store`.

### `response_format` (`VideoResponseFormat`)

| Поле | Допустимые значения | По умолчанию |
|---|---|---|
| `type` | `"video"` | в примерах Google помечено как необязательное |
| `aspect_ratio` | `"16:9"`, `"9:16"` | `16:9` |
| `resolution` | `"360p"`, `"720p"`, `"1080p"`, `"4k"` | `720p` |
| `duration` | строка, целое 3–10 + `"s"` — `"3s"` … `"10s"` | не задано → модель решает, «обычно 10 с или как у источника» |
| `delivery` | `"inline"`, `"uri"` | `inline` |
| `gcs_uri` | string | только Vertex; там обязателен при `delivery: "uri"` |

Пиксельные размеры выхода (из скилла Google):

| | 16:9 | 9:16 |
|---|---|---|
| `360p` | 640×360 | 360×640 |
| `720p` | 1280×720 | 720×1280 |
| `1080p` | 1920×1080 | 1080×1920 |
| `4k` | 3840×2160 | 2160×3840 |

`1080p` и `4k` — **апскейл** рендера 720p, это прямо сказано в changelog Google.

Три уточнения:

- `duration` **есть и в Gemini API**, не только на Vertex. Он в официальном REST-референсе и в собственном `generate_video.py` Google, где валидируется: `parse_and_validate_duration()` отклоняет дробные, отклоняет всё вне 3–10, срезает хвостовую `s` и возвращает `f"{n}s"`. Страница гайда Omni его просто не упоминает — неполон гайд, а не параметр.
- Changelog утверждает, что `resolution` живёт в `video_config`. **Это не так** — он в `response_format`. Схема и все примеры кода согласны против changelog.
- `delivery: "uri"` Google в собственном скилле использует безусловно, а не только для файлов больше 4 МБ.

### `generation_config.video_config`

Единственное поле `task`, открытый enum: `text_to_video` · `image_to_video` · `reference_to_video` · `edit` · `extend`.

Рекомендация Google дословно: *«We recommend relying primarily on prompting and using the `task` parameter only when prompting doesn't work… as using the `task` field adds some constraints.»*

Ограничения, из кода Google и cookbook:

- `task` и `previous_interaction_id` **взаимоисключающи** — `generation_config` собирается только `if task and not previous_interaction_id`. Задав `task`, теряешь цепочку правок.
- `task="extend"` **отключает мультимодальные референсы** — ни референсных изображений, ни видео.
- При `task="extend"` поле `aspect_ratio` нужно **опустить**, оно наследуется от исходного видео.

В `generation_config` также присутствуют (из общей схемы): `max_output_tokens`, `seed`, `speech_config`, `stop_sequences`, `thinking_level` (`minimal|low|medium|high`), `thinking_summaries` (`auto|none`), `tool_choice`, `transcription_config`, `image_config` (устарело). Vertex дополнительно перечисляет `temperature` и `top_p`. **Omni не учитывает ни temperature, ни top_p, ни stop_sequences, ни system_instruction** — это в его собственном списке ограничений. `seed` в схеме есть и в списке запретов его нет, но он не встречается ни в одном примере Omni и ни в одном фрагменте кода Google, поэтому воспроизводимость через seed для Omni **не подтверждена**.

### Части `input`

| Часть | Форма |
|---|---|
| текст | `{"type": "text", "text": "..."}` |
| изображение inline | `{"type": "image", "data": <b64>, "mime_type": "image/jpeg"｜"image/png"}` |
| изображение по URI | `{"type": "image", "uri": ..., "mime_type": ...}` |
| видео | `{"type": "video", "uri"｜"data", "mime_type": "video/mp4"}` |
| хендл Files API | `{"type": "document", "uri": "files/..."}` |
| форма-обёртка | `{"type": "user_input", "content": [ ... ]}` |

**`video` или `document` для загруженного видео:** гайд ai.google.dev использует `{"type": "document", "uri": ...}`; исполняемый скилл Google и Vertex-документация по задачам используют `{"type": "video", "uri": ..., "mime_type": ...}`. **Предпочитай `type: "video"` с явным `mime_type`** — это то, что реально отправляет рабочий код Google. `document`, судя по всему, тоже работает через вывод типа.

Полная схема `VideoContent`: `data`, `mime_type`, `name`, `processing` (`"static"｜"agentic"` или объект), `resolution`, `type`, `uri`.
Принимаемые MIME видео: `video/mp4, video/mpeg, video/mpg, video/mov, video/avi, video/x-flv, video/webm, video/wmv, video/3gpp` (Vertex также перечисляет `video/quicktime`, `video/x-ms-wmv`).
Принимаемые MIME изображений (Vertex): `image/png, image/jpeg, image/webp, image/heic, image/heif`.

**Порядок частей в коде Google**, он же определяет нумерацию тегов: первый кадр → последний кадр → референсные изображения → исходное/расширяемое видео → референсные видео → **текст всегда последним**.

## 5. Ответ

```json
{
  "steps": [
    { "type": "user_input",  "content": [{"type": "text",  "text": "..."}] },
    { "type": "thought",     "content": [{"text": "...", "type": "thought"}] },
    { "type": "model_output","content": [{"type": "video", "mime_type": "video/mp4",
                                          "data": "AAAAIGZ0eXBpc29t..." }] }
  ],
  "id": "v1_...", "status": "completed",
  "model": "gemini-omni-1.1-flash", "object": "interaction"
}
```

При `delivery:"uri"` блок контента несёт `uri` вместо `data`.

`interaction.output_video` / `.output_text` / `.output_image` / `.output_audio` — **удобства только SDK**. По сырому REST читай массив `steps`.

Enum `status`: `in_progress`, `requires_action`, `completed`, `failed`, `cancelled`, `incomplete`; ai.google.dev добавляет `budget_exceeded`, `queued`.

Ответы Vertex дополнительно несут `usage` (`total_tokens`, `total_input_tokens`, `input_tokens_by_modality[]`, `output_tokens_by_modality[]`, `total_output_tokens`, `total_thought_tokens`, `total_cached_tokens`, `total_tool_use_tokens`), плюс `role`, `created`, `updated`. На Vertex шаг `thought` использует ключ `summary`, а не `content`.

**Документированная ловушка, дословно:** *«calling `GET /v1beta/interactions/{id}` returns the video as inline base64 data in the `data` field, even if the interaction was originally created with `delivery: "uri"`. The `uri` field is only guaranteed to be present in the initial creation response or Server-Sent Events (SSE) stream.»*

## 6. Асинхронность — ни один паттерн не является Veo-Operation

**(a) Фоновая интеракция** — `background: true`, create возвращает `{"id":..., "status":"in_progress"}`; опрашивай интеракцию. Vertex хранит результат 14 дней. Ресурса `operations/{id}` нет, `:fetchPredictOperation` нет.

**(b) Доставка по URI** — опрашивай **файл**, а не операцию:

```python
interaction = client.interactions.create(
    model="gemini-omni-1.1-flash",
    input="A beautiful sunset.",
    response_format={"type": "video", "delivery": "uri"}
)
video_output = interaction.output_video
file_name = video_output.uri.split("/")[-1]
while True:
    f_info = client.files.get(name=f"files/{file_name}")
    if f_info.state.name == "ACTIVE": break
    elif f_info.state.name == "FAILED": raise RuntimeError("Generation failed.")
    time.sleep(5)
video_bytes = client.files.download(file=video_output.uri)
```

**(c) SSE** — `stream: true` при создании либо `GET .../interactions/{id}?stream=true&last_event_id=...` для возобновления. Порядок событий: `interaction.created` → `interaction.status_update` → `step.start` → `step.delta` → `step.stop` → `interaction.completed` → `event: done / data: [DONE]`. Ошибки приходят событиями с `event_type: "error"`.

**(d) Вебхуки** — `webhook_config` в теле create; в SDK есть `client.webhooks` с create/list/update/ping/rotate_signing_secret.

**Обработка входного файла** — отдельный опрос:

```python
video_file = client.files.upload(file="Video.mp4")
while video_file.state == "PROCESSING":
    time.sleep(10)
    video_file = client.files.get(name=video_file.name)
if video_file.state == "FAILED": raise ValueError(video_file.state)
```

**Таймауты:** скилл Google по умолчанию ставит 600 с HTTP-таймаута и рекомендует `--timeout 900` и выше для 4K и для многоходовых расширений к потолку 40 с. Это единственный ориентир по латентности, который Google публикует.

## 7. Канонические вызовы

Text to video:

```python
import base64
from google import genai
client = genai.Client()

interaction = client.interactions.create(
    model="gemini-omni-1.1-flash",
    input="A marble rolling fast on a chain reaction style track, continuous smooth shot."
)
with open("marble.mp4", "wb") as f:
    f.write(base64.b64decode(interaction.output_video.data))
```

С управлением форматом:

```python
interaction = client.interactions.create(
    model="gemini-omni-1.1-flash",
    input="A futuristic city with neon lights and flying cars, cyberpunk style",
    response_format={
        "type": "video",
        "aspect_ratio": "9:16",
        "resolution": "1080p",
        "duration": "8s",
    },
)
```

Image to video — обрати внимание, как собственный пример Google прямо запрещает показывать исходный рисунок:

```python
interaction = client.interactions.create(
    model="gemini-omni-1.1-flash",
    input=[
        {"type": "image", "data": base64_image, "mime_type": "image/jpeg"},
        {"type": "text", "text": "turn this into realistic footage, using the drawing only as a guide for movement, do not show the drawing in the final video"}
    ],
)
```

Примечание Google: *«For best results with image-to-video, use high-resolution images and provide specific motion descriptions. Vague prompts like 'make it move' produce less compelling results than detailed descriptions of the camera movement, subject motion, and environmental effects.»*

REST, минимальный:

```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-omni-1.1-flash",
    "input": "A marble rolling fast on a chain reaction style track, continuous smooth shot."
  }'
```

Vertex — форма тела другая, `response_format` это **массив**:

```json
{
  "model": "gemini-omni-1.1-flash-preview",
  "input": [ { "type": "text", "text": "TEXT_PROMPT" } ],
  "response_format": [
    { "type": "video", "delivery": "uri", "gcs_uri": "gs://bucket/out/",
      "aspect_ratio": "16:9", "resolution": "720p", "duration": "10s" }
  ],
  "generation_config": { "video_config": { "task": "text_to_video" } }
}
```

## 8. Files API

До 20 ГБ на проект, 2 ГБ на файл, хранение **48 часов** с автоудалением, бесплатно во всех поддерживаемых регионах. Inline base64 упирается в практический потолок ~4 МБ — выше используй `delivery="uri"` на выходе и Files API на входе.

Пофайловые лимиты Vertex: изображения максимум 10 на промпт, 20 МБ inline / 30 МБ из GCS; текст 50 МБ через API/GCS, 7 МБ через консоль; видео максимум 10 с, максимум 3 на промпт.

`upload_file.py` Google предупреждает выше 25 МБ и рекомендует предобработку — эти 25 МБ **эвристика скорости загрузки**, а не лимит API.

## 9. Площадки различаются — проверь до обещаний

| Площадка | Особенности |
|---|---|
| Gemini API / AI Studio | Полный набор 1.1. Основная девелоперская площадка, на неё написан этот модуль. |
| Vertex / Agent Platform | ID с `-preview`, только `global`, вывод в `gcs_uri`, `duration` документирован. Потребление: **только фиксированная квота** — нет pay-as-you-go, нет batch, нет provisioned throughput. |
| Google Flow | Добавляет голосовые референсы, именование `@character` / `@me`, ingredients. **Расширять клипы Omni не умеет** (только Veo). Путь правки: загрузка ≤60 с / 1 ГБ, обрезка до ≤30 с, выбор сегмента ≤10 с, ~3 разговорных хода до потери контекста. |
| Приложение Gemini / YouTube | Только расширение сцены для подписчиков. Единственная площадка, где встречается вход `<audio>`. |

## 10. Цены (Gemini API, оба ID, бесплатного тарифа нет)

- Вход **$1.50** / 1M токенов (текст / изображение / видео / аудио)
- Выход **$9.00** / 1M (текст), **$17.50** / 1M (видео), включая thinking-токены
- Дословно: *«Billing is based on total output token consumption, calculated at a rate of 5,792 tokens per second of 720p video… approximately $0.10 per second.»*

Ставки за секунду по разрешениям, по нескольким вторичным источникам (не со страницы Google): 360p $0.03 · 720p $0.10 · 1080p $0.15 · 4K $0.30. **360p — рычаг экономии**: Google указывает до 60% быстрее при трети стоимости 720p. Черновик в 360p, апскейл победителя.

Хранение сохранённых интеракций: платный тариф 55 дней (настраивается на 7/14/28/55 в AI Studio), бесплатный — 1 день.

## 11. Коды ошибок

На странице Omni их нет; это коды Interactions API.

`invalid_request` 400 · `failed_precondition` 400 (например, отключён биллинг) · `out_of_range` 416 · `parameter_unknown` 400 · `authentication` 401 · `permission_denied` 403 · `not_found` 404 · `model_not_found` 404 · `already_exists` 409 · `aborted` 409 · `rate_limit_exceeded` 429 · `quota_exceeded` 429 · `too_many_requests` 429 · `cancelled` 499 · `api_error` 500 · `unimplemented` 501 · `service_unavailable` 503 · `deadline_exceeded` 504. Всё не перечисленное сводится к snake_case-версии HTTP-статуса.

Коды **блокировки генерации**: `safety` · `recitation` · `language` · `prohibited_content` · `spii` · `blocklist` · `image_safety` · `image_prohibited_content` · `image_recitation` · `image_other` · `content_blocked`.

Коды **ошибки генерации**: `malformed_function_call` · `malformed_tool_call` · `unexpected_tool_call` · `no_image` · `too_many_tool_calls` · `missing_thought_signature`.

Кода **`no_video` не существует** — как на самом деле проявляется отказ Omni, см. `gemini-omni-flash-failures.md`.

Форма ошибки:

```json
{ "error": { "code": "invalid_request", "message": "..." } }
```

Политика повтора: экспоненциальный backoff с джиттером на 429/408/5xx; **никогда не повторять 400/403**. Python SDK уже сам повторяет транзиентные ошибки до четырёх раз (≈1 с начальная задержка, 60 с максимум).
