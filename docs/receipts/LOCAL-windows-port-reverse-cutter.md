# LOCAL-windows-port revision4 Cutter/Rizin receipt

User explicitly authorized native Windows portable Cutter/Rizin setup. Prior task
scope preserved; contract Human/JSON updated revision4. No remote publication.
SKILL_RECEIPT: previously read complete reverse-engineering-standard, rea-integration,
vendorREA and dev-implementation-standard remain applicable; supplemental CLI scope
only, ownedtarget, no execution, no newREAprovider. Canonical registry extended.

Official Cutter v2.5.0 asset Windows x86_64 zip140530846bytes from
https://github.com/rizinorg/cutter/releases/download/v2.5.0/Cutter-v2.5.0-Windows-x86_64.zip
SHA256 a04154a03a392dbf5886a629938582f7d23a93636fa0611c3e1c34905b197e69
matched official GitHub release API digest before extraction. ZIP member paths checked
stay within task work/tools. Portable dir work/tools/Cutter-v2.5.0-Windows-x86_64.
No global PATH/install, no account/license purchase, no agentMCP changes.

OBSERVED cutter.exe --version exit0 `cutter 2.5.0-HEAD-a6f6ad7`; rizin.exe -v exit0
`rizin 0.9.1 @ windows-x86-64`, commitc3a90e9226d977f58f4e9c75f78fa6b07afe13c7.
Rizin supplied inside official Cutter archive, no standalone secondpackage.
Cutter GUI not opened, versionCLI only. Logs outputs/cutter-windows-version.txt,
rizin-windows-version.txt.

Owned PE fixture unchanged SHA2566d3eea26039d6f7451a1af38995e334a664996330c8d36fb34316ae594014a3d.
Static command rizin.exe -A -q -c "e scr.color=0;s 0x140001000;pd 2" <fixture> exit0,
observed mov eax,0x2a;ret. Target NEVER executed or debuggerattached.
Bundled rz-ghidra pdg initially lacked Sleigh config; explicitly setting
`e ghidra.sleighhome=<portable>/lib/rizin/plugins/rz_ghidra_sleigh;s 0x140001000;pdg`
returned `return 0x2a` exit0. Initial unsupportedpdd command replaced with correctpdg.
Final logs outputs/rizin-windows-owned-analysis.txt and rizin-windows-owned-decompile.txt.
No claimCutterisREAprovider, fullGUIverified or alltargetformatscovered.

Existing tool-state detect via process-scoped portablePATH records Rizin0.9.1 as
installed and absoluteexe/provenance/method. Cutterhyphenatedversion initially rejected
sharedhelperregex; parentWindowsagent corrected semver handling with regression.
Final Cutter detect and two consecutive resolves PASS with version2.5.0-HEAD-a6f6ad7;
Rizin detect and two resolves PASS version0.9.1. No repeatedinstall/confirmation.
Log outputs/cutter-rizin-state-validation.txt.
Cachedresolve intentionally compares PATH-discoveredexe identity; documented local
fallback reuses knownportablebin processPATH, not globalPATH or per-requestreinstall.
Specialist ignoredruntime-state/tool-state.json holds machine-specificstate.

Primary IDAFree source https://hex-rays.com/ida-free states non-commercialuse only,
noIDAPython/C++SDK, clouddecompiler. NoIDAinstall/account/activation attempted.
Hopper https://www.hopperapp.com/download.html offers Mac/Linuxdemo, noWindowsbuild;
noHopperinstall. Open alternativeCuttersGPL3/RizinLGPL3 metadata checked officialrepos;
upstream license texts retained portablefolder, not bundledplugin redistribution.
IndependentQA pending. Plugin source changes registry+runtimeREADME only, taskrev4 and
this receipt. Currenttokenusage NOT_AVAILABLE; no merge/deploy/publish.

Final installed-validation clarification: forcing QT_QPA_PLATFORM=offscreen/minimal
causes Windows Cutter version CLI to hang in this package. Native Windows default
(no forced QT platform) verifies immediately in both portable and workspace cwd.
Do not inject a generic offscreen Qt override for Cutter --version. Parent repeated
installed detect/resolve successfully with native environment, output
cutter-rizin-installed-state-validation.txt. No product fix or weakened cache needed;
owned timed-out probe processes cleaned by parent. GUI behavior remains unvalidated.
