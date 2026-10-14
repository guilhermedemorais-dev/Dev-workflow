# Pinned Frappe UI instruction subset

Upstream: [frappe/frappe-ui](https://github.com/frappe/frappe-ui/tree/d39298ec2155a1c4cda57a4be656568217506982/skills/frappe-ui),
revision `d39298ec2155a1c4cda57a4be656568217506982`.
The source package at that revision declares version 1.0.2; this does not attest
that an arbitrary installed npm package has the same API.

Installed with the official Codex skill-installer GitHub helper into this plugin.
Distribution contains SKILL.md, CORE.md, DATA.md and SETUP.md plus the exact
upstream [MIT notice](LICENSE.md), local metadata and this provenance.
[ORIGIN.json](ORIGIN.json) records source URLs, original and packaged SHA256,
the unchanged upstream body hash, and hashes of omitted evaluation files.

Local changes narrow automatic discovery to compatible Vue 3/Frappe UI work and
prepend the Harness ownership/approval boundary. The upstream component/data/setup
contracts remain intact. SETUP is conditional, not authority to migrate an
existing project or install dependencies in every project. CORE/DATA/SETUP are
unchanged source files; SKILL's upstream body remains after its marked boundary.

The upstream evals folder is omitted: its workflow/scorer is evaluation tooling,
not needed by the linked instruction references and not a runtime dependency.
No upstream evaluation or project setup commands were executed during packaging.
Future updates must repin, audit instructions/licenses/references and rerun tests.
These Markdown skills are available on all operating systems. Only separately
owned executable tools receive OS compatibility selection.
