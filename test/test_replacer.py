# Fix error module not found
import os
import sys
sys.path.append(os.getcwd())

from jagad.utils.replacer import replace_prompt
from jagad.utils.constants import DEFAULT_PROMPT

print (replace_prompt(DEFAULT_PROMPT, path="~"))