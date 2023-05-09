# TRS-Helper-v2.0.0
The ‘TRS Helper’ is a Python tool designed to generate reports from SYSTRAN’s TRS Store using a public REST API.

Supports the following reports:
* Raw JSON – retrieves the entire contents of TRS, no filter, into a JSON file
* All – Displays all ‘master’, ‘runnable’, ‘validated’, ‘stable’, ‘Generic’, ‘SYSTRAN’ available that are stored in TRS
* Best – Given a list of Language Pairs, this report displays the ‘Best’ technology available. Best is defined by the descending priority list:
  * NMT v9.2, NMT v9.0, NMT v8-lua, SPE, SMT, RBMT
* TR ID – Given a list of LPs, display the latest version available across all available technologies, along with the TR ID
* NMT v9 – Given an input list of Language Pairs, displays all NMT v9.0 and v9.2 Translators
  * Diff option – the option exists to provide a previously dump raw TRS JSON file for comparison to show TRs that are added/deleted/upgraded/downgraded/equal
