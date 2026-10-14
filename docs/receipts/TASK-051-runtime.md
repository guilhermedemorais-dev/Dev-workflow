# TASK-051 runtime validation receipt

Task TASK-051, list ui-runtime, revision1. Authorized isolated proof artifacts only;
no production UI/library installation or shipped third-party components. Current
QA_STATUS PASS (representative Windows/Linux runtime only), macOS/Windows11 NOT_VALIDATED. Harness owns final reconciliation.

SKILL_RECEIPT: complete frontend-testing-debugging, ui-ux-standard and
qa-testing-standard read; QA test-strategy read. Applied target-flow/user-visible
checks, fresh runtime/screenshot proof, separate fixture from backend integration,
license provenance, no support assertion without actual runtime. Browser plugin's
`browser` skill absent; regular Playwright fallback explicitly permitted.

COMPONENT_SOURCE_INVENTORY: no client project UI exists; selected official pinned
Frappe FormControl+Button for compatibleVue form, ReactBits BlurText TS-CSS forReact.
Frappe source d39298ec2155a1c4cda57a4be656568217506982 package1.0.2 (not1.0.1),
MIT; pinned SETUP requires Node>=20.19, Vue>=3.5,Tailwind>=3.4.2<4 and Vite7.
Generic local form uses no backend; frappeProxy/jinjaBootData/buildConfig disabled;
no Frappe useCall against REST. Pinned SETUP leaves optimizeDeps to plugin, which
supersedes older unpinned Context7 snippets. Vuefixture packageinstalledfile:../frappe-source.

ReactBits source496968c4117e21278f13917201b7d615bc5e7450,
src/ts-default/TextAnimations/BlurText/BlurText.tsx fetched rawexactpin in localproof.
LICENSE.md MIT+CommonsClause copiedlocalproof; no sourcecomponentsredistributedHarness.
Custom owned example wrapper provides statechange button and static reduced-motion
fallback; no WebGL/GPU dependency. Known externalcode is only this local testfixture.

QA scenarios: Frappe / -> emptySave -> requiredmessage; Nameinput -> Save -> Savedname.
React / -> actual BlurText mount -> change text -> updateddisplay/animationcomplete;
mobileprefers-reduced-motion -> staticfulltext/noanimation. Desktop1280/mobile390,
identity/notblank/frameworkoverlay/pageconsole/overflow/screenshots. NativeEdge
installed available. Productionbuild plusbrowser target; noAPI,persistence/auth proof.

Scoped runtimepreparation: NodeWindows24.19 existing, trustedpnpmJS11.25.0;
ignore-scripts localprivateprojects; no globalPATH/MCP changes. React19.2.4,
ReactDOM19.2.4,Motion12.35.0,Vite7.3.2,PlaywrightCore1.58.2. WindowsVueinstallation
completed successfully. LinuxKaliNode24.19.0 and browser verified and reused.
PortableLinuxNode24.19 archive downloadedofficial
SHA25614b342e71204f811bde6153be8e04b62aef63c236fef92b55f9c83154b409647 verified,
extractioninterruptedunderhostmemorypressure; unused because existingnativeKaliNode
was subsequently verified. Final Linux results are below.

Proofs/logs/screenshot paths outside repository: work/ui-proofs/{vue-proof,react-proof},
run-proof.mjs, evidence/. Source receipt is the only source write by runtime executor.
Tokenusage NOT_AVAILABLE. No commit, merge, publication or global configmutation.

## Final runtime checkpoint, Windows and Linux representative PASS

Windows: native Node24.19.0, pnpm11.25.0, Edge headless existinginstalledbinary.
Linux: KaliGNU/LinuxRolling2026.2 underWSL, native /usr/bin/node24.19.0 and
existing Chromium1247 readonly. No use of WindowsNode/browser to claimLinux.
Linux projects copied to /tmp/task051-ui, new native node_modules installed using
same frozen pnpm-lock files, ignore-scripts, no globalPATH/MCP modifications.
Unused portableLinuxNodearchive remained scratch; existingNode used instead.

Dependencies: FrappeUI1.0.2 fromexactpinnedlocalsource, Vue3.5.30,
VueRouter4.6.4,Tailwind3.4.19,PostCSS8.5.6,Autoprefixer10.4.24,
Vite7.3.2,pluginVue6.0.4. React19.2.4,ReactDOM19.2.4,Motion12.35.0,
transitiveFramerMotion12.43.0 locked,PlaywrightCore1.58.2 bothproofs.

Executed full productionbuild then isolated browsercontext perdesktop1280x800 and
mobile390x800, localhost127.0.0.1 ports4511Vue/4512React. Meaningful nonblankheading,
correcttitle/URL, no page/consoleerrors, no horizontaloverflow, screenshotcaptured.
Vue bothOS/viewports: clickSaveempty -> Namerequired; fillOwnedQA -> Save ->
SavedOwnedQA, realFrappeFormControlv-model and Button event. Localownedstateonly,
noAPI,Frappebackend,authentication,persistence or productionbusinessflow claim.
React bothOS/viewports: changebutton -> Updatedinterfaceproof; actualBlurText motion
finishes desktop; mobileprefers-reduced-motion context rendersstaticfulltext and
getAnimations(subtree) length0. This verifies ownedwrapperfallback, not that every
ReactBitscomponentautomaticallysupportsreducedmotion. NoGPU/WebGLcomponents used.

Initialproofharnessfailure CommonJSPlaywrightimport destructuring corrected to
createRequire outsideproductsource. InitialVueTailwindcontentwarning due harnesscwd
corrected process.chdir(proofroot), finalrebuildstyles425.24KB with actualtokens.
ReactRollupignored-use-client directive warnings are expectedSPA bundlingwarnings;
finalbrowserconsoleclean. No externalfonts required; GooglefontsCSS request stubbed
empty if present, localInterfonts bundled. Builds alone were nevercalledruntimePASS.
WindowsVue finalbuild12.11s;LinuxVue6.87s;LinuxReact1.76s. Fullcommands/logs outside
repo work/ui-proofs/{vue,react}-{windows,linux}-build-browser.log, run-proof.mjs.

Artifacts copied to chatoutputs forreview: vue-windows.json/react-windows.json,
vue-linux.json/react-linux.json and corresponding1280/390PNGs. Sourcecomponentcode
and dependencies remain localworkproofs, not shippedHarness. Browserplugin unavailable
fallbackreason documentedabove. Browser/server ownedprocesses closed finally after
allruns; no userMCP or userGUIprocess cleanup.

QA_STATUS PASS bounded representativeWindows/Linuxruntimecheckpoint. GlobalTask
acceptance requires independentQA/source/license/routing/structural gates owned by
Harness. macOS,Windows11, allFrappe/ReactBitscomponents, API/backend behavior remain
NOT_VALIDATED. No commit/push/merge/publication in this executionlist.

Observed WindowsEdge executable ProductVersion155.0.4283.45.
Observed Linux browser Google Chrome for Testing155.0.8059.12, existingchromium1247 directory.
