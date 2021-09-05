import pandas as pd
import ssl
import collections
from elasticsearch import Elasticsearch
from elasticsearch.connection import create_ssl_context
from cryptography.fernet import Fernet
import yaml
from datetime import datetime,timedelta


from gramex.transforms import handler
ssl_context = create_ssl_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

import warnings
warnings.filterwarnings('ignore')

def read_query(domain,objective,sub_objective):
    with open(domain+"_queries.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)[objective][sub_objective]
        except yaml.YAMLError as exc:
            print(exc)


def _decode_credentails():
    cred_filename = "secret.ini"

    key = ""

    with open("key.key", "r") as key_in:
        key = key_in.read().encode()

    f = Fernet(key)
    with open(cred_filename, "r") as cred_in:
        lines = cred_in.readlines()
        config = {}
        for line in lines:
            tuples = line.rstrip("\n").split("=", 1)
            if tuples[0] in ("Username", "Password"):
                config[tuples[0]] = tuples[1]

        password = f.decrypt(config["Password"].encode()).decode()
        return config["Username"], password


class ElasticResponse:
    """Get response from elasticsearch"""

    def __init__(
        self, host=["https://146.89.11.183:9200/"], auth=_decode_credentails()
    ):
        self.es = es = Elasticsearch(
            hosts=host,
            verify_certs=False,
            timeout=1000,
            http_auth=auth,
        )

    def _flatten(self, d, parent_key="", sep="_"):
        """Flatten the nested dict"""
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(self.flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    @staticmethod
    def _transform_response(result):
        df = pd.DataFrame(
            result["rows"], columns=[en.get("name") for en in result["columns"]]
        )
        return df

    @staticmethod
    def _sanitize_sql_query(query):
        """FutureImplementation : fix column names with spaces by adding escape character"""
        pass

    @staticmethod
    def _date_range_setter(query, params):
        return query.replace("from_timestamp", params.get('from_timestamp').__str__()).replace(
            "to_timestamp", params.get('to_timestamp').__str__()
        )

    @staticmethod
    def _whitespace_remover(dataframe):
        for i in dataframe.columns:
            # checking datatype of each columns
            if dataframe[i].dtype == 'object':
                # applying strip function on column
                dataframe[i] = dataframe[i].map(str.strip)
            else:
                # if condn. is False then it will do nothing.
                pass
        return dataframe

    def get_response(self, query,params):

        query = self._date_range_setter(query,params)
        results = self.es.sql.query(body={"query": query})
        results = self._transform_response(results)
        return self._whitespace_remover(results)

def main(handler):
    data = ElasticResponse()
    params =  handler.argparse(from_timestamp={'type': str, 'default':(datetime.utcnow()- timedelta(weeks=10)).isoformat()},
                               to_timestamp={'type': str, 'default':datetime.utcnow().isoformat()},
                               data={'type':bool,'default':False})
    sql_query = read_query("backup",*handler.path_args)
    return data.get_response(sql_query,params)



if __name__ == "__main__":
    main()

