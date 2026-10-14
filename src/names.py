"""Compositional fiction-name generation.

Names of places and subjects are produced by **combining** pools rather than
being drawn from a short fixed list. A lookup table of ~35 place names was
reused 12-17 times per region across 69-331 groups, which would have made the
place name itself a detectable artefact of how the data was built.

Design:

    place  = real prefecture-level city  +  fictional district/street
    outlet = fictional brand stem        +  media suffix
    org    = (real city | fictional stem) +  organisation suffix
    person = fictional name pool

Real city names are used only as geographic anchors. They never combine with a
real organisation, real media outlet or real person, so no combination can be
read as a statement about an actual body.
"""

from common import FICTION, rng_for


def _pick(seq, rng):
    return seq[rng.randrange(len(seq))]


class NameFactory:
    """Deterministic combinatorial name source bound to one region and language."""

    _counter = [0]

    def __init__(self, region, language, seed_key):
        self.region = region
        self.language = language
        # Salt the per-group RNG with a monotonically increasing counter so that
        # consecutive groups do not repeatedly land on the same pool entries.
        NameFactory._counter[0] += 1
        self.rng = rng_for("names", seed_key, region, language, NameFactory._counter[0])
        self._places = []
        self._outlets = []
        self._orgs = []
        self._persons = []

    # ------------------------------------------------------------------ place
    def _city(self):
        cities = FICTION["real_cities"].get(self.region)
        if not cities:
            cities = FICTION["real_cities"]["CN" if self.language.startswith("zh") else "NA"]
        return _pick(cities, self.rng)

    def _district(self):
        d = FICTION["fictional_districts"].get(self.region)
        if not d:
            d = FICTION["fictional_districts"]["CN" if self.language.startswith("zh") else "NA"]
        return _pick(d, self.rng)

    def place(self):
        """Real city + fictional district."""
        city, district = self._city(), self._district()
        if self.language == "en":
            if district.endswith(("County", "Shire", "District", "Region")):
                return f"{city}, {district}"
            return f"{city}, {district}"
        if self.language == "zh-Hant":
            if district.endswith(("區", "里", "街", "道", "坊")):
                return f"{city}{district}"
            return f"{city}{district}"
        if district.endswith(("区", "里", "街", "道", "坊")):
            return f"{city}{district}"
        return f"{city}{district}"

    def place_short(self):
        """City only, for compact UI slots."""
        return self._city()

    # ----------------------------------------------------------------- outlet
    def outlet(self):
        """Fictional media outlet name."""
        stems = FICTION["fictional_brand_stems"]
        if self.language == "en":
            p = _pick(stems["en"]["prefix"], self.rng)
            s = _pick(stems["en"]["media_suffix"], self.rng)
            return f"{p} {s}"
        p = _pick(stems["CN"]["prefix"], self.rng)
        s = _pick(stems["CN"]["media_suffix"], self.rng)
        return f"{p}{s}"

    # ------------------------------------------------------------ institution
    def institution(self):
        """Fictional authority name: fictional stem + official suffix."""
        suffixes = FICTION["organization_suffixes"].get(self.region)
        if not suffixes:
            suffixes = FICTION["organization_suffixes"]["CN" if self.language.startswith("zh") else "NA"]
        suffix = _pick(suffixes, self.rng)
        if self.language == "en":
            return f"{self._city()} {suffix}" if False else _pick(
                FICTION["fictional_brand_stems"]["en"]["prefix"], self.rng) + " " + suffix
        stem = _pick(FICTION["fictional_brand_stems"]["CN"]["prefix"], self.rng)
        return f"{stem}{suffix}"

    # ---------------------------------------------------------------- person
    def person(self):
        pool = FICTION["fictional_persons"].get(self.region)
        if not pool:
            pool = FICTION["fictional_persons"]["CN" if self.language.startswith("zh") else "NA"]
        return _pick(pool, self.rng)

    # ------------------------------------------------------------- assignment
    def prepare(self, counts):
        """Pre-draw distinct names for the slots in one image.

        Each category draws independently, so two slots in the same figure never
        receive identical text.
        """
        def distinct(fn, n):
            seen, out = set(), []
            guard = 0
            while len(out) < n and guard < n * 20:
                guard += 1
                v = fn()
                if v not in seen:
                    seen.add(v)
                    out.append(v)
            while len(out) < n:            # fall back if the pool is tiny
                out.append(fn())
            return out

        self._places = distinct(self.place, max(counts.get("place", 1), 1) + 1)
        self._outlets = distinct(self.outlet, max(counts.get("outlet", 1), 1))
        self._orgs = distinct(self.institution, max(counts.get("org", 1), 1) + 1)
        self._persons = distinct(self.person, max(counts.get("person", 1), 1) + 1)

    def nth_place(self, i=0):
        if not self._places:
            self._places = [self.place() for _ in range(3)]
        return self._places[i % len(self._places)]

    def nth_outlet(self, i=0):
        if not self._outlets:
            self._outlets = [self.outlet()]
        return self._outlets[i % len(self._outlets)]

    def nth_org(self, i=0):
        if not self._orgs:
            self._orgs = [self.institution() for _ in range(3)]
        return self._orgs[i % len(self._orgs)]

    def nth_person(self, i=0):
        if not self._persons:
            self._persons = [self.person() for _ in range(3)]
        return self._persons[i % len(self._persons)]
