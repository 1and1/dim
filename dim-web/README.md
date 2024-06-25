# dimfe

> DIM Frontend

## Build Setup

You need to edit [prod.env.js](config/prod.env.js) or [dev.env.js](config/dev.env.js) depends on your need 

Example:
```bash
  DIM_LOGIN: '"https://dim.example.com/dim/login"',
  DIM_RPC: '"https://dim.example.com/dim/jsonrpc"',
  LOGIN: '"https://dim.example.com/cas"',
  LOGOUT: '"https://dim.example.com/cas/logout"',
  BASE_URL: '"/"',
```
Then start npm install and build
``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run all tests
npm test
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

## Docker build
docker build --progress=plain \
    --build-arg DIM_LOGIN=http://dim-nginx:8000/login \
    --build-arg DIM_RPC=http://dim-nginx:8000/jsonrpc \
    --build-arg LOGIN=http://dim-nginx:8000/dim-cas/ \
    --build-arg LOGOUT=http://dim-nginx:8000/dim-cas/logout \
    --build-arg BASE_URL=/web \
    .
