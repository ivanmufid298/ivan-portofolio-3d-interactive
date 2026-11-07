import bpy, math, random, os
from mathutils import Vector
random.seed(18)
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
def mat(name, color, emission=0):
 m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
 p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'); p.inputs['Base Color'].default_value=(*color,1); p.inputs['Roughness'].default_value=.78
 if emission: p.inputs['Emission Color'].default_value=(*color,1); p.inputs['Emission Strength'].default_value=emission
 return m
grass=mat('Moss · jade',(.22,.36,.24)); earth=mat('Island · earth',(.13,.22,.19)); water=mat('Water · jade',(.12,.46,.48)); red=mat('Torii · vermilion',(.65,.12,.08)); wood=mat('Wood · cedar',(.20,.10,.065)); roof=mat('Roof · charcoal',(.08,.15,.16)); plaster=mat('Walls · ivory',(.83,.72,.51)); stone=mat('Stone · warm gray',(.46,.48,.40)); glow=mat('Lantern · light',(1,.52,.12),2)
pinks=[mat('Sakura '+str(i),c) for i,c in enumerate([(.91,.45,.52),(.98,.64,.65),(.83,.30,.43),(.99,.75,.72)])]
def finish(o,name,material):
 o.name=name; o.data.materials.append(material); return o
def cube(name,loc,scale,material):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.scale=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); return finish(o,name,material)
def ico(name,loc,scale,material,sub=1):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc); o=bpy.context.object; o.scale=scale; return finish(o,name,material)
def beam(name,a,b,r,material):
 d=Vector(b)-Vector(a); bpy.ops.mesh.primitive_cylinder_add(vertices=8,radius=r,depth=d.length,location=(Vector(a)+Vector(b))/2); o=bpy.context.object; o.rotation_euler=d.to_track_quat('Z','Y').to_euler(); return finish(o,name,material)
def mesh(name,vs,fs,material):
 m=bpy.data.meshes.new(name); m.from_pydata(vs,[],fs); m.update(); o=bpy.data.objects.new(name,m); bpy.context.collection.objects.link(o); o.data.materials.append(material); return o
# A deliberately sculpted floating garden. Blender Z becomes web Y on export.
ico('Floating garden foundation',(0,0,-.75),(7.6,5.8,1.6),earth,2)
ico('Moss garden',(0,0,-.23),(7.45,5.7,.8),grass,2)
ico('Koi pond',(0,-1.1,.59),(5.6,2.65,.06),water,3)
for i in range(38):
 t=i/38*math.tau; x=5.65*math.cos(t); y=-1.1+2.7*math.sin(t)
 ico('Pond riverstone',(x,y,.57),(random.uniform(.2,.55),random.uniform(.2,.45),random.uniform(.18,.4)),stone)
# Arched cedar bridge across the pond.
for i in range(19):
 x=-2.1+i*.235; z=.65+.6*(1-(x/2.3)**2)
 cube('Bridge plank',(x,-1.2,z),(.23,1.4,.13),wood)
 for y in [-1.98,-.42]:
  if i%3==0: beam('Bridge red post',(x,y,z),(x,y,z+.7),.065,red)
  if i<18:
   xx=x+.235; zz=.65+.6*(1-(xx/2.3)**2)
   beam('Bridge rail',(x,y,z+.65),(xx,y,zz+.65),.055,red)
# Torii facing the visitor.
for x in [-4.65,-2.55]:
 beam('Torii vermilion pillar',(x,.8,.35),(x,.8,3.65),.16,red); cube('Torii stone foot',(x,.8,.42),(.48,.48,.3),stone)
