import babycenterdb
import babycenterdb.filter
from babycenterdb.query import Query
from datetime import datetime
import pandas as pd
import json

class QueryWrapper:
  def __init__(self, params : dict):
   
    self.query_type = params.pop("post_or_comment")

    if int(params["num_documents"]) <= 0:
      self.num_documents = 10000
    self.num_documents =params.pop("num_documents")

    self.filters = self.build_filters(params)
    self.query = Query(collection=self.query_type, filters=self.filters, limit=int(self.num_documents))
  
  def build_filters(self, params: dict) -> dict:
    filters = []
    # Country Filter
    filters.append(babycenterdb.filter.CountryFilter(value=str(params['country']).upper()))
    # Date Filter
    start_date = datetime.strptime(params['start'], "%Y%m%d")  # Assuming start is in YYYYMMDD format
    end_date = datetime.strptime(params['end'], "%Y%m%d")  # Assuming end is in YYYYMMDD format
    filters.append(babycenterdb.filter.DateFilter(floor=start_date, ceiling=end_date))
    # Keywords Filter
    keywords = params['keywords']
    if len(keywords) == 1 and keywords[0] == 'all':
      keywords.remove('all')

    print(keywords)

    if len(keywords) > 1:
        filters.append(babycenterdb.filter.TextFilter(value_list=keywords))
    elif len(keywords) == 1:
        filters.append(babycenterdb.filter.TextFilter(value=keywords[0]))
    # Groups Filter
    groups = params['groups']
    if len(groups) == 1 and groups[0] == 'all':
      groups.remove('all')

    if len(groups) > 1:
        filters.append(babycenterdb.filter.GroupFilter(value_list=groups))
    elif len(groups) == 1:
        filters.append(babycenterdb.filter.GroupFilter(value=groups[0]))
    # Number of Comments Filter
    num_comments = int(params['num_comments'])

    if num_comments > 0 and self.query_type == 'posts':
        filters.append(babycenterdb.filter.NumCommentsFilter(value=num_comments))

    print(filters)
    return filters

  def execute(self) -> dict:
    data = pd.DataFrame(self.query.execute())
    data.fillna(int(0), inplace=True)
    data['_id'] = data['_id'].astype(str)
    data = data.to_dict(orient='records')
    return data