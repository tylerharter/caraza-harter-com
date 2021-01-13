'use strict'

const fs = require('fs')

// eslint-disable-next-line
const PATTERN = /^readme\.(?:markdown|mdown|mkdn|md|textile|rdoc|org|creole|mediawiki|wiki|rst|asciidoc|adoc|asc|pod|txt)/i

module.exports = function readmeFilename(dir) {
  return new Promise((resolve, reject) => {
    dir = dir || '.'

    fs.readdir(dir, (err, files) => {
      if (err) return reject(err)

      const filename = files.find(file => PATTERN.test(file)) || null
      resolve(filename)
    })
  })
}
