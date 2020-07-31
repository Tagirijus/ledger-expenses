# Changelog

The changelog format follows these rules: [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) and sticks to [semantic versioning](http://semver.org/spec/v2.0.0.html).

## [0.0.6] - 2018-11-07
### Fix
- Sometimes I hate git.

## [0.0.5] - 2018-11-07
### Added
- `-nt` as parameter for no total calculation in the output.

## [0.0.4] - 2018-06-10
### Added
- Time journals can now also be analysed.
- If 'Total' is given as an account name, its account will be used for total.

### Changed
- Only show income or expense, if there are accounts.
- Put many methods in differnet modules for a better structure.
- Time-Output beautified.

## [0.0.3] - 2018-06-08
### Added
- It is now possible to add additional accounts with amount, which are not in the ledger journal.
- It is also now possible to define an individual `from date` and `to date`.

### Changed
- Dates are now calculated by month only. The day was "to precise" and brought me not taht good results.

## [0.0.2] - 2018-06-06
### Changed
- Output if it's yearly or monthly.
- Income accounts now need two arguments: one for the account, one for the name.
- Removed the `--full-text` argument.

## [0.0.1] - 2018-06-06
### Added
- Main functions for the programm.
