(function () {
  function connect(svg, boardRect, elA, elB, weight) {
    const a = elA.getBoundingClientRect();
    const b = elB.getBoundingClientRect();
    const x1 = a.left - boardRect.left + a.width / 2;
    const y1 = a.top - boardRect.top + a.height / 2;
    const x2 = b.left - boardRect.left + b.width / 2;
    const y2 = b.top - boardRect.top + b.height / 2;
    const midX = (x1 + x2) / 2 + (Math.random() * 30 - 15);
    const midY = (y1 + y2) / 2 + (Math.random() * 30 - 15);
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", `M ${x1} ${y1} Q ${midX} ${midY} ${x2} ${y2}`);
    path.setAttribute("class", "cb-string");
    path.setAttribute("stroke-width", weight);
    svg.appendChild(path);
  }

  function draw() {
    const board = document.getElementById("board");
    const svg = document.getElementById("svg");
    svg.innerHTML = "";
    const boardRect = board.getBoundingClientRect();
    const verdict = document.getElementById("verdict");
    const suspects = [
      [document.getElementById("s1"), 3.2],
      [document.getElementById("s2"), 2.8],
      [document.getElementById("s3"), 2.4],
      [document.getElementById("s4"), 2.3],
      [document.getElementById("s5"), 1.8],
      [document.getElementById("s6"), 1.5],
      [document.getElementById("s7"), 1.2],
    ];
    suspects.forEach(([el, w]) => connect(svg, boardRect, el, verdict, w));
  }

  window.addEventListener("load", draw);
  window.addEventListener("resize", draw);
  setTimeout(draw, 150);
})();
