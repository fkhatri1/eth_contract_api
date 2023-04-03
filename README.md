# eth_contract_api

Uses Alchemy to invoke `eth_call`.
From there it's just encoding/decoding the functions and args.

Limitations:
1. Only implemented uint, bool and address argument types.  Just to limit scope and complexity for this exercise.
2. Have not tested this super thoroughly, I'm sure there are a lot of bugs.  But it works.

## This API is live!
Invoke it in the [browser](http://34.210.199.235:3001/contract/0xdAC17F958D2ee523a2206206994597C13D831ec7?func=balanceOf(address)&arguments=[%220x39bE25dDf6F7F5955bBDb8CC65Ca999746FD1a6A%22]&return_type=int) or using curl.


`
curl  -g \
      --request GET \
      --url "http://34.210.199.235:3001/contract/0xdAC17F958D2ee523a2206206994597C13D831ec7?func=balanceOf(address)&arguments=[%220x39bE25dDf6F7F5955bBDb8CC65Ca999746FD1a6A%22]&return_type=int"
`

