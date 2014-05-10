#python


layerservice = lx.Service('layerservice')
layerservice.select('layer.id', 'main')
layer_index = layerservice.query('layer.index')

layerservice.select('edge.N', 'all')
num_edges = layerservice.query('edge.N')

lx.eval('select.typeFrom vertex true')

for i in xrange(num_edges):
    layerservice.select('edge.vertList', str(i))
    verts = layerservice.query('edge.vertList')
    lx.eval('select.element %s vertex set %s' %(layer_index, verts[0]))
    lx.eval('select.element %s vertex add %s' %(layer_index, verts[1]))
    #lx.out('layerindex: %s| verts: %s' %(layer_index, verts))
    lx.eval('poly.makeCurveOpen')
    
layerservice.select('poly.N', 'all')
num_poly = layerservice.query('poly.N')

lx.eval('select.typeFrom polygon true')
lx.eval('select.drop polygon')
for i in xrange(num_poly):
    layerservice.select('poly.type', str(i))
    if layerservice.query('poly.type') == 'curve':
        lx.eval('select.element %s polygon add %s' %(layer_index, i))

lx.eval('cut')
lx.eval('layer.new')
lx.eval('paste')
