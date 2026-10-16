# Режимы и источники

Маршрут выбирает метод; полный workflow доступен через library.py. `search` находит ID, `show ID` возвращает полный документ, `materialize ID --destination NEW_FOLDER` даёт source tree с кодом/references/assets. Не ставь материализованные источники в каталог автоматически обнаруживаемых навыков.

| Режим | Поисковый ключ / источник |
|---|---|
| Озвучка и актёрская речь | own:zauran-voice-director |
| ТЗ для After Effects | own:zauran-ae-brief-director |
| История | zauran-story-engine |
| Персонажи | zauran-character-forge |
| Постановка | zauran-scene-director |
| Генерации | ZAURAN/ZAURAN-AI-CREATIVE root skill |
| Контекст | zauran-context-guard |
| Референс и semantic anchors | hypit-ai/hypit |
| Промо проекта | latent-spaces/brag |
| Кинематографическое промо | Vincentwei1021/video-shotcraft |
| Озвученная объяснялка | Vincentwei1021/video-talkcraft |
| Вертикальный монтаж | nopefallacy/vertical-video-editing-skills |
| HTML-композиции | heygen-com/hyperframes |
| React-композиции | remotion-dev/skills |
| Векторная анимация | motion-canvas/motion-canvas, framework без SKILL.md |
| Другие production workflows | calesthio/OpenMontage; robonuggets/hyperframes-helper |
| After Effects | HeroicSwan/after-effects-mcp |
| DaVinci Resolve | samuelgursky/davinci-resolve-mcp |
| Удаление фона | danielgatis/rembg; ZhengPeng7/BiRefNet; Bria-AI/RMBG-2.0 |
| Видео-маски | facebookresearch/sam2; Barty-Bart/motion-graphics: skills/object-separation |
| Тайминг, easing, характер движения | LottieFiles/motion-design-skill |
| Звуковой проход: SFX по cue, бит-сетка, LUFS | Barty-Bart/motion-graphics: skills/sound-effects |
| B-roll к говорящей голове по транскрипту | Barty-Bart/motion-graphics: skills/motion-broll |
| Стили product explainer: high-energy / default / engaging | Barty-Bart/motion-graphics: skills/explainer-high-energy, explainer-default, explainer-engaging |
| Процедурная анимация в стиле: cut paper, crosshatch, riso, sketchbook, math, pixel, isometric или по референсам | cth9191/animate |
| Форматы сюжета короткой анимации F1–F8 и их инварианты | cth9191/animate: grammar/FORMATS.md, grammar/STORY.md, craft.md |

Границы новых источников:
- LottieFiles/motion-design-skill написан для UI. Для роликов брать характеры движения, карту «эмоция → движение», три слоя движения, правила 1/3, длительность от расстояния и QA-чеклист. Бюджет stagger <500 мс, `prefers-reduced-motion` и масштабирование под платформы относятся к интерфейсам.
- explainer-* синтезируют музыку и SFX осцилляторами. sound-effects это запрещает. Визуальную схему брать из explainer, звук делать через sound-effects.
- motion-broll и explainer-* несут свои рендереры. По правилу одного backend их правила и сценарии переносятся в выбранный backend проекта. Собственный движок источника используется, только когда он выбран backend сегмента.
- Скрипты Barty-Bart написаны под macOS/Linux (`bash setup.sh`, `python3`, `.venv/bin/`). На Windows пути и команды адаптировать.
- cth9191/animate — свой backend: один `<canvas>` в `index.html`, рендер через Playwright и ffmpeg. Работает через три check-in (story, look, storyboard), до утверждённой раскадровки не анимирует. Доказанные форматы: F2, F4, F5. Остальные изучены, но не проверены: говорить об этом при выборе. Партитура синтезируется в коде; с треком пользователя в коде остаются только SFX. Голос через ElevenLabs стоит ~1 кредит за символ: показывать сумму и получать согласие до полной генерации.
- Звуки sound-effects в `sfx/` — CC0. Mixkit скачивается в проект при запуске и не хранится в источнике. Лицензию музыки и площадку публикации проверять по шагу 0 источника.

## Локальные provider workflows

В личном комплекте все 17 skill-папок Higgsfield сохранены целиком; в публичном clone их байтов нет. Поиск `local:` показывает их ID и requires_local_payload. После attach-payload своего provider snapshot materialize сохраняет соседство всех папок для относительных ссылок.

- youtube-script: полный сценарий; ai-host-video/faceless-video: эпизоды в их границах.
- ugc-product-video, ugc-review-video, ugc-try-on-video, ugc-tutorial-video, ugc-unboxing-video, ugc-website-video: разные форматы со своими требованиями.
- video-editing, motion-craft, subtitles, narrator: нативная сборка, motion tracks, captions, timed takes.
- ad-multiplier: целевые варианты имеющегося ролика.
- thumbnail-generation, higgsfield, website-builder: обложки, named presets, действительно запрошенный hosted website.

Для Vox-подобной объяснялки соединять story/VO, источники фактов, карты/диаграммы/цитаты, вырезки и смысловую анимацию. Для мультсцен — character canon, staging, supported model references, continuity и композицию. Для музыкального Reels — beat grid, footage, типографику и captions при наличии речи. Каждый сегмент использует реальный формат backend.

Skillry сохранён по типам video/html/image/presentation и gallery categories motion/interactive/3d/explainer. Non-video материалы могут дать изображения, карты и композиции для ролика. Каталог не превращает студию в обязательный маршрут для любых несвязанных запросов.
