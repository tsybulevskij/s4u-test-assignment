# Task overview

Build a basic system that keeps track of a set of accounts and allows external systems to execute transactions that change the accounts balances.

# Domain model
### Accounts
Accounts are identified by 8-digit numbers which are assigned by the system.

Accounts can be denominated in one of the following currencies: USD, EUR, GBP, CHF and the system stores the current balance of each account.

### Transactions
Account balance can be changed by external and internal transfers. External transfers change the balance of a single account, internal transfers operate on a pair of accounts.

Transactions with only a destination account are called deposits, transactions with only a source account are called withdrawals.

Internal transfers convert the transferred amount if the source and destination accounts are denominated in different currencies.

Transactions that would result in negative balance on any account are not permitted.

# Major system components
The system will consist of an API server that implements all necessary operations and a UI that allows to view account status and operation history for a specific account.

# Component specifications
### UI
The system will provide the following views:
 - List of accounts with balances and links to individual accounts.
 - Detail view for an individual account showing the transaction history of that account.

The UI specification is intentionally low-detail and you should implement what you consider a sensible UI for the given tasks.

# API
API server calls should be authorized by passing a shared key in a request header. All API output should be JSON.

All objects need to be stored in some form of persistent storage, preferably a relational database.

Exchange rates for any currency conversions should be acquired from  http://fixer.io/ You can implement the endpoints necessary for the UI however you need.

The account and transaction creation endpoints are considered an external interface, their output should have the following general shape:

```
{
  error: true|false,  // indicates if there was an error during processing of the request
  // if error is true
  code: "MACHINE_FRIENDLY_STATUS",
  message: "Human readable description of the error",
  
  // if error is false
  data: ...  // The output, in whatever shape is appropriate
}
```

The account creation endpoint specification:
Method: POST
Path: /accounts
Input params (passed as form params):
 - currency - the currency which the account is denominated in

Output on success:
```
{
  error: false,
  data: {accountNumber: "12345678"  // String containing 8-digit number}
}
```

The transaction creation endpoint specification:
Method: POST
Path: /transactions
Input params (passed as form params):
  - sourceAccount - number of the account to transfer from. Set to null for deposits.
  - destAccount - number of the account to transfer to. Set to null for withdrawals.
  - amount - The amount to transfer. For transfers between accounts denominated in
different currencies, this amount is in the source account currency.

Output on success:
```
{
  error: false,
  data: {transactionId: 938492895  // Unique numeric id for the created transaction}
}
```

Fork your own copy of eglobal-it/s4u-test-assignment to your account and share the result with us.
