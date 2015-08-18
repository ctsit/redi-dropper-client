# Change Log

## [0.0.2] - 2015-08-18

### Fixed
* Fix issue with settings.conf not linked when doing `vagrant up` + improve docs/README.md (Andrei Sura)
* Fix issue #104 and add tests for it (Ruchi Vivek Desai)
* Fix issue #44 - parallax the login page (Ruchi Vivek Desai)
* Fix issue #75 - cURL max time (configurable in settings.conf with `REDCAP_CURL_API_MAX_TIME` (Andrei Sura)
* Fix issue #73 - show user email instead of id in logs  (Andrei Sura)

### Removed
* Remove duplicate vagrant to avoid confusion (Andrei Sura)

### Changed
* Make "upload box" larger - related to issue #34 (Andrei Sura)
* Change sed call to work with BSD and GNU versions (Taeber Rapczak)

### Added
* Added bootstrap parallax design to `prototype` dir for later integration (Kevin Steven Hanson)


## [0.0.1c] - 2015-07-23

### Fixed
* Fix bugs in deployment script (Andrei Sura)


## [0.0.1b] - 2015-07-21

### Fixed
* Display APP_VERSION in the footer (fixes issue #74 ) (Andrei Sura)
* Fix deploy/fabfile.py to properly reference the 'current' requirements (Andrei Sura)
* Check if the tag number is valid during deployment (Andrei Sura)


## [0.0.1a] - 2015-07-21

### Added
* Add '-t tag_number' to app/README.rst (Andrei Sura)
* Add the missing CHANGELOG.md (Andrei Sura)

### Fixed
* Fix for issue #86 - specify tag number for deployment $ ./deploy.sh -i -t 0.0.1 (Andrei Sura)
* Fix remove conversion to int for `redcap_id` (Andrei Sura)


## [0.0.1] - 2015-07-18

### Added
* Save code with working deployment script


## [0.0.0] - 2015-03-13
### Added
* Initial commit with a one line README.md
