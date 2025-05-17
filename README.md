# xml-factory
## Effortless XSD to XML
Ever sigh when you realize you have to craft another sample XML file that matches some gnarly schema? Dread the endless 
cycles of trial-and-error to make your test data *just right*? You’re not alone, and you don’t have to suffer through it
anymore.

This CLI tool is your fast track to sanity. Feed it an XSD, set your preferences, and get instantly valid, 
production-ready XML. No more schema guesswork. No more manual fussing. Just smooth, error-free outputs and your 
valuable time reclaimed.

## Why xml-factory?
- **Supercharge your productivity** — Instantly generate complex, schema-perfect XML. Skip the mindless manual editing 
and focus on real problems
- **No more dreaded data prep** — Forget the ritual of tweaking, fixing, and fixing again. One command, one XML, done
- **Peace of mind** — Know every file matches your schema exactly, catching errors and edge cases before they trip you 
up down the line

## Solving real developer pain
- Churning out example XML for demos and docs
- Building robust automated tests that demand valid, varied XML
- Mocking APIs or simulating integration points on a tight timeline
- Getting new team members up to speed without *can you send me a sample file?*

## How it works
- Download latest release
- Point to your XSD file
- Choose your settings
- Plug in custom value patterns via JSON if needed
- Run. Get schema-compliant XML instantly

```bash
xml-factory --xsd my-schema.xsd --xml sample.xml --root MyRootElem
```

Check out the CLI options to tailor the output for any use case, be it exhaustive QA tests or showcase docs:

```bash
xml-factory --help
```

## Key features
- **Full occurrence control** — Force min/max, require at least one, or randomize, your call
- **Smart value generation** — Default, min, max, or random restriction-compliant values
- **Pattern-aware** — Drop in your own value patterns as needed
- **CLI simplicity** — Fast, deterministic, and effortless

## Current limitations
- `<xsd:list>` and `<xsd:union>` elements not supported
- `<xsd:duration>` and `<xsd:QName>` data types not supported
