# Changelog

## [0.6.3](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.6.2...v0.6.3) (2025-09-08)


### Bug Fixes

* **javascript:** update content in the correct element ([7b45a81](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/7b45a81b64d8e5e33230fb10de53151e1cfb02c7)), closes [#83](https://github.com/acdh-oeaw/apis-highlighter-ng/issues/83)
* **templates:** drop useless close button in confirm-delete template ([bc14bf8](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/bc14bf879790b668991e7a357393a94727d56daf))
* **templates:** replace hardcoded static uris with static templatetag ([a498e08](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/a498e089819fb91580055cef986bb2337d59afea))

## [0.6.2](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.6.1...v0.6.2) (2025-08-18)


### Bug Fixes

* **templates:** pass reverse paramter to form view ([7cabd18](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/7cabd1844539a98afd1b99812c9c240d7d52e9f9))

## [0.6.1](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.6.0...v0.6.1) (2025-04-16)


### Miscellaneous Chores

* release 0.6.1 ([4903eaa](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/4903eaa3acb80ad0798f7bf63af5322d4e71f74e))

## [0.6.0](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.5.1...v0.6.0) (2025-04-16)


### Features

* adapt the code to work with apis-core-rdf&gt;=0.40.0 ([8f678ac](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/8f678acc6a34412b2a7939ef9d08d8fb55bd4da1))
* **urls:** drop separate `annotations` route ([9d1b9d7](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/9d1b9d78e93745603ffed7c16d4c2bd5ebb9a268))

## [0.5.1](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.5.0...v0.5.1) (2024-12-05)


### Bug Fixes

* **view:** pass request to `highlight_text` ([7c0834d](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/7c0834d8b5e8b4a8f1e016a8f1ae22de1627bc71))

## [0.5.0](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.4.2...v0.5.0) (2024-10-16)


### Features

* **js:** allow to filter the relations in the popup ([eb0cd83](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/eb0cd8308fb2b24282dde6a7d3cb5d7b301b8efe))
* **templates, js:** use the new view for creating annotations ([5b2bc5e](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/5b2bc5e01f666e8df2a2177bc5053daf0b3c2500))
* **views:** add an annotation view based on the new APIS relations ([ca856d1](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/ca856d122d3f8a0cc8540d7dc18ef00004bc3dbd))

## [0.4.2](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.4.1...v0.4.2) (2024-10-07)


### Bug Fixes

* **dependencies:** loosen Django version ([ee4b3eb](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/ee4b3eb61ea35101a0927d9828c7fcd825961ab5))

## [0.4.1](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.4.0...v0.4.1) (2024-10-05)


### Bug Fixes

* **templatetags:** use Djangos html.escape filter to escape strings ([280ceeb](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/280ceeb4f3edbea7cea3948662f5484297ef58c5)), closes [#56](https://github.com/acdh-oeaw/apis-highlighter-ng/issues/56)

## [0.4.0](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.3.2...v0.4.0) (2024-06-19)


### Features

* **js:** store position of the popup in a cookie and reuse the values ([ff52e41](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/ff52e41f19baefd4f000dbcaa8b561bb4f571291)), closes [#40](https://github.com/acdh-oeaw/apis-highlighter-ng/issues/40)
* store the selected annotation project in the session ([8a6e894](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/8a6e8947fffb9a357ec41a1c92710c9b4a6890a2)), closes [#49](https://github.com/acdh-oeaw/apis-highlighter-ng/issues/49)

## [0.3.2](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.3.1...v0.3.2) (2024-06-19)


### Bug Fixes

* **templates:** make the selection menu reflect the selected value ([dc6edb5](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/dc6edb593e48a107221a6adba408054e9dd67d0a))

## [0.3.1](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.3.0...v0.3.1) (2024-04-11)


### Bug Fixes

* update pre_save signal to work with field names ([58cc1b4](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/58cc1b4793657a9754b46244510957052eddd1b5)), closes [#46](https://github.com/acdh-oeaw/apis-highlighter-ng/issues/46)

## [0.3.0](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.2.1...v0.3.0) (2024-04-11)


### Features

* store the name of the field in the annotation ([e801219](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/e80121979372d41ddab0343dc07c6978c1a161bf)), closes [#43](https://github.com/acdh-oeaw/apis-highlighter-ng/issues/43)

## [0.2.1](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.2.0...v0.2.1) (2024-03-15)


### Bug Fixes

* hide delete skeleton menu ([668cc68](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/668cc6819c208d4777107245a0cfad64ac259dbe))

## [0.2.0](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.1.4...v0.2.0) (2024-03-11)


### Features

* create human readable annotation string representation ([0900bd7](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/0900bd75dd6f95a391b8d43277a2cbb8a5299ce0))

## [0.1.4](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.1.3...v0.1.4) (2024-02-09)


### Bug Fixes

* make signal more robust ([5bee60f](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/5bee60f6cfbb9ff7398e83dba2ed05c63761f8a0))

## [0.1.3](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.1.2...v0.1.3) (2024-02-09)


### Bug Fixes

* add basic readme ([e10e896](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/e10e896883dc14224018faf38e3b684759b848b6))

## [0.1.2](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.1.1...v0.1.2) (2024-02-09)


### Bug Fixes

* add license file ([481f135](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/481f135b8856b431f291ff569a83fb92c365b929))

## [0.1.1](https://github.com/acdh-oeaw/apis-highlighter-ng/compare/v0.1.0...v0.1.1) (2024-02-09)


### Bug Fixes

* add empty README file ([d6a67bf](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/d6a67bfeece97f980c59c9fa21e00640bec39e65))

## 0.1.0 (2024-02-09)


### Features

* add css to highlighter marks ([21403eb](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/21403ebeac58959c1001ae172adb984bf8aa4d7a))
* add views and routes ([1e48dc0](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/1e48dc0692464e3411784f3bdded0b7222b7e692))
* implement deletion of annotations ([3c3810c](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/3c3810cc5bbcd642ef1cf32b97b8fa7c1bba3487))
* implement highlighting with javascript ([8f4eea2](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/8f4eea2d7c7ca7204890e1135eefa54759c7f1ae))
* implement project selector ([a589a31](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/a589a312559bd04dac483c3e1933f274ce622bf0))
* include needed css ([9c62df4](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/9c62df48fc8debb20055c61eee701c90349de747))
* show name of annotationproject as default repr ([d82e68c](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/d82e68cf5f434acab9b82568c983248f057da82e))


### Bug Fixes

* bug in js ([c995fc4](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/c995fc4709ded0c5e504be8b3cc4cf22d04ff00f))
* cleanup javascript ([ab47403](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/ab474031610e37f9811a5a985e65002a82d27d00))
* delete view ([4e10c7c](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/4e10c7cdd1b22cfc86d3091b073e8b09fa495187))
* fallback to first annotation project if no default exists ([2c22d2c](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/2c22d2c4e74b6c6e8bcee98c0d251bec6099d63d))
* overlapping ranges in templatetag ([4826c30](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/4826c30693981c6cc6935b99e3d651bb519e40a0))
* replace view logic with templatetag ([5ab0ee2](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/5ab0ee286570ff54bc92f6481d090a2446f833ff))
* save orig_string in annotation data ([88c42e9](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/88c42e9ab20b0d7f046f29cc0db8f3753687eb30)), closes [#5](https://github.com/acdh-oeaw/apis-highlighter-ng/issues/5)
* save user in annotation ([28a009b](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/28a009b4460f6b4679940a59895ba4c8abdb864a)), closes [#3](https://github.com/acdh-oeaw/apis-highlighter-ng/issues/3)
* update annotations ([6137025](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/61370252e036583f245b0d201790931173c81a83)), closes [#20](https://github.com/acdh-oeaw/apis-highlighter-ng/issues/20) [#24](https://github.com/acdh-oeaw/apis-highlighter-ng/issues/24)
* use tuples instead of ranges to compare overlap ([47423bf](https://github.com/acdh-oeaw/apis-highlighter-ng/commit/47423bf4f9b5442515ac6659c4916e4e69991e22))
