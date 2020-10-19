import nukeDrawTool

markup = nuke.menu("Nodes")
markup.addCommand('NukeDraw',"nukeDrawTool.start()",icon="screen.png")