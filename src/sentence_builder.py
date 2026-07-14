from src.models import Word, Sentence


class SentenceBuilder:

    MAX_WORDS = 12
    MAX_DURATION = 7.0
    MAX_PAUSE = 0.8

    def build(self, words: list[Word]) -> list[Sentence]:
        sentences = []

        current = []

        for word in words:

            # Existe uma palavra anterior?
            if current:
                pause = word.start - current[-1].end

                if pause >= self.MAX_PAUSE:
                    sentences.append(self._create_sentence(current))
                    current = []

            current.append(word)

            if self._should_split(current):
                sentences.append(self._create_sentence(current))
                current = []

        if current:
            sentences.append(self._create_sentence(current))

        return sentences

    def _should_split(self, words: list[Word]) -> bool:
        first = words[0]
        last = words[-1]

        duration = last.end - first.start

        # Muitas palavras
        if len(words) >= self.MAX_WORDS:
            return True

        # Muito tempo
        if duration >= self.MAX_DURATION:
            return True

        # Terminou frase
        if last.text.endswith((".", "!", "?")):
            return True

        # Vírgula depois de uma frase razoável
        if len(words) >= 5 and last.text.endswith(","):
            return True

        return False

    def _create_sentence(self, words: list[Word]) -> Sentence:
        text = " ".join(word.text.strip() for word in words)

        return Sentence(
            text=text,
            start=words[0].start,
            end=words[-1].end,
            words=words.copy()
        )