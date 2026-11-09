#import "@preview/touying:0.8.0": *
#import themes.metropolis: *
#import "@preview/cetz:0.5.2"
#import "@preview/fletcher:0.5.8" as fletcher: node, edge
#import "@preview/numbly:0.1.0": numbly
#import "@preview/theorion:0.6.0": *
#import "@preview/lilaq:0.6.0" as lq
#import cosmos.clouds: *
#show: show-theorion
#import "viz/report.typ" : *
#import "figures/cell-rk45.typ" as cell-rk45
#import "figures/cell-euler.typ" as cell-euler
#import "figures/nanog-lif.typ" as nanog-lif
#import "viz/methodology.typ": methodology

#let primary-color = rgb("#eb811b")

#show: metropolis-theme.with(
  aspect-ratio: "16-9",
  // align: horizon,
  // config-common(handout: true),
  config-common(frozen-counters: (theorem-counter,)),  // freeze theorem counter for animation
  config-info(
    title: [Keeping Stem Cells "Stem" with STEM],
    subtitle: [],
    author: [Joseph Binns, Matti Bleckmann, Preston Stover],
    date: datetime.today(),
  ),
)
#title-slide()
#let body-size = 20pt
#let note-size = 16pt
#set text(size: body-size)

#include "viz/intro.typ"
#include "viz/circuit.typ"

#slide(title: [Methodology])[
  #methodology(primary-color)
]

#slide(title: [Euler Results])[
  #set text(size: 10pt)
  #align(center)[Forward Euler, fixed step $h = 0.1$]
  #align(center)[
    #utils.fit-to-width(100%)[
      #cell-euler.plot()
    ]
  ]
  #v(4pt)
  #cell-euler.error-note()
]

#slide(title: [RK-45 Results])[
  #set text(size: 10pt)
  #align(center)[Adaptive RK45, maximum step $h = 0.1$]
  #align(center)[
    #utils.fit-to-width(100%)[
      #cell-rk45.plot()
    ]
  ]
  #v(4pt)
  #cell-rk45.error-note()
]

#slide(title: [Errors])[
  #set text(size: 18pt)
  #align(center + horizon)[
    Global error estimate:

    #text(size: 64pt, weight: "bold")[
      $frac(abs(y_h - y_(2h)), 2^p - 1)$
    ]
  ]
]

#slide(title: [Nanog pluripotency?])[
  #align(center + horizon)[
    #text(size: 30pt, weight: "bold")[
      Can we make Nanog overexpression result in persistent pluripotency?
    ]
  ]
]

#slide(title: [Nanog pluripotency?])[
  #set text(size: 10pt)
  #align(center)[
    #utils.fit-to-width(100%)[#nanog-lif.plot()]
  ]
]

#include "viz/toggle_intro.typ"
#include "viz/toggle_figure.typ"

#slide(title: [Thank you!])[
  #align(center + horizon)[
    #text(size: 36pt, weight: "bold")[Any questions?]
    #place(left + horizon, image("figures/mouse_joe.svg", width: 24%))

  ]
]
