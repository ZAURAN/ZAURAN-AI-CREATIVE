# Источники и границы заимствования

Исследование: 13 сентября 2026. Проверялись первичные GitHub-репозитории и доступные SKILL.md, а также документация Adobe. Это выборка близких решений, не полный аудит GitHub. Репозитории меняются; ссылки ниже ведут на текущие ветки, а не закреплённую ревизию. Их код не устанавливался и не исполнялся. Новый скилл написан самостоятельно; чужие файлы/код/длинные фрагменты не включены.

| Источник | Что изучено и полезно | Граница применения |
|---|---|---|
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes), [entry skill](https://github.com/heygen-com/hyperframes/blob/main/skills/hyperframes/SKILL.md) | Разделение намерения, брифа и специализированных workflows; модульная организация видеозадач | HTML-видео и собственный CLI. Команды установки, рендера и обязательные производственные этапы не перенесены в AE-брифинг |
| [kennykankush/skillpack — storyboard](https://github.com/kennykankush/skillpack/blob/main/plugins/videos/skills/storyboard/SKILL.md) | Разделение правды о продукте, визуальных источников, повествования и контроля кадров | Генерация кадров — отдельная работа; не обязательный этап текстового ТЗ |
| [kennykankush/skillpack — motion-handoff](https://github.com/kennykankush/skillpack/blob/main/plugins/videos/skills/motion-handoff/SKILL.md) | Явное намерение, последовательность состояний, ограничения, непрерывность при передаче в анимацию | Ориентирован на AI-video tools. В нашем скилле передача описывает редактируемые элементы AE, а не гарантии генеративной модели |
| [remotion-dev/skills](https://github.com/remotion-dev/skills), [best-practices skill](https://github.com/remotion-dev/skills/blob/main/skills/remotion-best-practices/SKILL.md) | Узкие тематические модули и разделение предметной задачи/исполнения | React и Remotion API не являются AE API. Runtime-зависимости не переносились |
| [LevyBytes/AI-SKILL-adobe-products](https://github.com/LevyBytes/AI-SKILL-adobe-products), [After Effects](https://github.com/LevyBytes/AI-SKILL-adobe-products/blob/main/after-effects/SKILL.md) | Маршрутизация по документации AE, различение expressions/scripting/SDK, внимание к версии | Справочный навигатор, не режиссёрская система. Его контент не включён в пакет |
| [Dakkshin/after-effects-mcp](https://github.com/Dakkshin/after-effects-mcp) | Пример отдельного слоя автоматизации AE | Это MCP-инструмент, не готовый скилл брифинга. Его наличие не означает, что ZAURAN AI DEV использует его или обладает теми же возможностями |

Локально также просмотрены entrypoints `after-effects`, `zauran-ai-creative` и `zauran-story-engine`: первый относится к автоматизации (его рассмотренный runner ориентирован на macOS), остальные — к более широкому креативному и сценарному производству. Новый скилл не меняет их настройки и не зависит от них. Предыдущий просмотренный `motion-graphics` относится к производству HyperFrames; его рендер-процесс не нужен для текстового брифа.

## Первичные технические ориентиры

- [Adobe — управление скоростью между ключами](https://helpx.adobe.com/after-effects/desktop/animate-in-after-effects/speed-between-keyframes/speed.html): движение во времени, Graph Editor и управление скоростью. Использовать как техническую опору при уточнении интерполяции, не как предписание единого стиля.
- [Adobe — Graph Editor для характера движения](https://www.adobe.com/uk/learn/after-effects/web/adjusting-keyframes-dynamic-movement): настройка профиля движения. Наличие Easy Ease само по себе не определяет готовую режиссуру.
- [Adobe — Scripts in After Effects](https://helpx.adobe.com/after-effects/desktop/automate-in-after-effects/automate-animation/scripts.html): scripting относится к исполнению; этот пакет не запускает скрипты.

Вывод исследования: найдены полезные компоненты, но в просмотренной выборке не найдено точного объединения русскоязычного чат-брифинга, четырёх направлений, раскадровки и передачи в ZAURAN AI DEV под AE. Поэтому выбран самостоятельный модульный скилл. Это не утверждение, что аналогов нигде не существует.
