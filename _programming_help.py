from dragonfly import (
    CompoundRule,
    MappingRule,
    RuleRef,
    Repetition,
    Dictation,
    IntegerRef,
    Grammar
)

from lib.dynamic_aenea import (
    GlobalDynamicContext,
    Key,
    Text,
)

class SeriesMappingRule(CompoundRule):

    def __init__(self, mapping, extras=None, defaults=None):
        mapping_rule = MappingRule(mapping=mapping, extras=extras,
                                   defaults=defaults, exported=False)
        single = RuleRef(rule=mapping_rule)
        series = Repetition(single, min=1, max=16, name="series")

        compound_spec = "<series>"
        compound_extras = [series]
        CompoundRule.__init__(self, spec=compound_spec,
                              extras=compound_extras, exported=True)

    def _process_recognition(self, node, extras):  # @UnusedVariable
        series = extras["series"]
        for action in series:
            action.execute()

series_rule = SeriesMappingRule(
    mapping={
        # Filler words.
        "foobar": Text("foobar"),
        "foo": Text("foo"),
        "bar": Text("bar"),
        # Lorem ipsum, filler text
        # (Multiple Key's are much faster than long Text's.)
        "Lorem ipsum [short]": Key("L,o,r,e,m,space,i,p,s,u,m,space,d,o,l,o,r,space,s,i,t,space,a,m,e,t,comma,space,c,o,n,s,e,c,t,e,t,u,r,space,a,d,i,p,i,s,i,c,i,n,g,space,e,l,i,t,dot"),  # @IgnorePep8
        "Lorem ipsum medium": Key("L,o,r,e,m,space,i,p,s,u,m,space,d,o,l,o,r,space,s,i,t,space,a,m,e,t,comma,space,c,o,n,s,e,c,t,e,t,u,r,space,a,d,i,p,i,s,i,c,i,n,g,space,e,l,i,t,comma,space,s,e,d,space,d,o,space,e,i,u,s,m,o,d,space,t,e,m,p,o,r,space,i,n,c,i,d,i,d,u,n,t,space,u,t,space,l,a,b,o,r,e,space,e,t,space,d,o,l,o,r,e,space,m,a,g,n,a,space,a,l,i,q,u,a,dot,space,U,t,space,e,n,i,m,space,a,d,space,m,i,n,i,m,space,v,e,n,i,a,m,comma,space,q,u,i,s,space,n,o,s,t,r,u,d,space,e,x,e,r,c,i,t,a,t,i,o,n,space,u,l,l,a,m,c,o,space,l,a,b,o,r,i,s,space,n,i,s,i,space,u,t,space,a,l,i,q,u,i,p,space,e,x,space,e,a,space,c,o,m,m,o,d,o,space,c,o,n,s,e,q,u,a,t,dot"),  # @IgnorePep8
        "Lorem ipsum long": Key("L,o,r,e,m,space,i,p,s,u,m,space,d,o,l,o,r,space,s,i,t,space,a,m,e,t,comma,space,c,o,n,s,e,c,t,e,t,u,r,space,a,d,i,p,i,s,i,c,i,n,g,space,e,l,i,t,comma,space,s,e,d,space,d,o,space,e,i,u,s,m,o,d,space,t,e,m,p,o,r,space,i,n,c,i,d,i,d,u,n,t,space,u,t,space,l,a,b,o,r,e,space,e,t,space,d,o,l,o,r,e,space,m,a,g,n,a,space,a,l,i,q,u,a,dot,space,U,t,space,e,n,i,m,space,a,d,space,m,i,n,i,m,space,v,e,n,i,a,m,comma,space,q,u,i,s,space,n,o,s,t,r,u,d,space,e,x,e,r,c,i,t,a,t,i,o,n,space,u,l,l,a,m,c,o,space,l,a,b,o,r,i,s,space,n,i,s,i,space,u,t,space,a,l,i,q,u,i,p,space,e,x,space,e,a,space,c,o,m,m,o,d,o,space,c,o,n,s,e,q,u,a,t,dot,space,D,u,i,s,space,a,u,t,e,space,i,r,u,r,e,space,d,o,l,o,r,space,i,n,space,r,e,p,r,e,h,e,n,d,e,r,i,t,space,i,n,space,v,o,l,u,p,t,a,t,e,space,v,e,l,i,t,space,e,s,s,e,space,c,i,l,l,u,m,space,d,o,l,o,r,e,space,e,u,space,f,u,g,i,a,t,space,n,u,l,l,a,space,p,a,r,i,a,t,u,r,dot,space,E,x,c,e,p,t,e,u,r,space,s,i,n,t,space,o,c,c,a,e,c,a,t,space,c,u,p,i,d,a,t,a,t,space,n,o,n,space,p,r,o,i,d,e,n,t,comma,space,s,u,n,t,space,i,n,space,c,u,l,p,a,space,q,u,i,space,o,f,f,i,c,i,a,space,d,e,s,e,r,u,n,t,space,m,o,l,l,i,t,space,a,n,i,m,space,i,d,space,e,s,t,space,l,a,b,o,r,u,m,dot,L,o,r,e,m,space,i,p,s,u,m,space,d,o,l,o,r,space,s,i,t,space,a,m,e,t,comma,space,c,o,n,s,e,c,t,e,t,u,r,space,a,d,i,p,i,s,i,c,i,n,g,space,e,l,i,t,comma,space,s,e,d,space,d,o,space,e,i,u,s,m,o,d,space,t,e,m,p,o,r,space,i,n,c,i,d,i,d,u,n,t,space,u,t,space,l,a,b,o,r,e,space,e,t,space,d,o,l,o,r,e,space,m,a,g,n,a,space,a,l,i,q,u,a,dot,space,U,t,space,e,n,i,m,space,a,d,space,m,i,n,i,m,space,v,e,n,i,a,m,comma,space,q,u,i,s,space,n,o,s,t,r,u,d,space,e,x,e,r,c,i,t,a,t,i,o,n,space,u,l,l,a,m,c,o,space,l,a,b,o,r,i,s,space,n,i,s,i,space,u,t,space,a,l,i,q,u,i,p,space,e,x,space,e,a,space,c,o,m,m,o,d,o,space,c,o,n,s,e,q,u,a,t,dot,space,D,u,i,s,space,a,u,t,e,space,i,r,u,r,e,space,d,o,l,o,r,space,i,n,space,r,e,p,r,e,h,e,n,d,e,r,i,t,space,i,n,space,v,o,l,u,p,t,a,t,e,space,v,e,l,i,t,space,e,s,s,e,space,c,i,l,l,u,m,space,d,o,l,o,r,e,space,e,u,space,f,u,g,i,a,t,space,n,u,l,l,a,space,p,a,r,i,a,t,u,r,dot,space,E,x,c,e,p,t,e,u,r,space,s,i,n,t,space,o,c,c,a,e,c,a,t,space,c,u,p,i,d,a,t,a,t,space,n,o,n,space,p,r,o,i,d,e,n,t,comma,space,s,u,n,t,space,i,n,space,c,u,l,p,a,space,q,u,i,space,o,f,f,i,c,i,a,space,d,e,s,e,r,u,n,t,space,m,o,l,l,i,t,space,a,n,i,m,space,i,d,space,e,s,t,space,l,a,b,o,r,u,m,dot"),  # @IgnorePep8
        # File extensions.
        "dot A S P": Text(".asp"),
        "dot A S P X": Text(".aspx"),
        "dot C S": Text(".cs"),
        "dot css": Text(".css"),
        "dot less": Text(".less"),
        "dot J S": Text(".js"),
        "dot jar": Text(".jar"),
        "dot (py|pie|P Y)": Text(".py"),
        "dot (ruby|R B)": Text(".rb"),
        "dot (rar|R A R)": Text(".rar"),
        "dot sass": Text(".sass"),
        "dot S H": Text(".sh"),
        "dot T X T": Text(".txt"),
        # Non mainstream web url extensions.
        "dot S E": Text(".se"),
        "dot (O R G|org)": Text(".org"),
        # Protocols.
        "protocol H T T P": Text("http://"),
        "protocol H T T P S": Text("https://"),
        "protocol (git|G I T)": Text("git://"),
        "protocol F T P": Text("ftp://"),
        "protocol S S H": Text("ssh://"),
        },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
        ],
    defaults={
        "n": 1
    }
)

grammar = Grammar("Programming help", context=GlobalDynamicContext())
grammar.add_rule(series_rule)
grammar.load()


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
