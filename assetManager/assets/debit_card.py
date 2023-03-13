from plaid.model.transactions_refresh_request import TransactionsRefreshRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.products import Products
from datetime import date
from assetManager.models import AccountType, AccountTypeEnum
from plaid.exceptions import ApiException
from assetManager.API_wrappers.plaid_wrapper import AccessTokenInvalid
from assetManager.transactionInsight.bank_graph_data import BankGraphData
from django.core.exceptions import ObjectDoesNotExist
from datetime import date

class InvalidInstitution(Exception):
    def __init__(self):
        self.message = 'Provided Instituion Name is not Linked'

#only supports 20 currencies most common
def get_currency_symbol(iso_code):
    symbols = {
        'USD': '$',
        'EUR': '€',
        'JPY': '¥',
        'GBP': '£',
        'CHF': 'Fr',
        'CAD': '$',
        'AUD': '$',
        'NZD': '$',
        'CNY': '¥',
        'HKD': '$',
        'SGD': '$',
        'MXN': '$',
        'INR': '₹',
        'RUB': '₽',
        'ZAR': 'R',
        'BRL': 'R$',
        'TRY': '₺',
        'AED': 'د.إ',
        'SAR': '﷼',
    }
    return symbols.get(iso_code, '')


"""
DebitCard class to represent a Bank Card asset with relevant methods to access transactions and account specific data
"""
def format_accounts_data(request_accounts):
    accounts = {}
    for account in request_accounts:
        if (account['balances']['available'] is None):
            case = {'name':account['name'],'available_amount':0.0, 'current_amount':account['balances']['current'],'type':str(account['type']),'currency':account['balances']['iso_currency_code']}
        else:
            case = {'name':account['name'],'available_amount':account['balances']['available'], 'current_amount':account['balances']['current'],'type':str(account['type']),'currency':account['balances']['iso_currency_code']}

        accounts[account['account_id']] = case


    return accounts

class DebitCard():
    def __init__(self,concrete_wrapper,user):
        self.plaid_wrapper = concrete_wrapper
        self.user = user
        self.access_tokens = self.plaid_wrapper.retrieve_access_tokens(self.user,'transactions')
        self.bank_graph_data = {}

    #Method to refresh the plaid api for any new transactions, must be made before querying transactions directly
    def refresh_api(self,token):
        refresh_request = TransactionsRefreshRequest(access_token=token)
        try:
            refresh_response = self.plaid_wrapper.client.transactions_refresh(refresh_request)
        except ApiException:
            raise AccessTokenInvalid


    def get_institution_name_from_db(self,token):
        try:
            institution_name = AccountType.objects.get(user = self.user, access_token = token, account_asset_type = AccountTypeEnum.DEBIT).account_institution_name
        except ObjectDoesNotExist:
            return None

        return institution_name

    #returns a dictionary containing account balances for all DEBIT account types stored in the database for a specific user, including if a user has multiple existing transactions access_tokens
    #outermost keys are the institution_name, then all accounts under that instituion by id, the all the relevant info
    def get_account_balances(self):
        balances = {}
        for token in self.access_tokens:
            request_accounts = self.plaid_wrapper.get_accounts(token)

            accounts = format_accounts_data(request_accounts)

            balances[self.plaid_wrapper.get_institution_name(token)] = accounts


        return balances


    def get_transactions_by_date(self,start_date_input,end_date_input):
        transactions = []
        for token in self.access_tokens:
            self.refresh_api(token)

            transaction_request = TransactionsGetRequest(
                access_token=token,
                start_date=start_date_input,
                end_date=end_date_input,
            )

            transaction_response = self.plaid_wrapper.client.transactions_get(transaction_request)
            transactions.append(transaction_response['transactions'])

        return transactions

    def make_bank_graph_data_dict(self,token,transactions,transaction_count):
        self.bank_graph_data[self.get_institution_name_from_db(token)] = BankGraphData(transactions[transaction_count])


    def make_graph_transaction_data_insight(self,start_date_input,end_date_input):
        transaction_count = 0
        transactions = self.get_transactions_by_date(start_date_input,end_date_input)
        for token in self.access_tokens:
            self.make_bank_graph_data_dict(token,transactions,transaction_count)
            transaction_count = transaction_count + 1

    def get_insight_data(self):
        if(not self.bank_graph_data):
            return None
        else:
            return self.bank_graph_data

    #write further tests for validaiton of elements returned by the function
    #convert authorised date back to a date as it will be a string when merging with line-graphs branch
    def get_recent_transactions(self,institution_name):
        if(not self.bank_graph_data):
            raise TypeError("Bank graph data is empty")

        if institution_name not in self.bank_graph_data.keys():
            raise InvalidInstitution

        recent_transactions = {}
        transactions = self.bank_graph_data[institution_name].transaction_history

        all_transactions = []
        for account in transactions:
            if(account['authorized_date'] == date.today()):
                if(account['merchant_name'] is None):
                    merchant_name = 'Not provided'
                else:
                    merchant_name = account['merchant_name']

                case = {'amount': get_currency_symbol(account['iso_currency_code']) + str(account['amount']), 'date':account['authorized_date'], 'category':account['category'], 'merchant':merchant_name}

                all_transactions.append(case)

        recent_transactions[institution_name] = all_transactions
        return recent_transactions
