# Gemini Omni Flash — звук, диалог, музыка

Companion к `gemini-omni-flash.md`. Omni генерирует картинку и звук в **одном проходе**. Звук — не постобработка и не параметр, а проза внутри единственной строки промпта.

## 1. Аудио-поверхности в API нет вообще

- **Нет** флага `generate_audio` / `generateAudio`. У Veo он есть; у Omni нет.
- **Нет** параметра аудиодорожки, нет отдельного поля аудиопромпта, нет ID голоса, нет mute, нет режима немого рендера.
- Единственные поля `response_format` — `type`, `aspect_ratio`, `resolution`, `duration`, `delivery` (+ `gcs_uri` на Vertex).
- Каждый клип возвращается со звуковой дорожкой, спрашивал ты её или нет.
- **Вход аудио в API не поддерживается.** Нельзя подать закадровый голос и попросить Omni подогнать видео под него. Гайды, утверждающие обратное, ошибаются — это самая громкая жалоба практиков на модель. Вход аудио существует только в Flow и приложении Gemini.
- **Редактирование голоса не поддерживается.** Model card прямо говорит, что возможность есть и намеренно придержана: *«As part of editing videos, Gemini Omni Flash is capable of changing people's speech. For now, we are restricting this capability.»*

## 2. Официальное руководство Google по звуку — целиком

> By default the model will try to generate an appropriate audio track for a video. This might not always be what you want. You can use your prompt to describe the type of audio you want. This is especially important if you want music in your video:
> - `Include calm background music`
> - `The video has a high energy techno beat`
> - `The audio is a low tinny radio broadcast in the background, playing a song`

Это вся официальная аудио-секция. Всё ниже — примеры Google плюс разобранная практика.

## 3. Единственная метка, которую использует Google

`Sound design:` — из собственного примера односценного промпта:

```text
…Sunbeams illuminate dust motes in the air. Sound design: Gentle breeze, distant bird chirps. No dialogue.
```

Префиксы `Dialogue:` / `SFX:` / `Ambient:` ходят по гайдам практиков и работают, но **не документированы и не имеют привилегий**. Ни один префикс не обязателен. Документированная форма — обычные предложения; Cloud-гайд рекомендует *«separate sentences in your prompt to describe the audio»*.

## 4. Тишина и негативы

Mute нет. Только негативы в промпте — вот строки самого Google:

```text
No dialogue
No embellishments
No extra sound effects
No dialogue or voiceover.
No text overlay on screen.
No music, just realistic real world sound.
Don't add text.
```

Полный пример из cookbook: `A peaceful campfire glowing softly in a misty forest at dusk. No dialogue or voiceover. No text overlay on screen.`

**Полная тишина недостижима.** `No music, no dialogue` плюс упоминание только room tone даёт чистую подложку, но не тишину.

Правило Vertex-гайда «никогда не пиши no/don't» здесь **не применяй** — оно про заполнение поля `negativePrompt` у Veo, которого у Omni нет. Четыре независимые площадки Google используют для Omni прямое отрицание, включая исполняемый код скилла.

## 5. Диалог

В API-гайде Omni **секции про диалог нет вообще** — диалог там фигурирует только как то, что подавляют. Синтаксис берётся из Cloud-гайда по видеопромптам и гайда DeepMind по Omni.

**Паттерн:**

```text
<визуальное описание говорящего> says/replies/whispers [+ подача]: "<точная реплика>"
```

Личность несёт **именная группа**, а не метка спикера. Именно это заставляет реплику лечь на нужное лицо. Синтаксиса `SPEAKER_1:` **нет**, тегов персонажей нет, формата сценария нет, разметки `<speaker>` нет.

Пример Google на двух говорящих:

```text
A medium shot in a dimly lit interrogation room. The seasoned detective says: Your story has holes. The nervous informant, sweating under a single bare bulb, replies: I'm telling you everything I know. The only other sounds are the slow, rhythmic ticking of a wall clock and the faint sound of rain against the window
```

Пример DeepMind, с кавычками, внутри расширения:

```text
The man in the blue sweater replies: "Did your father go out on the boat too?"
The camera pulls back in one continuous movement as he continues his story: "He used to say that this harbour had a soul. And that the boats were a part of us." The music swells.
```

Ещё диалоговые промпты авторства Google:

```text
Camera slightly pans and we now see she is talking to a man with curly hair, we see man's back, he says "I see it too" dramatic music score
He then stands up walks around the desk to the camera and says "what would you choose?"
```

Правила практиков, совпадающие с употреблением Google:

- **Цитируй реплику дословно**, в прямых кавычках. Пересказ (`the character says something about lunch`) даст несвязанную импровизацию.
- **Называй подачу** — «calm conversational», «hurried whisper», «firm and clear».
- Держи реплики **короткими** — до ~20 слов на 10-секундный клип.
- Пиши диалог **внутри одного связного описания сцены**. Не разбивай 10-секундный промпт на «Shot 1 / Shot 2 / Shot 3».

