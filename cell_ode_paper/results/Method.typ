#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
  footer: align(center)[#context text(size: 10pt)[#counter(page).display("1")]]
)
#set cite(style: "apa") // acs with author name was bugged
#set text(font: "Liberation Serif", size: 11pt, fill: black)
#set par(justify: true, leading: 0.65em)
#set heading(numbering: "1.1")
#set math.equation(numbering: "(1)")
#show heading: set text(fill: black, weight: "bold")
// Figure text
#show figure.caption: set text(size: 10pt, style: "italic")
#show figure.caption: it => [#strong[#it.supplement~#it.counter.display():]~#it.body]

#let hdr(body) = table.cell(fill: rgb("#e8eef4"))[*#body*]
#let weak = rgb("#fdecea")
// content

- Method is well described for all elements of the task 
- Choices made during data preprocessing and model training are well described 
- Evaluation metrics are presented

Brainstorm:
worst performing overall biome, Why do we include certain features from SHAP scores?

= Variables Explained
== How macro F1 is computed

Take one biome, say biome 11, and treat it as "positive" with every other biome as "negative". Over the test set you count:

TP: cells that really are biome 11 and were predicted as 11

FP: cells predicted as 11 that are actually something else

FN: cells that really are 11 but were predicted as something else

Then:

precision = TP / (TP + FP). Of the cells the model called biome 11, how many really were?

recall = TP / (TP + FN). Of the real biome 11 cells, how many did the model find?

F1 = 2 · precision · recall / (precision + recall). This is the harmonic mean of the two.



= Random Forest Biome Models: Performance Comparison
 
Target: `Biome_obs` (17 biomes, 59,191 grid cells). All models are default `RandomForestClassifier` with an 80/20 random split (`random_state=42`) unless stated otherwise.
 
== Table 1: Multi-class model, by evaluation scenario
 
#figure(
  table(
    columns: (2.6fr, 1.6fr, 1fr, 1fr, 1.1fr, 1fr),
    align: (left, left, center, center, center, center),
    stroke: 0.5pt + luma(180),
    inset: 6pt,
    hdr[Scenario], hdr[Train / test cells], hdr[Test accuracy], hdr[Baseline accuracy], hdr[Balanced accuracy], hdr[Macro F1],
    [Global (random split)], [47,352 / 11,839], [0.953], [0.187], [0.907], [0.914],
    [India only (random split)], [883 / 221], [0.905], [0.249], [0.905], [0.916],
    [Train outside India → test India], [58,087 / 1,104], [0.849], [0.017], [0.883], [0.888],
  ),
  caption: [Training accuracy is 1.0 in every scenario (fully grown trees), so it is not reported as a comparison metric.],
)
 
== Table 2: Feature ablation (binary one-vs-rest models, global)
 
#figure(
  table(
    columns: (3fr, 1.4fr),
    align: (left, center),
    stroke: 0.5pt + luma(180),
    inset: 6pt,
    hdr[Feature set], hdr[Mean F1 across biomes],
    [All features], [0.902],
    [Without Lat/Lon], [0.893],
    [Without Biome_Cmax / Biome_LAI], [0.883],
    [Without Lat/Lon and Biome_Cmax / Biome_LAI], [0.836],
  ),
)
 
== Table 3: Weakest biomes (per-class F1)
 
#figure(
  table(
    columns: (2.6fr, 3fr),
    align: (left, left),
    stroke: 0.5pt + luma(180),
    inset: 6pt,
    hdr[Scenario], hdr[Weakest biomes (F1)],
    [Multi-class, global], [7 (0.67), 3 (0.78), 11 (0.83)],
    [Multi-class, train outside India → India], [15 (0.72), 14 (0.81), 11 (0.82), 8 (0.83)],
    [Binary, spatial hold-out (India)], [15 (0.70), 11 (0.73), 8 (0.86), 10 (0.86)],
  ),
)
 
== Table 4: Climate-variable model (to be filled in)
 
#figure(
  table(
    columns: (2.6fr, 1fr, 1fr, 1.1fr, 1fr),
    align: (left, center, center, center, center),
    stroke: 0.5pt + luma(180),
    inset: 6pt,
    hdr[Model], hdr[Test accuracy], hdr[Baseline accuracy], hdr[Balanced accuracy], hdr[Macro F1],
    [Climate only (precip., Tmax, Tmin, SW rad.)], [—], [—], [—], [—],
  ),
)
 
#v(1em)
 
#block(
  fill: rgb("#f6f6f0"),
  stroke: (left: 3pt + rgb("#b59f3b")),
  inset: 10pt,
  width: 100%,
)[
  *Note: why these metrics?*
 
  *Accuracy* is the fraction of cells assigned the correct biome. It is easy to read and is the standard headline number, but with 17 imbalanced classes it can look good even when rare biomes are missed. In the binary models the "never this biome" baseline already scores 0.81–0.998, so accuracy is never reported without its baseline.
 
  *Baseline accuracy* (always predict the most common training class) is the floor a model must beat. It puts accuracy in context and shows how much skill the forest adds, for example 0.953 against 0.187 globally.
 
  *Balanced accuracy* is the mean per-class recall. Each biome counts equally regardless of how many cells it has, so a model cannot score well by ignoring small biomes such as 3, 7 and 11. It answers "does the model find every biome?"
 
  *F1 score* is the harmonic mean of precision and recall. It penalises both false positives (cells wrongly labelled as a biome) and false negatives (cells of that biome missed), which matters for rare classes. We report *macro F1* (unweighted mean over biomes) so small biomes have the same influence as large ones, and *per-class F1* to identify which biomes fail.
 
  *Evaluation scenarios.* The random split measures in-distribution performance. The train-outside-India, test-India hold-out is a spatial split that measures transfer to an unseen region. The drop from 0.953 to 0.849 accuracy shows that a random split alone overstates real-world skill, which matters because the model will later be used for projections.
 
  *Why not training accuracy?* It is 1.0 for default random forests because the trees are fully grown, so it says nothing about generalisation and is excluded from comparison.
 
  *Ablation (mean F1)* shows which inputs carry the signal, for example the cost of removing location or the LPJ-GUESS-derived `Biome_Cmax` / `Biome_LAI` features.
]
 