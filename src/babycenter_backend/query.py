import babycenterdb
import babycenterdb.filter
from babycenterdb.query import Query
from datetime import datetime
import pandas as pd
from pydantic import BaseModel, model_validator

class QueryWrapper(BaseModel):
    post_or_comment: str
    num_documents: int
    country: str
    startDate: str
    endDate: str
    keywords: list
    groups: list
    num_comments: int

    @model_validator(mode='before')
    @classmethod
    def validate(cls, values):
        # Validate query_type
        post_or_comment = values.get('post_or_comment')
        if post_or_comment not in ['posts', 'comments']:
            raise ValueError('Query type must be either "posts" or "comments"')

        # Validate num_documents
        num_documents = values.get('num_documents')
        if num_documents is not None and num_documents <= 0:
            raise ValueError('Number of documents must be greater than 0')

        # Validate country
        country = values.get('country')
        if country is not None and str(country).upper() not in ['USA', 'BRAZIL']:
            raise ValueError('Country must be either "USA" or "BRAZIL"')

        # Validate start date
        startDate = values.get('startDate')
        if startDate is not None:
            try:
                datetime.strptime(startDate, "%Y%m%d")
            except ValueError:
                raise ValueError('Start date must be in the format YYYYMMDD')

        # Validate end date
        endDate = values.get('endDate')
        if endDate is not None:
            try:
                datetime.strptime(endDate, "%Y%m%d")
            except ValueError:
                raise ValueError('End date must be in the format YYYYMMDD')

        # Validate keywords
        keywords = values.get('keywords')
        if keywords:
            if len(keywords) > 1 and keywords[0] == 'all':
                raise ValueError('Keywords cannot be "all"')
            for keyword in keywords:
                if not isinstance(keyword, str) or not keyword.isalpha():
                    raise ValueError('Keywords must be alphanumeric strings')

        # Validate groups
        groups = values.get('groups')
        if groups:
            if len(groups) > 1 and groups[0] == 'all':
                raise ValueError('Groups cannot be "all"')
            for group in groups:
                if not isinstance(group, str) or not group.isalpha():
                    raise ValueError('Groups must be alphanumeric strings')

        # Validate num_comments
        num_comments = values.get('num_comments')
        if type(num_comments) != int or num_comments < -1:
            raise ValueError('Number of comments must be an integer')

        return values

    def build_filters(self) -> list:
        filters = []
        # Country Filter
        filters.append(babycenterdb.filter.CountryFilter(value=self.country.upper()))
        # Date Filter
        start_date = datetime.strptime(self.startDate, "%Y%m%d")
        end_date = datetime.strptime(self.endDate, "%Y%m%d")
        filters.append(babycenterdb.filter.DateFilter(floor=start_date, ceiling=end_date))
        # Keywords Filter
        keywords = self.keywords
        if len(keywords) == 1 and keywords[0] == 'all':
            keywords.remove('all')

        if len(keywords) > 1:
            filters.append(babycenterdb.filter.TextFilter(value_list=keywords))
        elif len(keywords) == 1:
            filters.append(babycenterdb.filter.TextFilter(value=keywords[0]))
        # Groups Filter
        groups = self.groups
        if len(groups) == 1 and groups[0] == 'all':
            groups.remove('all')

        if len(groups) > 1:
            filters.append(babycenterdb.filter.GroupFilter(value_list=groups))
        elif len(groups) == 1:
            filters.append(babycenterdb.filter.GroupFilter(value=groups[0]))
        # Number of Comments Filter
        num_comments = self.num_comments

        if num_comments > 0 and self.post_or_comment == 'posts':
            filters.append(babycenterdb.filter.NumCommentsFilter(value=num_comments))

        return filters

    def execute(self) -> dict:
        filters = self.build_filters()
        query = Query(collection=self.post_or_comment, filters=filters, limit=self.num_documents)
        data = pd.DataFrame(query.execute())
        data.fillna(0, inplace=True)
        data['_id'] = data['_id'].astype(str)
        return data.to_dict(orient='records')
    

class Loader(BaseModel):
    computed_type: str
    name: str

    """
    @model_validator(mode='before')
    @classmethod
    def validate(cls, values):
        # Validate type             
        computed_type = values.get('computed_type')
        if computed_type not in ['query', 'ngram', 'topic']:
            raise ValueError('Type must be either "query", "ngram", or "topic"')
        
        name = values.get('name')
        if not isinstance(name, str):
            raise ValueError('Name must be a string')
        return values
    """
    
    def build_filters(self) -> list:
        filters = []
        if self.name != 'all':
            filters.append(babycenterdb.filter.IDFilter(value=self.name))

        # Try passing computed_type directly
        filters.append(babycenterdb.filter.TypeFilter(value=self.computed_type))
        return filters

    
    def execute(self) -> dict:
        collection = 'precomputed'
        filters = self.build_filters()
        query = Query(collection=collection, filters=filters)
        data = pd.DataFrame(query.execute())
        data.fillna(0, inplace=True)
        data['_id'] = data['_id'].astype(str)
        return data.to_dict(orient='records')
        
