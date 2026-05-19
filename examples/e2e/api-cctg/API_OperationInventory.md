# API Operation Inventory

## POST /accounts/list

- **Method**: POST
- **Endpoint**: /accounts/list
- **Source**: BIDV sample API specification page 6
- **Required headers**: AuthToken, requestID, Accept-Language, X-App-Code, Content-Type=application/json
- **Required body fields**: requestCif
- **Response schema**: accountNumber, currentBalance, currency, minBal, acctBranchcode

## POST /v1/buy/order

- **Method**: POST
- **Endpoint**: /v1/buy/order
- **Source**: BIDV sample API specification page 9
- **Required headers**: AuthToken, requestID, Accept-Language, X-App-Code, Content-Type=application/json
- **Required body fields**: requestId, requestCif, orderAmount, expectedSalesDate, receivingAccount
- **Business errors**: 115=ACC_DETAIL_INVALID_CIF, 117=IMPLICT_BALANCE
