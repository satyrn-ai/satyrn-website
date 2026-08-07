document$.subscribe(function () {
  const fmt = new Intl.DateTimeFormat(undefined, {
    year: "numeric", month: "long", day: "numeric", timeZone: "UTC"
  })
  document.querySelectorAll("time[datetime]").forEach(function (el) {
    const raw = el.getAttribute("datetime")
    if (!/^\d{4}-\d{2}-\d{2}$/.test(raw)) return
    const [y, m, d] = raw.split("-").map(Number)
    el.textContent = fmt.format(new Date(Date.UTC(y, m - 1, d)))
  })
})
