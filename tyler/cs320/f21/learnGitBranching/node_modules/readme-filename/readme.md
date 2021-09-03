# readme-filename

> Get a project readme file name.

[![travis][travis-image]][travis-url] [![codecov][codecov-image]][codecov-url]

[travis-image]: https://img.shields.io/travis/ngryman/readme-filename.svg?style=flat
[travis-url]: https://travis-ci.org/ngryman/readme-filename
[codecov-image]: https://img.shields.io/codecov/c/github/ngryman/readme-filename.svg
[codecov-url]: https://codecov.io/github/ngryman/readme-filename


## Install

```bash
npm install --save readme-filename
```

## Usage

```javascript
const readmeFilename = require('readme-filename')

readmeFilename().then(console.log)
// => readme.md

readmeFilename('some/path').then(console.log)
// => README.markdown
```

## License

MIT © [Nicolas Gryman](http://ngryman.sh)
