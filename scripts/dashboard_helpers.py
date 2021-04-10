from app.models import *
### FOR TEMPLATE RENDERING
from io import BytesIO
import random, os, json
from datetime import datetime

def get_extra_context(**params):

  if "single_member" in params.get("segment", ""):

    member_data = Transaction.get_for_member(params.get("id"))

    return dict(
                member_details = Member.get_single(params.get("id")),
                member_transactions = member_data.get("data"),
                member_totals = member_data.get("totals"),
              )
              
  elif "index" in params.get("segment", ""):

    return Transaction.get_graph_data()

  else:

    return dict(
                member_details = {},
                member_transactions = {},
                member_totals = {}
              )