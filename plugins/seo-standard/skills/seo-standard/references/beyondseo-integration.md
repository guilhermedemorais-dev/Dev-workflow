# BeyondSEO Integration

BeyondSEO 2.9.1 is the pinned evidence engine for SEO Standard.

Upstream: https://github.com/beyondtahir/beyondseo
License: MIT

The runtime is vendored as a release ZIP under
`plugins/seo-standard/vendor/beyondseo/`. Normal use must prefer the local
vendored copy so execution does not depend on the upstream repository remaining
available.

## Runtime boundary

SEO Standard calls the local gateway/bootstrap. BeyondSEO performs crawling and
evidence collection. SEO Standard interprets results and turns them into Task
requirements, copy, priorities and validation checks.

## Default audit scope

For ordinary landing pages and small sites:

1. inspect the target page and core supporting pages;
2. use technical/on-page/schema/AEO/GEO/conversion checks;
3. use competitor/backlink/reputation modules only when materially relevant;
4. produce exact affected URLs and acceptance checks;
5. after implementation, run a fresh audit folder and compare results.

A crawler result is evidence, not authority to alter code or publish.
