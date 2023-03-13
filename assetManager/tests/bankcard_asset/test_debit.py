from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.assets.debit_card import DebitCard, format_accounts_data,InvalidInstitution
from django.test import TestCase
from assetManager.models import User, AccountType, AccountTypeEnum
from datetime import date
from assetManager.API_wrappers.plaid_wrapper import AccessTokenInvalid,PublicTokenNotExchanged
from unittest import skip
from django.core.exceptions import ObjectDoesNotExist
from assetManager.transactionInsight.bank_graph_data import BankGraphData
import json
import os
from assetManager.API_wrappers.plaid_wrapper import PublicTokenNotExchanged
from dateutil.tz import tzlocal
import datetime
from datetime import date

#change locations of long jsons
class DebitCardSandBoxWrapperTestCase(TestCase):
    fixtures = ['assetManager/tests/fixtures/users.json']
    #recursively checks that two dictionaries have the same structure and have the same value

    def are_dicts_same(self,dict1, dict2):
        if isinstance(dict1, dict) and isinstance(dict2, dict):
            if len(dict1) != len(dict2):
                return False
            for key in dict1:
                if key not in dict2 or not self.are_dicts_same(dict1[key], dict2[key]):
                    return False
            return True
        else:
            return dict1 == dict2


    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.org')
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token_custom_user()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(self.user, ['transactions'])
        self.debit_card = DebitCard(plaid_wrapper, self.user)

        self.recent_transactions = [[{'account_id': 'JrJZmPgzGACD3naN3DP5sP9W4d8mdxCQegPGk',
         'account_owner': None,
         'amount': 896.65,
         'authorized_date': date.today(),
         'authorized_datetime': None,
         'category': ['Transfer', 'Debit'],
         'category_id': '21006000',
         'check_number': None,
         'date': datetime.date(2022, 12, 17),
         'datetime': None,
         'iso_currency_code': 'USD',
         'location': {'address': None,
            'city': None,
            'country': None,
            'lat': None,
            'lon': None,
            'postal_code': None,
            'region': None,
            'store_number': None},
         'merchant_name': 'Bank Of Switzerland',
         'name': 'DEBIT CRD AUTOPAY 98712 000000000028791 KIUYPWRSGTKF UXYOTLLKJHA C',
         'payment_channel': 'in store',
         'payment_meta': {'by_order_of': None,
                'payee': None,
                'payer': None,
                'payment_method': None,
                'payment_processor': None,
                'ppd_id': None,
                'reason': None,
                'reference_number': None},
         'pending': False,
         'pending_transaction_id': None,
         'personal_finance_category': None,
         'transaction_code': None,
         'transaction_id': 'PaJgwMn4y9fbPzjdPbl5hg9zN8kg1pSXyWRn6',
         'transaction_type': 'special',
         'unofficial_currency_code': None}, {'account_id': 'PaJgwMn4y9fbPzjdPbl5hg9qkab8awCXyWRnv',
         'account_owner': None,
         'amount': 398.34,
         'authorized_date': date.today(),
         'authorized_datetime': None,
         'category': ['Food and Drink', 'Restaurants', 'Fast Food'],
         'category_id': '21006000',
         'check_number': None,
         'date': datetime.date(2022, 12, 17),
         'datetime': None,
         'iso_currency_code': 'GBP',
         'location': {'address': None,
            'city': None,
            'country': None,
            'lat': None,
            'lon': None,
            'postal_code': None,
            'region': None,
            'store_number': None},
         'merchant_name': 'Eat Tokyo',
         'name': 'DEBIT CRD AUTOPAY 98712 000000000098712 WRSGTKIUYPKF KJHAUXYOTLL A',
         'payment_channel': 'in store',
         'payment_meta': {'by_order_of': None,
                'payee': None,
                'payer': None,
                'payment_method': None,
                'payment_processor': None,
                'ppd_id': None,
                'reason': None,
                'reference_number': None},
         'pending': False,
         'pending_transaction_id': None,
         'personal_finance_category': None,
         'transaction_code': None,
         'transaction_id': '4e1XPQq43Bs5L4m6L5pEFGgjMA5GQvUlRAPKp',
         'transaction_type': 'special',
         'unofficial_currency_code': None}, {'account_id': 'JrJZmPgzGACD3naN3DP5sP9W4d8mdxCQegPGk',
         'account_owner': None,
         'amount': 1708.12,
         'authorized_date':date.today(),
         'authorized_datetime': None,
         'category': ['Food and Drink', 'Restaurants'],
         'category_id': '13005000',
         'check_number': None,
         'date': datetime.date(2022, 12, 16),
         'datetime': None,
         'iso_currency_code': 'INR',
         'location': {'address': None,
            'city': None,
            'country': None,
            'lat': None,
            'lon': None,
            'postal_code': None,
            'region': None,
            'store_number': None},
         'merchant_name': 'Burger and Lobster',
         'name': 'CREDIT CRD AUTOPAY 29812 000000000098123 CRGKFKKSPABG UXZYOTAYLDA D',
         'payment_channel': 'in store',
         'payment_meta': {'by_order_of': None,
                'payee': None,
                'payer': None,
                'payment_method': None,
                'payment_processor': None,
                'ppd_id': None,
                'reason': None,
                'reference_number': None},
         'pending': False,
         'pending_transaction_id': None,
         'personal_finance_category': None,
         'transaction_code': None,
         'transaction_id': 'NxJp9Qkdemcw4X7L4wW5cwqryvjwepTXA5wzp',
         'transaction_type': 'place',
         'unofficial_currency_code': None}, {'account_id': 'PaJgwMn4y9fbPzjdPbl5hg9qkab8awCXyWRnv',
         'account_owner': None,
         'amount': 1109.01,
         'authorized_date': date.today(),
         'authorized_datetime': None,
         'category': ['Transfer', 'Debit'],
         'category_id': '21006000',
         'check_number': None,
         'date': datetime.date(2022, 12, 16),
         'datetime': None,
         'iso_currency_code': 'NOK',
         'location': {'address': None,
            'city': None,
            'country': None,
            'lat': None,
            'lon': None,
            'postal_code': None,
            'region': None,
            'store_number': None},
         'merchant_name': None,
         'name': 'CREDIT CRD AUTOPAY 29812 000000000098123 KABCRGKSPKFG YOTALDUXZYA B',
         'payment_channel': 'in store',
         'payment_meta': {'by_order_of': None,
                'payee': None,
                'payer': None,
                'payment_method': None,
                'payment_processor': None,
                'ppd_id': None,
                'reason': None,
                'reference_number': None},
         'pending': False,
         'pending_transaction_id': None,
         'personal_finance_category': None,
         'transaction_code': None,
         'transaction_id': 'aWQwlaxAE4tKn1bEnKAvimBLNpMm7DtkKQMvK',
         'transaction_type': 'special',
         'unofficial_currency_code': None}, {'account_id': 'PaJgwMn4y9fbPzjdPbl5hg9qkab8awCXyWRkl',
         'account_owner': None,
         'amount': 200,
         'authorized_date': datetime.date(2022, 12, 16),
         'authorized_datetime': None,
         'category': ['Transfer', 'Debit'],
         'category_id': '21006000',
         'check_number': None,
         'date': datetime.date(2022, 12, 16),
         'datetime': None,
         'iso_currency_code': 'NOK',
         'location': {'address': None,
            'city': None,
            'country': None,
            'lat': None,
            'lon': None,
            'postal_code': None,
            'region': None,
            'store_number': None},
         'merchant_name': None,
         'name': 'CREDIT CRD AUTOPAY 29812 000000000098123 KABCRGKSPKFG YOTALDUXZYA B',
         'payment_channel': 'in store',
         'payment_meta': {'by_order_of': None,
                'payee': None,
                'payer': None,
                'payment_method': None,
                'payment_processor': None,
                'ppd_id': None,
                'reason': None,
                'reference_number': None},
         'pending': False,
         'pending_transaction_id': None,
         'personal_finance_category': None,
         'transaction_code': None,
         'transaction_id': 'aWQwlaxAE4tKn1bEnKAvimBLNpMm7DtkKQMkl',
         'transaction_type': 'special',
         'unofficial_currency_code': None}]]

        self.single_transaction_history = [[{'account_id': 'kK3EeGbokrHnb1GWao1wc5rbep6npEIJQLxLa',
 'account_owner': None,
 'amount': 500.0,
 'authorized_date': None,
 'authorized_datetime': None,
 'category': ['Travel', 'Airlines and Aviation Services'],
 'category_id': '22001000',
 'check_number': None,
 'date': datetime.date(2022, 12, 16),
 'datetime': None,
 'iso_currency_code': 'GBP',
 'location': {'address': None,
              'city': None,
              'country': None,
              'lat': None,
              'lon': None,
              'postal_code': None,
              'region': None,
              'store_number': None},
 'merchant_name': 'United Airlines',
 'name': 'United Airlines',
 'payment_channel': 'in store',
 'payment_meta': {'by_order_of': None,
                  'payee': None,
                  'payer': None,
                  'payment_method': None,
                  'payment_processor': None,
                  'ppd_id': None,
                  'reason': None,
                  'reference_number': None},
 'pending': False,
 'pending_transaction_id': None,
 'personal_finance_category': None,
 'transaction_code': None,
 'transaction_id': 'M3vq1AwVoBIGj5kv8X5oFlVw6pmLAziLGk1nk',
 'transaction_type': 'special',
 'unofficial_currency_code': None}]]

        self.multiple_transaction_history = [[{'account_id': 'JrJZmPgzGACD3naN3DP5sP9W4d8mdxCQegPGk',
 'account_owner': None,
 'amount': 896.65,
 'authorized_date': datetime.date(2022, 12, 16),
 'authorized_datetime': None,
 'category': ['Transfer', 'Debit'],
 'category_id': '21006000',
 'check_number': None,
 'date': datetime.date(2022, 12, 17),
 'datetime': None,
 'iso_currency_code': 'USD',
 'location': {'address': None,
              'city': None,
              'country': None,
              'lat': None,
              'lon': None,
              'postal_code': None,
              'region': None,
              'store_number': None},
 'merchant_name': None,
 'name': 'DEBIT CRD AUTOPAY 98712 000000000028791 KIUYPWRSGTKF UXYOTLLKJHA C',
 'payment_channel': 'in store',
 'payment_meta': {'by_order_of': None,
                  'payee': None,
                  'payer': None,
                  'payment_method': None,
                  'payment_processor': None,
                  'ppd_id': None,
                  'reason': None,
                  'reference_number': None},
 'pending': False,
 'pending_transaction_id': None,
 'personal_finance_category': None,
 'transaction_code': None,
 'transaction_id': 'PaJgwMn4y9fbPzjdPbl5hg9zN8kg1pSXyWRn6',
 'transaction_type': 'special',
 'unofficial_currency_code': None}, {'account_id': 'PaJgwMn4y9fbPzjdPbl5hg9qkab8awCXyWRnv',
 'account_owner': None,
 'amount': 398.34,
 'authorized_date': datetime.date(2022, 12, 16),
 'authorized_datetime': None,
 'category': ['Transfer', 'Debit'],
 'category_id': '21006000',
 'check_number': None,
 'date': datetime.date(2022, 12, 17),
 'datetime': None,
 'iso_currency_code': 'USD',
 'location': {'address': None,
              'city': None,
              'country': None,
              'lat': None,
              'lon': None,
              'postal_code': None,
              'region': None,
              'store_number': None},
 'merchant_name': None,
 'name': 'DEBIT CRD AUTOPAY 98712 000000000098712 WRSGTKIUYPKF KJHAUXYOTLL A',
 'payment_channel': 'in store',
 'payment_meta': {'by_order_of': None,
                  'payee': None,
                  'payer': None,
                  'payment_method': None,
                  'payment_processor': None,
                  'ppd_id': None,
                  'reason': None,
                  'reference_number': None},
 'pending': False,
 'pending_transaction_id': None,
 'personal_finance_category': None,
 'transaction_code': None,
 'transaction_id': '4e1XPQq43Bs5L4m6L5pEFGgjMA5GQvUlRAPKp',
 'transaction_type': 'special',
 'unofficial_currency_code': None}, {'account_id': 'JrJZmPgzGACD3naN3DP5sP9W4d8mdxCQegPGk',
 'account_owner': None,
 'amount': 1708.12,
 'authorized_date': datetime.date(2022, 12, 16),
 'authorized_datetime': None,
 'category': ['Food and Drink', 'Restaurants'],
 'category_id': '13005000',
 'check_number': None,
 'date': datetime.date(2022, 12, 16),
 'datetime': None,
 'iso_currency_code': 'USD',
 'location': {'address': None,
              'city': None,
              'country': None,
              'lat': None,
              'lon': None,
              'postal_code': None,
              'region': None,
              'store_number': None},
 'merchant_name': None,
 'name': 'CREDIT CRD AUTOPAY 29812 000000000098123 CRGKFKKSPABG UXZYOTAYLDA D',
 'payment_channel': 'in store',
 'payment_meta': {'by_order_of': None,
                  'payee': None,
                  'payer': None,
                  'payment_method': None,
                  'payment_processor': None,
                  'ppd_id': None,
                  'reason': None,
                  'reference_number': None},
 'pending': False,
 'pending_transaction_id': None,
 'personal_finance_category': None,
 'transaction_code': None,
 'transaction_id': 'NxJp9Qkdemcw4X7L4wW5cwqryvjwepTXA5wzp',
 'transaction_type': 'place',
 'unofficial_currency_code': None}, {'account_id': 'PaJgwMn4y9fbPzjdPbl5hg9qkab8awCXyWRnv',
 'account_owner': None,
 'amount': 1109.01,
 'authorized_date': datetime.date(2022, 12, 16),
 'authorized_datetime': None,
 'category': ['Transfer', 'Debit'],
 'category_id': '21006000',
 'check_number': None,
 'date': datetime.date(2022, 12, 16),
 'datetime': None,
 'iso_currency_code': 'USD',
 'location': {'address': None,
              'city': None,
              'country': None,
              'lat': None,
              'lon': None,
              'postal_code': None,
              'region': None,
              'store_number': None},
 'merchant_name': None,
 'name': 'CREDIT CRD AUTOPAY 29812 000000000098123 KABCRGKSPKFG YOTALDUXZYA B',
 'payment_channel': 'in store',
 'payment_meta': {'by_order_of': None,
                  'payee': None,
                  'payer': None,
                  'payment_method': None,
                  'payment_processor': None,
                  'ppd_id': None,
                  'reason': None,
                  'reference_number': None},
 'pending': False,
 'pending_transaction_id': None,
 'personal_finance_category': None,
 'transaction_code': None,
 'transaction_id': 'aWQwlaxAE4tKn1bEnKAvimBLNpMm7DtkKQMvK',
 'transaction_type': 'special',
 'unofficial_currency_code': None}], [{'account_id': 'bMXdQVkDRXHABLR5bZnycpXjq3qnP9uomZJK3',
 'account_owner': None,
 'amount': 896.65,
 'authorized_date': datetime.date(2022, 12, 16),
 'authorized_datetime': None,
 'category': ['Payment', 'Credit Card'],
 'category_id': '16001000',
 'check_number': None,
 'date': datetime.date(2022, 12, 17),
 'datetime': None,
 'iso_currency_code': 'USD',
 'location': {'address': None,
              'city': None,
              'country': None,
              'lat': None,
              'lon': None,
              'postal_code': None,
              'region': None,
              'store_number': None},
 'merchant_name': None,
 'name': 'DEBIT CRD AUTOPAY 98712 000000000028791 KIUYPWRSGTKF UXYOTLLKJHA C',
 'payment_channel': 'other',
 'payment_meta': {'by_order_of': None,
                  'payee': None,
                  'payer': None,
                  'payment_method': None,
                  'payment_processor': None,
                  'ppd_id': None,
                  'reason': None,
                  'reference_number': None},
 'pending': False,
 'pending_transaction_id': None,
 'personal_finance_category': None,
 'transaction_code': None,
 'transaction_id': 'V3LRGAPZzLfeDz1MxgGRfeLXr7BlbQfqdvgJy',
 'transaction_type': 'special',
 'unofficial_currency_code': None}, {'account_id': 'nrDL1VlR6DI4zMo5AXgdFwlRaJamZ7U3AWXVK',
 'account_owner': None,
 'amount': 398.34,
 'authorized_date': datetime.date(2022, 12, 16),
 'authorized_datetime': None,
 'category': ['Payment', 'Credit Card'],
 'category_id': '16001000',
 'check_number': None,
 'date': datetime.date(2022, 12, 17),
 'datetime': None,
 'iso_currency_code': 'USD',
 'location': {'address': None,
              'city': None,
              'country': None,
              'lat': None,
              'lon': None,
              'postal_code': None,
              'region': None,
              'store_number': None},
 'merchant_name': None,
 'name': 'DEBIT CRD AUTOPAY 98712 000000000098712 WRSGTKIUYPKF KJHAUXYOTLL A',
 'payment_channel': 'other',
 'payment_meta': {'by_order_of': None,
                  'payee': None,
                  'payer': None,
                  'payment_method': None,
                  'payment_processor': None,
                  'ppd_id': None,
                  'reason': None,
                  'reference_number': None},
 'pending': False,
 'pending_transaction_id': None,
 'personal_finance_category': None,
 'transaction_code': None,
 'transaction_id': 'XdGXEn7b3GsZM5zLn8NpCzQ6apBZN8C1ErKRv',
 'transaction_type': 'special',
 'unofficial_currency_code': None}]]

    def test_debit_card_set_up_correctly(self):
        self.assertTrue(self.debit_card.plaid_wrapper.ACCESS_TOKEN is not None)
        self.assertEqual(self.debit_card.plaid_wrapper.SANDBOX_KEY, '3c1540e977fb113fe9bdbb12bf61fd')
        self.assertTrue(self.debit_card.plaid_wrapper.client is not None)
        self.assertEqual(self.debit_card.plaid_wrapper.CLIENT_ID, '63d288b343e6370012e5be86')
        self.assertEqual(self.debit_card.plaid_wrapper.retrieve_access_tokens(self.user,'transactions')[0], self.debit_card.access_tokens[0])
        identity = self.debit_card.plaid_wrapper.get_identity()
        self.assertEqual(identity['names'][0],'John Smith')
        self.assertEqual(self.user.email, self.debit_card.user.email)
        accounts = AccountType.objects.filter(user = self.user)
        self.assertEqual(len(accounts),1)

    def test_get_recent_transactions_with_incorrect_institution_name(self):
        self.debit_card.make_bank_graph_data_dict(self.debit_card.access_tokens[0],self.single_transaction_history,0)
        with self.assertRaises(InvalidInstitution) as cm:
            self.debit_card.get_recent_transactions('HSBC')

        self.assertEqual(str(cm.exception.message),'Provided Instituion Name is not Linked')

    def test_get_recent_transactions_without_graph_data_initialised(self):
        with self.assertRaises(TypeError) as e:
            self.debit_card.get_recent_transactions('Royal Bank of Scotland - Current Accounts')

        #self.assertEqual(str(e.message),'Bank graph data is empty')
    def test_get_recent_transactions_one_institution_linked_without_transactions_today(self):
        self.debit_card.make_bank_graph_data_dict(self.debit_card.access_tokens[0],self.multiple_transaction_history,0)
        recent_transactions = self.debit_card.get_recent_transactions('Royal Bank of Scotland - Current Accounts')
        self.assertEqual(len(recent_transactions['Royal Bank of Scotland - Current Accounts']),0)

    def test_with_whole_flow_of_recent_transactions(self):
        pass


    def test_get_recent_transactions_with_one_institution_linked_and_today_dates(self):
        self.assertEqual(len(self.recent_transactions[0]),5)
        self.debit_card.make_bank_graph_data_dict(self.debit_card.access_tokens[0],self.recent_transactions,0)
        recent_transactions = self.debit_card.get_recent_transactions('Royal Bank of Scotland - Current Accounts')
        self.assertEqual(list(recent_transactions.keys())[0],'Royal Bank of Scotland - Current Accounts')
        self.assertEqual(len(recent_transactions[list(recent_transactions.keys())[0]]),4)

        self.assertEqual(recent_transactions['Royal Bank of Scotland - Current Accounts'][0]['amount'],'$896.65')
        self.assertEqual(recent_transactions['Royal Bank of Scotland - Current Accounts'][1]['amount'],'£398.34')
        self.assertEqual(recent_transactions['Royal Bank of Scotland - Current Accounts'][2]['amount'],'₹1708.12')
        self.assertEqual(recent_transactions['Royal Bank of Scotland - Current Accounts'][3]['amount'],'1109.01')

        self.assertEqual(recent_transactions['Royal Bank of Scotland - Current Accounts'][0]['date'],date.today())
        self.assertEqual(recent_transactions['Royal Bank of Scotland - Current Accounts'][1]['date'],date.today())
        self.assertEqual(recent_transactions['Royal Bank of Scotland - Current Accounts'][2]['date'],date.today())
        self.assertEqual(recent_transactions['Royal Bank of Scotland - Current Accounts'][3]['date'],date.today())

        self.assertEqual(recent_transactions['Royal Bank of Scotland - Current Accounts'][0]['merchant'],'Bank Of Switzerland')
        self.assertEqual(recent_transactions['Royal Bank of Scotland - Current Accounts'][1]['merchant'],'Eat Tokyo')
        self.assertEqual(recent_transactions['Royal Bank of Scotland - Current Accounts'][2]['merchant'],'Burger and Lobster')
        self.assertEqual(recent_transactions['Royal Bank of Scotland - Current Accounts'][3]['merchant'],'Not provided')

        self.assertEqual(recent_transactions['Royal Bank of Scotland - Current Accounts'][0]['category'],['Transfer', 'Debit'])
        self.assertEqual(recent_transactions['Royal Bank of Scotland - Current Accounts'][1]['category'],['Food and Drink', 'Restaurants', 'Fast Food'])
        self.assertEqual(recent_transactions['Royal Bank of Scotland - Current Accounts'][2]['category'],['Food and Drink', 'Restaurants'])
        self.assertEqual(recent_transactions['Royal Bank of Scotland - Current Accounts'][3]['category'],['Transfer', 'Debit'])




    def test_get_correct_indexing_of_transactions_data_with_single_institution(self):
        self.debit_card.make_bank_graph_data_dict(self.debit_card.access_tokens[0],self.single_transaction_history,0)
        insight_data = self.debit_card.get_insight_data()

        self.assertEqual(list(insight_data.keys())[0], 'Royal Bank of Scotland - Current Accounts')
        self.assertEqual(len(insight_data['Royal Bank of Scotland - Current Accounts'].transaction_history),1)
        self.assertEqual(insight_data['Royal Bank of Scotland - Current Accounts'].transaction_history[0]['amount'], 500.0)
        self.assertEqual(insight_data['Royal Bank of Scotland - Current Accounts'].transaction_history[0]['iso_currency_code'], 'GBP')
        self.assertEqual(insight_data['Royal Bank of Scotland - Current Accounts'].transaction_history[0]['name'], 'United Airlines')
        self.assertEqual(insight_data['Royal Bank of Scotland - Current Accounts'].transaction_history[0]['transaction_type'], 'special')

    def test_get_correct_indexing_of_transactions_data_with_multiple_institutions(self):

        AccountType.objects.create(
            user = self.user,
            account_asset_type = AccountTypeEnum.DEBIT,
            access_token = 'access-sandbox-8ab976e6-64bc-4b38-98f7-731e7a349971',
            account_institution_name = 'HSBC',
        )

        sandbox_wrapper = SandboxWrapper()

        new_debit_card = DebitCard(sandbox_wrapper,self.user)
        self.assertEqual(len(new_debit_card.access_tokens),2)

        new_debit_card.make_bank_graph_data_dict(new_debit_card.access_tokens[0],self.multiple_transaction_history,0)
        new_debit_card.make_bank_graph_data_dict(new_debit_card.access_tokens[1],self.multiple_transaction_history,1)

        insight_data = new_debit_card.get_insight_data()

        self.assertEqual(list(insight_data.keys())[0], 'Royal Bank of Scotland - Current Accounts')
        self.assertEqual(list(insight_data.keys())[1], 'HSBC')
        self.assertEqual(len(insight_data['Royal Bank of Scotland - Current Accounts'].transaction_history),4)
        self.assertEqual(len(insight_data['HSBC'].transaction_history),2)


        self.assertEqual(insight_data['Royal Bank of Scotland - Current Accounts'].transaction_history[0]['amount'], 896.65)
        self.assertEqual(insight_data['Royal Bank of Scotland - Current Accounts'].transaction_history[1]['amount'], 398.34)
        self.assertEqual(insight_data['Royal Bank of Scotland - Current Accounts'].transaction_history[2]['amount'], 1708.12)
        self.assertEqual(insight_data['Royal Bank of Scotland - Current Accounts'].transaction_history[3]['amount'], 1109.01)

        self.assertEqual(insight_data['Royal Bank of Scotland - Current Accounts'].transaction_history[0]['amount'], 896.65)
        self.assertEqual(insight_data['Royal Bank of Scotland - Current Accounts'].transaction_history[1]['amount'], 398.34)

    def test_correct_instution_for_access_token(self):
        self.assertEqual(self.debit_card.plaid_wrapper.get_institution_name(self.debit_card.plaid_wrapper.ACCESS_TOKEN),'Royal Bank of Scotland - Current Accounts')


    def test_get_balances_with_incorrect_access_token(self):
        self.debit_card.access_tokens = ['wrongaccesstokenstring']
        with self.assertRaises(AccessTokenInvalid):
            self.debit_card.get_account_balances()

    def test_get_balances_for_custom_user_one_access_token(self):
        accounts = self.debit_card.get_account_balances()
        same_accounts = self.debit_card.get_account_balances()
        self.assertTrue(self.are_dicts_same(accounts,same_accounts))
        self.assertEqual(len(list(accounts.keys())),1)
        self.assertEqual(list(accounts.keys())[0], 'Royal Bank of Scotland - Current Accounts')
        self.assertEqual(len(list(accounts[list(accounts.keys())[0]].keys())), 2)

    def test_get_balances_for_custom_user_one_access_token_different_amounts(self):
        accounts = self.debit_card.get_account_balances()
        same_accounts = self.debit_card.get_account_balances()
        account_ids = list(same_accounts['Royal Bank of Scotland - Current Accounts'].keys())
        same_accounts['Royal Bank of Scotland - Current Accounts'][account_ids[0]]['available_amount'] = 0
        same_accounts['Royal Bank of Scotland - Current Accounts'][account_ids[0]]['currency'] = 'GBP'
        self.assertFalse(self.are_dicts_same(accounts,same_accounts))

    def test_get_balances_for_multiple_access_tokens(self):
        user_lilly = User.objects.get(email='lillydoe@example.org')
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token_custom_user(bank_id='ins_115642', products_chosen=['transactions'], override_username="custom_sixth")
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(user_lilly, ['transactions'])

        plaid_wrapper_2 = SandboxWrapper()
        public_token_2 = plaid_wrapper_2.create_public_token_custom_user(bank_id='ins_1', products_chosen=['transactions'], override_username="custom_sixth")
        plaid_wrapper_2.exchange_public_token(public_token_2)
        plaid_wrapper_2.save_access_token(user_lilly, ['transactions'])

        debit_card_lilly = DebitCard(plaid_wrapper, user_lilly)

        self.assertEqual(len(debit_card_lilly.access_tokens),2)

        balances = debit_card_lilly.get_account_balances()
        same_balances = debit_card_lilly.get_account_balances()
        self.assertTrue(self.are_dicts_same(balances,same_balances))

        self.assertTrue(list(balances.keys())[0], 'Royal Bank of Scotland - Current Accounts')
        self.assertTrue(list(balances.keys())[1], 'Bank of America')

    def test_refresh_api_with_incorrect_access_token(self):
        self.debit_card.plaid_wrapper.ACCESS_TOKEN = 'wrongaccesstokenstring'
        with self.assertRaises(AccessTokenInvalid):
            self.debit_card.refresh_api(self.debit_card.plaid_wrapper.ACCESS_TOKEN)

    def test_get_transactions_with_incorrect_access_token(self):
        self.debit_card.access_tokens = ['wrongaccesstokenstring']
        with self.assertRaises(AccessTokenInvalid):
            start_date = date.fromisoformat('2022-12-16')
            end_date = date.fromisoformat('2022-12-19')
            transactions = self.debit_card.get_transactions_by_date(start_date,end_date)

    def test_get_transactions_with_one_and_multiple_access_token(self):
        user_lilly = User.objects.get(email='lillydoe@example.org')
        plaid_wrapper = SandboxWrapper()
        plaid_wrapper_2 = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token_custom_user()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(user_lilly, ['transactions'])

        public_token_2 = plaid_wrapper_2.create_public_token_custom_user(bank_id='ins_1', products_chosen=['transactions'])
        plaid_wrapper_2.exchange_public_token(public_token_2)
        plaid_wrapper_2.save_access_token(user_lilly, ['transactions'])

        debit_card_lilly = DebitCard(plaid_wrapper, user_lilly)

        self.assertEqual(len(debit_card_lilly.access_tokens),2)

        start_date = date.fromisoformat('2022-12-16')
        end_date = date.fromisoformat('2022-12-19')
        transactions = debit_card_lilly.get_transactions_by_date(start_date,end_date)

        self.assertEqual(len(transactions),2)
        self.assertEqual(len(transactions[0]),4)
        self.assertEqual(len(transactions[1]),4)

        self.assertFalse(self.are_dicts_same(transactions[0], transactions[1]))

        self.assertEqual(transactions[0][0]['amount'], 896.65)
        self.assertEqual(transactions[0][1]['amount'], 398.34)
        self.assertEqual(transactions[0][2]['amount'], 1708.12)
        self.assertEqual(transactions[0][3]['amount'], 1109.01)

    def test_get_non_existent_institution_name_from_db(self):
        access_tokens = 'wrongaccesstokenstring'
        institution_name = self.debit_card.get_institution_name_from_db(access_tokens)
        self.assertEqual(institution_name,None)

    def test_get_empty_insight_data_dict(self):
        self.assertEqual(self.debit_card.get_insight_data(), None)

    def test_create_debit_card_without_existing_access_tokens(self):
        concrete_wrapper = SandboxWrapper()
        user_lilly = User.objects.get(email='lillydoe@example.org')

        with self.assertRaises(PublicTokenNotExchanged):
            incorrect_debit_card = DebitCard(concrete_wrapper,user_lilly)

    def test_get_account_balances_with_None_available_amount_value(self):
        # Get the path to the directory containing the test file
        test_dir = os.path.dirname(os.path.abspath(__file__))

        # Specify the path to the json file relative to the test file directory
        json_file_path = os.path.join(test_dir, 'account.json')


        with open(json_file_path, 'r') as f:
            account_data = json.load(f)
            reformatted_data = format_accounts_data(account_data)

            for account in reformatted_data:
                self.assertTrue(reformatted_data[account]['available_amount'] is not None)
                self.assertTrue(reformatted_data[account]['current_amount'] is not None)
                self.assertTrue(isinstance(reformatted_data[account]['name'], str))
                self.assertTrue(isinstance(reformatted_data[account]['type'], str))
                self.assertTrue(isinstance(reformatted_data[account]['currency'], str))

    #attempt to incorporate set up in this
    def test_make_transaction_data_insight_with_one_access_token(self):
        user = User.objects.get(email='lillydoe@example.org')
        plaid_wrapper = SandboxWrapper()
        public_token = plaid_wrapper.create_public_token()
        plaid_wrapper.exchange_public_token(public_token)
        plaid_wrapper.save_access_token(user, ['transactions'])
        debit_card = DebitCard(plaid_wrapper, user)

        start_date = date.fromisoformat('2022-06-13')
        end_date = date.fromisoformat('2022-12-16')
        debit_card.make_graph_transaction_data_insight(start_date,end_date)

        insights = debit_card.get_insight_data()
        self.assertTrue(insights is not None)
        self.assertEqual(list(insights.keys())[0],'Royal Bank of Scotland - Current Accounts')
        self.assertTrue(isinstance(insights['Royal Bank of Scotland - Current Accounts'], BankGraphData))
