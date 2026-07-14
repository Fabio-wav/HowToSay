const player = document.getElementById("player");
const subtitle = document.getElementById("subtitle");

let current = 0;

/*
    Exibe uma frase do transcript na tela.
*/
function renderOccurrence(occurrence) {

    subtitle.innerHTML = "";

    occurrence.words.forEach(word => {

        const span = document.createElement("span");

        span.textContent = word.text + " ";

        span.dataset.start = word.start;
        span.dataset.end = word.end;

        subtitle.appendChild(span);

    });

}

/*
    Carrega um resultado da pesquisa.
*/
function playResult(index) {

    current = index;

    const r = results[index];

    player.src = r.video;

    player.onloadedmetadata = () => {

        player.currentTime = Math.max(0, r.start - 4);

        player.play();

    };

    document.getElementById("video-name").innerText = r.name;

    document.getElementById("sentence").innerText = r.sentence;

    document.getElementById("counter").innerText =
        `${index + 1} / ${results.length}`;

    document.querySelectorAll(".result").forEach((e, i) => {
        e.classList.toggle("selected", i === index);
    });

    /*
        Mostra inicialmente a primeira frase do transcript.
    */
    if (r.transcript.length > 0) {
        renderOccurrence(r.transcript[0]);
    }

}

/*
    Próximo resultado.
*/
function nextResult() {

    if (current < results.length - 1) {
        playResult(current + 1);
    }

}

/*
    Resultado anterior.
*/
function previousResult() {

    if (current > 0) {
        playResult(current - 1);
    }

}

/*
    Atualiza a legenda em tempo real.
*/
player.addEventListener("timeupdate", () => {

    if (!results.length) return;

    const r = results[current];

    const time = player.currentTime;

    /*
        Descobre qual frase deve aparecer.
    */
    const occurrence = r.transcript.find(o =>
        time >= o.start && time <= o.end
    );

    if (!occurrence) return;

    /*
        Se a frase mudou, recria a legenda.
    */
    if (
        subtitle.dataset.currentStart != occurrence.start
    ) {

        subtitle.dataset.currentStart = occurrence.start;

        renderOccurrence(occurrence);

    }

    /*
        Destaca apenas a palavra falada.
    */
    const spans = subtitle.querySelectorAll("span");

    occurrence.words.forEach((word, i) => {

        if (!spans[i]) return;

        if (
            time >= word.start &&
            time <= word.end
        ) {

            spans[i].classList.add("active");

        } else {

            spans[i].classList.remove("active");

        }

    });

});

/*
    Atalhos do teclado.
*/
document.addEventListener("keydown", e => {

    if (e.key === "ArrowRight") {
        nextResult();
    }

    if (e.key === "ArrowLeft") {
        previousResult();
    }

});

/*
    Carrega o primeiro resultado.
*/
if (results.length) {
    playResult(0);
}

console.log(results);