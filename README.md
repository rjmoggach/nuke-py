# nuke-py

This is my self-curated collection of python tools for Nuke.

I take no author credit for any of these whether I've written them or not. They've come from many different
people and morphed over the years into what they are now. They've all been cleaned up to
match my own [PEP 8](http://legacy.python.org/dev/peps/pep-0008/) preference for styling python code. 
I'm not a fan of camelCase as it's too easily mistaken for Capitalized and I always favor indents of 2 spaces
instead of 4 spaces or tabs. (despite VFX tendencies to prefer silly camelCase)

## Function Input Conventions

In general when I'm writing a tool that operates on a node, nodes, or all nodes I like to
keep it open to what input it takes so alot of the rewrites involve tailoring functions
in this manner. An example below:


    def eat_my_nodes(nodes=[]):
      if not nodes:
        nodes=nuke.selectedNodes()
      if not nodes:
        nodes=nuke.allNodes()
      if nodes:
        for node in nodes:
          eat_str = 'Eating Node: {0}'.format(node.name())
          nuke.tprint(eat_str)
        return
      else:
        return


This way I can use this function programatically somewhere else, I can pass in a list of nodes using nuke.SelectedNodes() or
some other way, or I can let it run on it's own and it will work as well.

## Menus

I have another tool called MyNk that I use inside my dotnuke folder to automagically add this or other structures
of python scripts to a namespaced python object. As part of that process the tool looks for the __menus__ attribute
in each function and uses that to generate my custom menus for me. The syntax is pretty straight forward. Here's
an example for the above function.

    __menus__ = {
      'Tools/Info/Eat Selected Nodes':  {
        'cmd': 'eat_my_nodes(nuke.selectedNodes())',
        'hotkey': '',
        'icon': ''
      },
      'Tools/Info/Eat All Read Nodes':  {
        'cmd': 'eat_my_nodes(nuke.allNodes('Read'))',
        'hotkey': '',
        'icon': ''
      }
    }
 
So that should make sense, although unless you're using the other tool or code like it you can ignore this.