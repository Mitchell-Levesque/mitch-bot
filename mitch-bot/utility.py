# File containing any utility functions

# Add "**" in front and behind message to bold it on discord
def bold(message: str) -> str:
  return "**"+message+"**"

# Add "*" in front and behind message to italicize it on discord
def italics(message: str) -> str:
  return "*"+message+"*"

# Add "***" in front and behind message to bold+italicize it on discord
def bold_and_italics(message: str) -> str:
    return "***"+message+"***"
