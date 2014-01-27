from dragonfly import *

config = Config("Fastmail")
config.mailboxes = Section("Mailbox Mappings")
config.mailboxes.map = Item(
  {
    "inbox":       "Inbox",
    "archive":     "Archive",
    "drafts":      "Drafts",
    "sent":        "Sent",
    "spam":        "Spam",
    "trash":       "Trash"
  }
)

config.load()

class CommandRule(MappingRule):
  mapping = {
    # Composition.
    "compose [new] (email|message)": Key("c"),
    "discard (email|message)": Key("ctrl:down, shift:down, alt:down, backspace, alt:up, shift:up, ctrl:up"),
    "send (email|message)": Key("c-enter"),
    "reply to (email|message)": Key("r"),
    "reply to all": Key("a"),
    "forward (email|message)": Key("f"),

    # Searching.
    "search email <text>": Key("slash") + Text("%(text)s") + Key("enter"),

    # Mailboxes.
    "refresh mailbox": Key("u"),
    "go to mailbox <text>": Key("escape, escape, g") + Text("%(text)s") + Key("enter"),
    "go to <mailbox>": Key("escape, escape, g") + Text("%(mailbox)s") + Key("enter"),

    # Message list.
    "next (email|message)": Key("j"),
    "previous (email|message)": Key("k"),
    "open (email|message)": Key("o"),
    "select (email|message)": Key("x"),
    "delete (email|message|messages)": Key("d"),
    "archive (email|message|messages)": Key("y"),
    "(mark as spam|report spam)": Key("exclamation"),
    "mark (email|message) read": Key("dot/10, r"),
    "mark (email|message) unread": Key("dot/10, u"),
    "pin (email|message)": Key("dot/10, p"),
    "unpin (email|message)": Key("dot/10, n"),
    "move (email|message|messages)": Key("m"),
    "select all (email|messages)": Key("asterisk, a"),
    "(deselect (email|messages)|unselect all)": Key("asterisk, n"),

    # General.
    "undo (action|archive|delete|move)": Key("z"),
  }

  extras = [
    Dictation("text"),
    Choice("mailbox", config.mailboxes.map)
  ]

global_context = None # Context is None, so grammar will be globally active.
grammar = Grammar("Fastmail commands", context=global_context)
grammar.add_rule(CommandRule())
grammar.load()

# Unload function which will be called at unload time.
def unload():
  global grammar
  if grammar:
    grammar.unload()
  grammar = None