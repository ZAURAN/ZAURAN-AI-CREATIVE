# Какие инструменты стоит брать в работу

Это отбор по первичной документации и исходникам, не рейтинг по результатам отрендеренных роликов. Число звёзд не использовано как доказательство качества. Поиск охватывает найденные публичные источники; проверить буквально весь интернет невозможно.

| Направление | Кандидаты | Для чего выбрать |
|---|---|---|
| Монтаж по референсу | [Hypit](https://github.com/hypit-ai/hypit) | Переиспользуемая структура ролика, заменяемые компоненты, привязка графики к словам, вариации |
| Промо продукта | [video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft), [brag](https://github.com/latent-spaces/brag) | Shotcraft — набор постановочных рецептов поверх Remotion; brag — продукт/репозиторий в короткий launch video |
| Reels / Shorts | [vertical-video-editing-skills](https://github.com/nopefallacy/vertical-video-editing-skills) | Workflow коротких вертикальных роликов: hook, A-roll/B-roll, captions, SFX поверх HyperFrames |
| Озвученные объяснялки | [video-talkcraft](https://github.com/Vincentwei1021/video-talkcraft), [Motion Canvas](https://github.com/motion-canvas/motion-canvas) | Narration-driven монтаж или программная векторная анимация для объяснения |
| Основа собственного motion pipeline | [Remotion skills](https://github.com/remotion-dev/skills), [HyperFrames](https://github.com/heygen-com/hyperframes) | React/TS или HTML/GSAP-композиции, параметризация, повторяемый рендер |
| Другой agentic production workflow | [OpenMontage](https://github.com/calesthio/OpenMontage), [hyperframes-helper](https://github.com/robonuggets/hyperframes-helper) | Дополнительные кандидаты для сравнения; не делать их обязательной частью первого прототипа |
| Работа в знакомом редакторе | [After Effects MCP](https://github.com/HeroicSwan/after-effects-mcp), [Resolve MCP](https://github.com/samuelgursky/davinci-resolve-mcp) | Управление установленным редактором, проверка совместимости и ручная доводка |
| Подготовка вырезок | [rembg](https://github.com/danielgatis/rembg), [BiRefNet](https://github.com/ZhengPeng7/BiRefNet) | Обработка фото для композитинга, отдельная проверка мягких краёв |

Для вашего проекта наиболее связный первый стек: существующий ZAURAN для истории и персонажей → Hypit для editable reference workflow → один backend графики → rembg для вырезок → visual/audio QA. Для ролика «вот что умеет мой репозиторий» отдельно использовать brag. Shotcraft и Talkcraft полезны как рецепты и готовые специализированные сценарии.

«Топовая motion-графика» получается за счёт художественного решения, ритма, читаемости, звука и проверки кадров. Наличие skills не заменяет это. Поэтому выбирать следует на трёх одинаковых тестовых брифах из INTEGRATION.md, с одинаковыми ассетами и критериями.

Skillry собран шире видеомонтажа: 141 video, 112 html, 83 image, 47 presentation. HTML, изображения и презентации оставлены, поскольку могут дать графику, сцены, персонажей, диаграммы и композиционные приёмы. Галерея содержит 223 motion, 68 interactive, 51 3d и 47 explainer. Интерактивные работы полезны как визуальные референсы, но не являются автоматически готовыми видео.

Как искать в каталоге: `reels`, `shorts`, `vertical`, `9:16` для коротких роликов; `typography`, `headline`, `title` для текста; `chart`, `map`, `evidence`, `quote` для объяснялок; `character`, `cutout`, `matting` для персонажей/вырезок; `launch`, `product`, `UI` для промо. Поля goodFit/notFor важнее совпадения по названию. Флаги promptPartial и locked не позволяют выдавать опубликованный отрывок за полный production prompt.

Лицензии каждого репозитория, движка, весов и медиа проверяются отдельно. Сохранённая страница и публичный текст не делают сторонние материалы вашим авторским пакетом. Цены и версии — снимок источника на дату сбора, а не обещание сохранения условий.
