module.exports = {
  backend: {
    output: {
      mode: 'tags-split',
      target: './src/',
      schemas: './src/api/models',
      client: 'react-query',
    },
    input: '/schemas/backend_openapi_schema.json',
  }
}