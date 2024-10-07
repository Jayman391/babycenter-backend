import babycenterdb
import babycenterdb.filter
from datetime import datetime

class Query:
  def __init__(self, params : dict):
    
    if params["post_or_comment"] not in ["posts", "comments"]:
            self.query_type = "posts"
    params.pop("post_or_comment")

    if int(params["num_documents"]) <= 0:
        self.num_documents = 10000
    
    params.pop("num_documents")

    self.filters = self.build_filters(params)
    self.query = babycenterdb.Query(self.query_type, filters=self.filters, limit=self.num_documents)

  def build_filters(self, params : dict) -> dict:
    
    filters = []

    for key, value in params.items():
      if key == "country":
        filters.append(babycenterdb.filter.CountryFilter(str(value).upper()))
      if key == "start":
        if params["end"] != "none":
           filters.append(babycenterdb.filter.DateFilter(floor=datetime(value), ceil=datetime(params["end"])))
      if key == "keywords":
        pass
      if key == "groups":
        if str(value).contains(','):
            filters.append(babycenterdb.filter.GroupFilter(value_list=str(value).split(',')))
        elif value != "all":
            filters.append(babycenterdb.filter.GroupFilter(value_list=[str(value)]))
      if key == "num_comments":
        pass

  def execute(self):
    pass

class QueryFactory:
  def __init__(self):
    pass
  def create_query(self, params):
    return Query(params)