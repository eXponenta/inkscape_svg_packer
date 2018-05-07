#!/usr/bin/env python

# These two lines are only needed if you don't put the script directly into
# the installation directory
import sys
import os
import json

sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex
# The simplestyle module provides functions for style parsing.
from simplestyle import *

class HelloWorldEffect(inkex.Effect):
    """
    Example Inkscape effect extension.
    Creates a new layer with a "Hello World!" text centered in the middle of the document.
    """
    def __init__(self):
        """
        Constructor.
        Defines the "--what" option of a script.
        """
        # Call the base class constructor.
        inkex.Effect.__init__(self)

        self.OptionParser.add_option('-f', '--from_directory', action='store', type='string', dest='from_directory',
                                     default='/', help='Read from:')
        self.OptionParser.add_option('-t', '--to_directory', action='store', type='string', dest='to_directory',
                                     default='/', help='Save to:')
        self.OptionParser.add_option('-n', '--name', action='store', type='string', dest='name',
                                     default='128', help='Name')
        self.OptionParser.add_option('-c', '--create_json', action='store', type='string', dest='create_json',
                                     default='True', help='Create JSON pack file')
        self.OptionParser.add_option('-r', '--recursive', action='store', type='string', dest='recursive',
                                     default='True', help='Recursive pack files')
        self.OptionParser.add_option('-p', '--padings', action='store', type='int', dest='padings',
                                     default=4, help='Padings between elements')

    def parseSVG(self,fname):
        svg = inkex.etree.parse(fname).getroot()
        w = svg.get("width")
        h = svg.get("height")
        if(w == None or h == None):
            vb = svg.get("viewBox").split(" ");
            w = vb[2]
            h = vb[3]
        
        name = os.path.basename(fname)
        svg.set(inkex.addNS('label', 'inkscape'), name)
        return {
            "svg":svg,
                "meta":{
                    "name" : name,
                    "path" : fname,
                    "width" : w,
                    "height" : h,
                }
            }

    def load(self,recursive, _dir):
        loaded_svg = list()
        for root, directories, filenames in os.walk(_dir):
            for filename in filenames:
                path = os.path.join(root,filename).decode("cp1251")
                if(filename.endswith(".svg")):
                    loaded_svg.append( self.parseSVG(path) )
                    #loaded_svg.append(path)
            if(not recursive):
                break
        return loaded_svg

    def effect(self):
        """
        Effect behaviour.
        Overrides base class' method and inserts "Hello World" text into SVG document.
        """
        # Get script's "--what" option value.
        name = self.options.name
        fd = self.options.from_directory
        td = self.options.to_directory
        rc = self.options.recursive

        pairs = self.load(rc, fd)
        """
        with open(os.path.join(td, name + "_atlas.json"), "w") as atlas:
            atlas.write(json.dumps(pairs,
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': '),
                    ensure_ascii=False).encode("utf-8"))
        """
        # Get access to main SVG document element and get its dimensions.
        svg = self.document.getroot()
        # or alternatively
        # svg = self.document.xpath('//svg:svg',namespaces=inkex.NSS)[0]

        # Again, there are two ways to get the attibutes:
        width  = self.unittouu(svg.get('width'))
        height = self.unittouu(svg.get('height'))
        # Create a new layer.
        layer = inkex.etree.SubElement(svg, 'g')
        layer.set(inkex.addNS('label', 'inkscape'), name)
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

        for p in pairs:
            layer.append(p["svg"])

# Create effect instance and apply it.
effect = HelloWorldEffect()
effect.affect()