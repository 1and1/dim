sed -i "s@DIM_LOGIN_PLACE_HOLDER@$DIM_LOGIN@g" config/prod.env.js
sed -i "s@DIM_RPC_PLACE_HOLDER@$DIM_RPC@g" config/prod.env.js
sed -i "s@LOGIN_PLACE_HOLDER@$LOGIN@g" config/prod.env.js
sed -i "s@LOGOUT_PLACE_HOLDER@$LOGOUT@g" config/prod.env.js
sed -i "s@BASE_URL_PLACE_HOLDER@$BASE_URL@g" config/prod.env.js