cube('Torii lower lintel',(-3.6,.8,2.9),(2.9,.22,.23),red)
cube('Torii upper lintel',(-3.6,.8,3.65),(3.4,.38,.22),red)
cube('Torii black crown',(-3.6,.8,3.82),(3.7,.43,.13),roof)
cube('Torii central tablet',(-3.6,.66,3.27),(.35,.13,.48),wood)
for x in [-5.35,-1.85]: beam('Torii raised eave',(x,.8,3.82),(x+(-.3 if x<-3 else .3),.8,3.97),.08,roof)
# Pagoda with three curved, broad hipped roofs.
px,py=2.5,1.6
cube('Temple stone platform',(px,py,.45),(3.3,2.8,.4),stone)
for level in range(3):
 z=.65+level*1.35; w=2.6-level*.5; d=2.15-level*.4
 cube('Pagoda ivory walls',(px,py,z+.5),(w,d,.95),plaster)
 for dx in [-w/2,w/2]:
  for dy in [-d/2,d/2]: beam('Pagoda cedar pillar',(px+dx,py+dy,z),(px+dx,py+dy,z+1),.085,red)
 for dx in [-.6,0,.6]: cube('Pagoda window',(px+dx*(w/2),py-d/2-.01,z+.48),(.25,.035,.58),wood)
 vs=[]
 for sx,sy,h in [(w/2+.48,d/2+.48,z+.92),(w/2+.20,d/2+.20,z+1.02),(.3,.24,z+1.62)]:
  vs += [(px-sx,py-sy,h),(px+sx,py-sy,h),(px+sx,py+sy,h),(px-sx,py+sy,h)]
 fs=[(j*4+i,j*4+(i+1)%4,(j+1)*4+(i+1)%4,(j+1)*4+i) for j in range(2) for i in range(4)]+[(8,9,10,11)]
 mesh('Pagoda sweeping roof',vs,fs,roof)
beam('Pagoda spire',(px,py,4.8),(px,py,5.6),.045,glow)
for z in [5,5.2,5.4]: ico('Spire ornament',(px,py,z),(.12,.12,.05),glow)
for x,y,s in [(-5,2,1.1),(-1.2,3.1,1.15),(5,1.3,1),(4,-3,.8),(-4.8,-2.6,.85)]:
 beam('Sakura trunk',(x,y,.3),(x+.15,y,2.3*s),.13*s,wood)
 for j in range(7):
  t=j*math.tau/7; bx=x+math.cos(t)*.85*s; by=y+math.sin(t)*.7*s; bz=(2.2+random.uniform(0,.5))*s
  beam('Sakura branch',(x,y,1.3*s),(bx,by,bz),.055*s,wood)
  ico('Sakura blossom',(bx,by,bz),(.85*s,.73*s,.64*s),pinks[j%4],2)
for i in range(22):
 x=random.uniform(-6,6); y=random.uniform(2.9,4)
 ico('Garden shrub',(x,y,.45),(.45,.45,.5),grass,1)
for x,y in [(-2.3,-2.7),(2.6,-2.3),(-4.5,.1),(4.4,.1)]:
 cube('Stone lantern base',(x,y,.4),(.45,.45,.25),stone); beam('Stone lantern stem',(x,y,.4),(x,y,.95),.12,stone)
 cube('Lantern glowing chamber',(x,y,1.05),(.3,.3,.35),glow); ico('Lantern cap',(x,y,1.3),(.4,.4,.18),roof)
for i in range(13): cube('Stepping stone',(-1.8+i*.32,1.15,.4),(.27,.55,.12),stone)
# Daylight and camera remain in the editable Blender file.
bpy.ops.object.light_add(type='AREA', location=(-3,-4,10)); bpy.context.object.data.energy=1800; bpy.context.object.data.shape='DISK'; bpy.context.object.data.size=8
bpy.ops.object.camera_add(location=(11,-16,12)); cam=bpy.context.object; cam.rotation_euler=(Vector((0,0,1))-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.type='ORTHO'; cam.data.ortho_scale=19
sc=bpy.context.scene; sc.camera=cam; sc.world.color=(.35,.35,.35); sc.render.resolution_x=1500; sc.render.resolution_y=1200; sc.render.resolution_percentage=100
sc['README']='Ivan Digital Garden. Editable original meshes. Export assets/garden.glb after edits. Web day/night lighting lives in scene.js.'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','Ivan-Japanese-Garden.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT,'assets','garden.glb'),export_format='GLB',export_cameras=False,export_lights=False)
print('GARDEN_SAVED',len(sc.objects))
