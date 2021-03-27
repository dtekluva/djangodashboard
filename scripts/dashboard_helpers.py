from app.models import *
### FOR TEMPLATE RENDERING
from io import BytesIO
import random, os, json
from datetime import datetime

def get_extra_context(**params):
  print(params)

  if "single_member" in params.get("segment", ""):

    return dict(
                member_details = Member.get_single(params.get("id")),
                member_transactions = Transaction.get_for_member(params.get("id"))
              )

  else:

    return dict(
                member_details = {},
                member_transactions = {}
              )