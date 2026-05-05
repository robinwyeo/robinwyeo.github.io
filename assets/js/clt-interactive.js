(function () {
  if (!window.cltChartJsReady) {
    window.cltChartJsReady = new Promise(function (resolve, reject) {
      if (window.Chart) {
        resolve();
        return;
      }
      var script = document.createElement("script");
      script.src = "https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js";
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  if (window.renderCLTInteractivePlot) {
    return;
  }

  function addStyles() {
    if (document.getElementById("clt-widget-styles")) {
      return;
    }
    var style = document.createElement("style");
    style.id = "clt-widget-styles";
    style.textContent = [
      ".clt-widget{border:1px solid #ddd;border-radius:8px;margin:1.5rem 0;padding:1rem;background:#fff}",
      ".clt-widget__controls{display:flex;flex-wrap:wrap;gap:.75rem;align-items:center;margin-bottom:.75rem}",
      ".clt-widget__controls input[type=range]{max-width:420px;width:100%}",
      ".clt-widget__status{color:#666;font-size:.9rem}",
      ".clt-widget__canvas-wrap{height:420px;position:relative}"
    ].join("");
    document.head.appendChild(style);
  }

  function seededRandom(seed) {
    return function () {
      seed |= 0;
      seed = (seed + 0x6D2B79F5) | 0;
      var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function normalPdf(x, mean, std) {
    var z = (x - mean) / std;
    return Math.exp(-0.5 * z * z) / (std * Math.sqrt(2 * Math.PI));
  }

  function drawStandardNormal(rng) {
    var u = 1 - rng();
    var v = 1 - rng();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  function drawSampleMean(distribution, n, rng) {
    var i;
    var sum = 0;

    if (distribution === "dice") {
      for (i = 0; i < n; i += 1) {
        sum += Math.floor(rng() * 6) + 1;
      }
      return sum / n;
    }

    if (distribution === "exponential") {
      for (i = 0; i < n; i += 1) {
        sum += -Math.log(1 - rng());
      }
      return sum / n;
    }

    if (distribution === "mixture") {
      var rightCount = 0;
      for (i = 0; i < n; i += 1) {
        if (rng() < 0.7) {
          rightCount += 1;
        }
      }
      var leftCount = n - rightCount;
      var rightSum = rightCount * 5 + Math.sqrt(rightCount) * 2 * drawStandardNormal(rng);
      var leftSum = leftCount * -4 + Math.sqrt(leftCount) * drawStandardNormal(rng);
      return (rightSum + leftSum) / n;
    }

    throw new Error("Unknown CLT distribution: " + distribution);
  }

  function quantile(sortedValues, p) {
    var idx = Math.min(sortedValues.length - 1, Math.max(0, Math.floor(p * sortedValues.length)));
    return sortedValues[idx];
  }

  function buildHistogram(values, bins, preferredRange) {
    var sorted = values.slice().sort(function (a, b) { return a - b; });
    var min = preferredRange ? preferredRange[0] : quantile(sorted, 0.005);
    var max = preferredRange ? preferredRange[1] : quantile(sorted, 0.995);
    var padding = (max - min) * 0.025 || 1;
    min -= padding;
    max += padding;

    var binWidth = (max - min) / bins;
    var counts = Array.from({ length: bins }, function () { return 0; });
    var included = 0;

    values.forEach(function (value) {
      if (value < min || value > max) {
        return;
      }
      var idx = Math.min(bins - 1, Math.floor((value - min) / binWidth));
      counts[idx] += 1;
      included += 1;
    });

    var histogram = counts.map(function (count, idx) {
      return {
        x: min + (idx + 0.5) * binWidth,
        y: count / (included * binWidth)
      };
    });

    return { histogram: histogram, min: min, max: max };
  }

  function simulate(config, n) {
    var rng = seededRandom((config.seed || 1) + n * 1009);
    var trials = config.trials || 5000;
    var maxTrials = config.maxTrials || 5000;
    if (trials > maxTrials) {
      trials = maxTrials;
    }
    var values = [];
    var useApprox = (n * trials) > 1500000;

    if (useApprox) {
      var approxSd = config.popStd / Math.sqrt(n);
      for (var j = 0; j < trials; j += 1) {
        values.push(config.popMean + approxSd * drawStandardNormal(rng));
      }
      return values;
    }

    for (var i = 0; i < trials; i += 1) {
      values.push(drawSampleMean(config.distribution, n, rng));
    }
    return values;
  }

  function drawCanvasFallback(canvas, histData, normalLine, titleText) {
    var ctx = canvas.getContext("2d");
    if (!ctx) {
      return false;
    }
    var width = canvas.clientWidth || 800;
    var height = canvas.clientHeight || 420;
    canvas.width = width;
    canvas.height = height;

    var margin = { top: 44, right: 20, bottom: 42, left: 56 };
    var plotW = width - margin.left - margin.right;
    var plotH = height - margin.top - margin.bottom;
    if (plotW <= 0 || plotH <= 0) {
      return;
    }

    var maxY = 0;
    var i;
    for (i = 0; i < histData.length; i += 1) {
      if (histData[i].y > maxY) {
        maxY = histData[i].y;
      }
    }
    for (i = 0; i < normalLine.length; i += 1) {
      if (normalLine[i].y > maxY) {
        maxY = normalLine[i].y;
      }
    }
    maxY = maxY * 1.1 || 1;

    var minX = histData[0].x;
    var maxX = histData[histData.length - 1].x;
    var binW = histData.length > 1 ? histData[1].x - histData[0].x : (maxX - minX) || 1;
    minX -= binW / 2;
    maxX += binW / 2;

    function pxX(x) {
      return margin.left + ((x - minX) / (maxX - minX)) * plotW;
    }
    function pxY(y) {
      return margin.top + plotH - (y / maxY) * plotH;
    }

    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, width, height);

    ctx.fillStyle = "#1f1f1f";
    ctx.font = "600 16px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(titleText, width / 2, 24);

    ctx.strokeStyle = "#444";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(margin.left, margin.top);
    ctx.lineTo(margin.left, margin.top + plotH);
    ctx.lineTo(margin.left + plotW, margin.top + plotH);
    ctx.stroke();

    ctx.fillStyle = "rgba(53, 120, 160, 0.68)";
    var barPxW = Math.max(1, (plotW / Math.max(1, histData.length)) * 0.92);
    for (i = 0; i < histData.length; i += 1) {
      var x = pxX(histData[i].x) - barPxW / 2;
      var y = pxY(histData[i].y);
      ctx.fillRect(x, y, barPxW, margin.top + plotH - y);
    }

    ctx.strokeStyle = "#111";
    ctx.setLineDash([6, 4]);
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (i = 0; i < normalLine.length; i += 1) {
      var lx = pxX(normalLine[i].x);
      var ly = pxY(normalLine[i].y);
      if (i === 0) {
        ctx.moveTo(lx, ly);
      } else {
        ctx.lineTo(lx, ly);
      }
    }
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.fillStyle = "#333";
    ctx.font = "12px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("Sample mean", margin.left + plotW / 2, height - 10);
    ctx.save();
    ctx.translate(14, margin.top + plotH / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText("Density", 0, 0);
    ctx.restore();
    return true;
  }

  window.renderCLTInteractivePlot = function (containerId, config) {
    addStyles();

    window.cltChartJsReady.then(function () {
      var container = document.getElementById(containerId);
      if (!container) {
        return;
      }

      container.innerHTML = [
        '<div class="clt-widget">',
        '  <div class="clt-widget__controls">',
        '    <label for="' + containerId + '-slider"><strong>Sample size n:</strong> <span id="' + containerId + '-value"></span></label>',
        '    <input id="' + containerId + '-slider" type="range" min="1" max="250" step="1">',
        '    <span id="' + containerId + '-status" class="clt-widget__status"></span>',
        '  </div>',
        '  <div class="clt-widget__canvas-wrap"><canvas id="' + containerId + '-canvas"></canvas></div>',
        '</div>'
      ].join("");

      var slider = document.getElementById(containerId + "-slider");
      var valueLabel = document.getElementById(containerId + "-value");
      var status = document.getElementById(containerId + "-status");
      var canvas = document.getElementById(containerId + "-canvas");
      var chart;

      slider.value = config.nDefault || 30;

      function redraw() {
        var n = parseInt(slider.value, 10);
        valueLabel.textContent = n;
        status.textContent = "Simulating...";

        try {
          var values = simulate(config, n);
          var preferredRange = config.distribution === "dice" && n === 1 ? [0.5, 6.5] : null;
          var hist = buildHistogram(values, config.bins || 60, preferredRange);
          var se = config.popStd / Math.sqrt(n);
          var normalLine = [];
          var steps = 160;
          for (var i = 0; i <= steps; i += 1) {
            var x = hist.min + (hist.max - hist.min) * (i / steps);
            normalLine.push({ x: x, y: normalPdf(x, config.popMean, se) });
          }

          if (chart) {
            chart.destroy();
          }

          if (window.Chart) {
            chart = new Chart(canvas, {
            data: {
              datasets: [
                {
                  type: "bar",
                  label: "Simulated sample means",
                  data: hist.histogram,
                  parsing: false,
                  backgroundColor: config.fillColor,
                  borderColor: "#ffffff",
                  borderWidth: 0.5
                },
                {
                  type: "line",
                  label: "CLT normal approximation",
                  data: normalLine,
                  parsing: false,
                  borderColor: "#111111",
                  borderDash: [6, 5],
                  borderWidth: 2,
                  pointRadius: 0,
                  tension: 0.2
                }
              ]
            },
            options: {
              animation: false,
              maintainAspectRatio: false,
              plugins: {
                title: {
                  display: true,
                  text: config.title + " (" + (n === 1 ? config.rawLabel : "n = " + n) + ")",
                  font: { size: 16, weight: "bold" }
                },
                legend: { position: "bottom" }
              },
              scales: {
                x: {
                  type: "linear",
                  min: hist.min,
                  max: hist.max,
                  grace: 0,
                  title: { display: true, text: "Sample mean" }
                },
                y: {
                  beginAtZero: true,
                  title: { display: true, text: "Density" }
                }
              }
            }
            });
          } else {
            var ok = drawCanvasFallback(
              canvas,
              hist.histogram,
              normalLine,
              config.title + " (" + (n === 1 ? config.rawLabel : "n = " + n) + ")"
            );
            if (!ok) {
              status.textContent = "Render error: canvas context unavailable";
              return;
            }
          }

          status.textContent = values.length.toLocaleString() + " simulated trials";
        } catch (err) {
          var okErr = drawCanvasFallback(canvas, [{ x: -1, y: 0 }, { x: 1, y: 0 }], [{ x: -1, y: 0 }, { x: 1, y: 0 }], "Rendering fallback");
          if (!okErr) {
            container.innerHTML = "<p><strong>Interactive chart failed:</strong> canvas context unavailable.</p>";
          } else {
            status.textContent = "Render error: " + (err && err.message ? err.message : "unknown");
          }
        }
      }

      slider.addEventListener("change", redraw);
      redraw();
    }).catch(function () {
      var container = document.getElementById(containerId);
      if (container) {
        container.innerHTML = "<p><strong>Interactive chart failed to load.</strong> Please enable JavaScript and refresh the page.</p>";
      }
    });
  };
}());
