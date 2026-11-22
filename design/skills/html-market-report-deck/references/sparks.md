# Small figures: the drawing beside a number

The small figures that stand beside a number on the cover and the contents: what they may show, and a snippet for each shape. Read at the build, before the cover and the contents are written. A small figure makes a reader want the slide behind the number; it is a picture of what the number is about, not a chart to read values from.

## What a small figure may show

- **A different shape for every item.** On one slide no two small figures are of one kind: three little line charts in a row read as decoration.
- **Real values or no values.** A series is drawn through the values measured, at least three, and bends where they bend. Two values are never joined by a straight line, and no value is invented to make a line bend: a figure of two values is an arrow, a pair of bars or a count. Beside a number that has values behind it (a series by year, a pair, a count), the figure is drawn from them: a pictogram below stands only beside an item with none, and two on a cover drawn with no values read as decoration and were sent back.
- **Counts are exact.** A figure of units holds the number it says (six of ten is six filled and four faint) and carries `data-count` on the group.
- **One colour.** A snippet draws in `currentColor`, with the part that is not the point at a lower opacity; the element around it sets the colour.

Each snippet is an `svg` on a `0 0 96 48` box, set to 96 by 48 pixels beside the number. Change the coordinates to the figure's own values; the shapes here are placeholders.

## A measured series

```html
<svg viewBox="0 0 96 48" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 40 30 30 52 34 88 8"/><path d="M72 8h16v16"/></svg>
```

A point a value measured, x by its date and y by its value; the arrowhead only where the last step rises.

## Two ways apart

```html
<svg viewBox="0 0 96 48" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 24h34M40 24 84 8M40 24l44 16"/><path d="M72 6l12 2-4 12M72 42l12-2-4-12"/></svg>
```

For one thing that split into two courses: one made easy while the other stayed hard.

## Up and down

```html
<svg viewBox="0 0 96 48" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M28 42V8M16 20 28 8l12 12"/><path d="M68 6v34M56 28l12 12 12-12" opacity=".4"/></svg>
```

For two values that moved against each other. The one the number speaks of is the full one.

## Past a mark

```html
<svg viewBox="0 0 96 48" fill="none" stroke="currentColor" stroke-linecap="round"><path d="M6 24h84" stroke-width="2" opacity=".4"/><path d="M52 10v28" stroke-width="2"/><path d="M52 24h38" stroke-width="6"/></svg>
```

For a share that lasts beyond a threshold (ads still running after ninety days): the thick part is the share past the mark.

## Units

```html
<svg viewBox="0 0 96 48" fill="currentColor"><g data-count="5"><circle cx="10" cy="24" r="7"/><circle cx="29" cy="24" r="7"/><circle cx="48" cy="24" r="7" opacity=".3"/><circle cx="67" cy="24" r="7" opacity=".3"/><circle cx="86" cy="24" r="7" opacity=".3"/></g></svg>
```

For "two of five": the filled ones are the count.

## A funnel

```html
<svg viewBox="0 0 96 48" fill="currentColor"><path d="M4 6h88L60 28v16H36V28z" opacity=".85"/></svg>
```

For many that became few.

## A bar and where it went

```html
<svg viewBox="0 0 96 48" fill="currentColor"><rect x="8" y="26" width="18" height="18" rx="3" opacity=".4"/><rect x="38" y="6" width="18" height="38" rx="3"/><path d="M68 36h18M78 28l8 8-8 8" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>
```

For a before and an after of one measure: the bars' heights are the two values.

## Coins

```html
<svg viewBox="0 0 96 48" fill="none" stroke="currentColor" stroke-width="3"><ellipse cx="30" cy="36" rx="20" ry="7"/><ellipse cx="30" cy="27" rx="20" ry="7"/><ellipse cx="30" cy="18" rx="20" ry="7"/><ellipse cx="72" cy="36" rx="16" ry="6" opacity=".4"/></svg>
```

For money one side makes and another does not.

## People

```html
<svg viewBox="0 0 96 48" fill="currentColor"><g data-count="4"><path d="M12 4a6 6 0 1 1 0 12a6 6 0 1 1 0-12zM2 44c0-16 20-16 20 0z"/><path d="M12 4a6 6 0 1 1 0 12a6 6 0 1 1 0-12zM2 44c0-16 20-16 20 0z" transform="translate(24)"/><path d="M12 4a6 6 0 1 1 0 12a6 6 0 1 1 0-12zM2 44c0-16 20-16 20 0z" transform="translate(48)" opacity=".3"/><path d="M12 4a6 6 0 1 1 0 12a6 6 0 1 1 0-12zM2 44c0-16 20-16 20 0z" transform="translate(72)" opacity=".3"/></g></svg>
```

For a share of people: payers among users, founders among entrants.

## One and many

```html
<svg viewBox="0 0 96 48" fill="currentColor"><circle cx="20" cy="24" r="16"/><circle cx="62" cy="14" r="5"/><circle cx="80" cy="14" r="5"/><circle cx="62" cy="34" r="5"/><circle cx="80" cy="34" r="5"/></svg>
```

For one large player beside many small ones.

## Signal bars

```html
<svg viewBox="0 0 96 48" fill="currentColor"><rect x="6" y="30" width="16" height="14" rx="3"/><rect x="30" y="20" width="16" height="24" rx="3"/><rect x="54" y="8" width="16" height="36" rx="3" opacity=".3"/></svg>
```

For how strong a signal is; the same three steps as the verdict mark of the scenes.
