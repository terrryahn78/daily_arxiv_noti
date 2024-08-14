# encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# Authentication for user filing issue (must have read/write access to repository to add issue to)
USERNAME = '**username**'
#TOKEN = '**github_token**'

# The repository to add this issue to
REPO_OWNER = '**username**'
REPO_NAME = 'daily-arxiv-noti'

# Set new submission url of subject
NEW_SUB_URL = ['https://arxiv.org/list/cond-mat/new', 'https://arxiv.org/list/quant-ph/new']


# Keywords to search
KEYWORD_LIST = ["keyword1", "keyword2", ...]