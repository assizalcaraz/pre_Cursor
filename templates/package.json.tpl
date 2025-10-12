{
  "name": "{{MODULO_PRINCIPAL}}",
  "version": "1.0.0",
  "description": "{{DESCRIPCION_PROYECTO}}",
  "main": "src/{{MODULO_PRINCIPAL}}.js",
  "scripts": {
    "start": "node src/{{MODULO_PRINCIPAL}}.js",
    "dev": "nodemon src/{{MODULO_PRINCIPAL}}.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint src/ tests/",
    "lint:fix": "eslint src/ tests/ --fix",
    "format": "prettier --write src/ tests/",
    "build": "npm run lint && npm test"
  },
  "keywords": [
    "{{PALABRAS_CLAVE}}"
  ],
  "author": "{{AUTOR}}",
  "license": "{{LICENCIA}}",
  "repository": {
    "type": "git",
    "url": "{{REPOSITORIO_URL}}"
  },
  "bugs": {
    "url": "{{REPOSITORIO_URL}}/issues"
  },
  "homepage": "{{REPOSITORIO_URL}}#readme",
  "engines": {
    "node": ">={{NODE_VERSION}}"
  },
  "dependencies": {
    {{DEPENDENCIAS_PRINCIPALES}}
  },
  "devDependencies": {
    {{DEPENDENCIAS_DESARROLLO}}
  },
  "jest": {
    "testEnvironment": "node",
    "collectCoverageFrom": [
      "src/**/*.js",
      "!src/**/*.test.js"
    ],
    "coverageDirectory": "coverage",
    "coverageReporters": [
      "text",
      "lcov",
      "html"
    ]
  }
}