Проверенный промпт на двух говорящих, где обе реплики легли:

```text
Cinematic night scene inside a rain-streaked parked car. A weary detective in a damp overcoat sits in the driver seat staring through the windshield at a neon-lit storefront. He exhales, then says quietly: "We were never supposed to find her here." The passenger, a younger officer, turns and replies: "Then why did you look?" Rain patters on the roof, distant traffic hum. Anamorphic lens, teal and amber grade, shallow focus, subtle handheld movement. Film grain, photorealistic.
```

**Lip sync Google нигде не называет** — ни как функцию, ни как настройку, ни как ручку. Он эмерджентен из совместного прохода. Ближайшее официальное свидетельство — строка бенчмарка DeepMind о лидирующих результатах по **Speech Adherence** на reference-to-video. Не обещай точность липсинка.

Связка с навыком: актёрскую задачу по-прежнему строй через `tig-acting-task.md`, но результат укладывай в эту грамматику реплики, а не в отдельный блок.

## 6. Музыка

Параметра нет. Только промпт, и Google отмечает музыку как случай, где промпт важнее всего.

- Жанр / энергия: `high energy techno beat`
- Диегетическая рамка: `a low tinny radio broadcast in the background, playing a song`
- Настроение: `calm background music` · `upbeat music` · `Accompanied by calm smooth music.` · `dramatic music score`
- Тайминг: `At 5s the chorus starts in the background audio.`
- При расширении: `The music continues into the chorus` · `The music swells.`

**Синхронизация музыки с картинкой — заявленная сильная сторона** и адресуется промптом:

```text
The lights of the apartments start turning on in sync with the music.
Add harp sounds synchronized to when I touch each fern leaf.
Continuous walking, continuous audio, and style shifts in perfect sync to the beat of the audio.
Coordinate the video cuts to occur on beat drops.
```

Управления BPM, тональностью и стемами нет, разделённых стемов на выходе нет, управления длиной музыки нет.

## 7. SFX и ambience

Тот же прозаический канал. Таксономия Cloud-гайда:

- **Sound effects** — «the sound of a phone ringing», «soft house sounds, the creak of a closet door, and a ticking clock»
- **Ambient noise** — «the sounds of city traffic and distant sirens», «the quiet hum of an office»

Паттерн, надёжно подавляющий музыкальную подложку по умолчанию с сохранением фоли — **назови каждый звук поимённо, затем закрой негативами**:

```text
…the tiny click of a screwdriver tip seating into a screw head, the soft brush of a loupe being lifted, the quiet metallic whisper of tweezers placing a ruby jewel, the gentle steady ticking of the watch mechanism, and a low warm room tone underneath. No music, no dialogue.
```

Поведение по умолчанию, если о звуке не сказано ничего: ambience комнаты + недиегетическая музыка под кинематографичными кадрами + отсутствие диалога.

## 8. Редактирование видео, у которого уже есть звук — механика, которой нет в прозе

Самый практически важный аудиофакт, и **промптом он не достигается**.

Из исполняемого скилла Google, дословно:

> **Keep original audio**: By default, Gemini Omni Flash preserves the existing audio layer (though it may modify or adapt it slightly during generation).
> **Regenerate all audio from scratch**: If you want Gemini Omni Flash to re-create a brand-new audio layer tailored to the new visual style or prompt, you **must** upload the video with its audio stream stripped out. **If any audio stream is present, Gemini Omni Flash will attempt to preserve/modify it instead of starting from scratch.**

Итого: чтобы получить свежий звук на правке, вырежи аудиодорожку **до загрузки**.

```bash
ffmpeg -i original.mp4 -an -c:v copy silent.mp4
```

Google поставляет это как `prep_video.py --strip-audio` / `generate_video.py --strip-audio`. **Никакая формулировка промпта этого не заменяет** — ни «ignore the original music», ни «remove the soundtrack», ни негативы: пайплайн просто протаскивает входной поток дальше.

## 9. Идентичность голоса — только Flow

В API нет. В Flow: модель → Omni Flash → Video → Ingredients → **Add Voices**; ссылка в промпте как `@Voice: Andrew`. Кастомный голос собирается из базового голоса, имени и описания «Voice Performance» («Make the voice sound slightly raspy with a New York accent»), с опциональным 8-секундным превью по «Sample Dialogue». Ограничение: голосовые референсы работают только на генерациях с ingredients, всё остальное вернёт ошибку.

## 10. Язык

*«English (EN) is fully supported, but other languages have not been evaluated, so they may work but results can vary.»*

Промпты пиши по-английски, даже когда пользователь пишет по-русски. Неанглийские реплики — в кавычки, и предупреди о разбросе.

## 11. Известный дефект звука

Инструментированный тест намерил **разброс громкости 26 dB** между генерациями — диалог около −18.2 dBFS против ambience в среднем −44.3 dBFS. Независимый бенчмарк отдельно отметил, что звук Omni приходит очень тихим. **Нормализуй каждый клип в посте, закладывай этот шаг в пайплайн и в оценку сроков.**
