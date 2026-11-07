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
# Small living details, all editable in the source file.
ivory=mat('Koi porcelain',(.95,.88,.72)); orange=mat('Koi vermilion',(.90,.20,.055)); black=mat('Ink',(.022,.028,.025)); leaf=mat('Lotus jade',(.12,.32,.16)); gold=mat('Flower pollen',(.98,.61,.12)); catmat=mat('Cat warm cream',(.83,.62,.35)); pink=mat('Cat nose',(.62,.25,.28)); ripplemat=mat('Ripple foam',(.56,.79,.73)); bamboo=mat('Bamboo shade',(.47,.32,.16))
# Shoji lattices, hanging bamboo blinds, eave brackets and entrance stairs.
for level in range(3):
 z=.65+level*1.35; w=2.6-level*.5; d=2.15-level*.4
 for dx in [-.6,0,.6]:
  xx=px+dx*(w/2); yy=py-d/2-.045
  cube('Shoji luminous paper',(xx,yy,z+.48),(.255,.025,.56),ivory)
  for off in [-.11,0,.11]: cube('Shoji vertical lattice',(xx+off,yy-.025,z+.48),(.018,.025,.58),wood)
  for off in [-.25,-.08,.09,.25]: cube('Shoji horizontal lattice',(xx,yy-.03,z+.48+off),(.27,.025,.018),wood)
  for n in range(5): cube('Bamboo window shade',(xx,yy-.08,z+.83-n*.032),(.34,.055,.02),bamboo)
  beam('Shade pull cord',(xx+.17,yy-.085,z+.83),(xx+.17,yy-.085,z+.4),.007,wood)
 for dx in [-w/2,w/2]: cube('Eave bracket',(px+dx,py-d/2,z+.87),(.3,.3,.12),wood)
for j in range(4): cube('Temple entrance step',(2.5,.08-j*.19,.52-j*.045),(1.4,.24,.14),stone)
# Lotus leaves with a characteristic wedge, and flowers made from layered petals.
for idx,(x,y) in enumerate([(-3.5,-1.9),(-2.7,-2.9),(1,-3.05),(3.7,-1.35),(3.4,-2.45),(-.8,-3)]):
 verts=[(x,y,.665)]+[(x+.38*math.cos(t),y+.34*math.sin(t),.67) for t in [(.22+i/24*(math.tau-.44)) for i in range(25)]]
 mesh('Lotus leaf',verts,[(0,i,i+1) for i in range(1,25)],leaf)
 if idx%2==0:
  for ring in range(2):
   for j in range(7):
    t=j*math.tau/7+ring*.4; p=ico('Lotus flower petal',(x+math.cos(t)*(.13-ring*.06),y+math.sin(t)*(.13-ring*.06),.74+ring*.08),(.17,.065,.055),pinks[(j+1)%4],2);p.rotation_euler=(0,-.35-ring*.3,t)
  ico('Lotus pollen heart',(x,y,.84),(.065,.065,.05),gold,2)
# Koi roots are preserved for swimming animation in Three.js.
for i in range(6):
 before=set(bpy.data.objects)
 ico('Koi body',(0,0,0),(.10,.30,.07),ivory,2)
 ico('Koi head',(0,-.24,.01),(.09,.09,.065),ivory,2)
 for yy in [-.12,.06,.17]: ico('Koi red patch',(.015,yy,.052),(.075,.07,.025),orange,1)
 for x in [-.075,.075]: ico('Koi eye',(x,-.265,.045),(.015,.02,.012),black,2)
 mesh('Koi tail',[(-.14,.42,0),(0,.23,0),(.14,.42,0),(0,.36,.025)],[(0,1,3),(1,2,3)],orange)
 for s in [-1,1]: mesh('Koi fin',[(s*.07,-.08,0),(s*.19,.06,-.015),(s*.07,.08,0)],[(0,1,2)],ivory)
 parts=set(bpy.data.objects)-before; root=bpy.data.objects.new('Koi_'+str(i),None);bpy.context.collection.objects.link(root)
 for o in parts:o.parent=root
 a=i*math.tau/6;root.location=(math.cos(a)*3.6,-1.1+math.sin(a)*1.45,.70);root.rotation_euler.z=a
# A watchful cat on the bank, with an animated tail pivot.
before=set(bpy.data.objects)
ico('Cat body',(0,0,.25),(.22,.30,.36),catmat,2);ico('Cat chest',(0,-.16,.29),(.16,.13,.24),ivory,2)
ico('Cat head',(0,-.1,.65),(.235,.21,.22),catmat,2)
for x in [-.14,.14]:
 mesh('Cat pointed ear',[(x-.085,-.12,.76),(x+.085,-.12,.76),(x,-.08,1.0),(x,.04,.77)],[(0,1,2),(1,3,2),(3,0,2)],catmat)
 mesh('Cat inner ear',[(x-.045,-.125,.79),(x+.045,-.125,.79),(x,-.09,.92)],[(0,1,2)],pink)
 ico('Cat bright eye',(x*.7,-.292,.69),(.035,.018,.045),leaf,2);ico('Cat pupil',(x*.7,-.31,.69),(.009,.008,.031),black)
 ico('Cat paw',(x,-.23,.05),(.09,.12,.07),ivory,2)
ico('Cat muzzle',(0,-.29,.58),(.10,.05,.065),ivory,2);ico('Cat nose',(0,-.34,.62),(.025,.015,.019),pink)
for side in [-1,1]:
 for j in range(3):beam('Cat whisker',(side*.04,-.33,.58),(side*.28,-.32,.56+j*.025),.003,ivory)
parts=set(bpy.data.objects)-before;cat=bpy.data.objects.new('GardenCat',None);bpy.context.collection.objects.link(cat)
for o in parts:o.parent=cat
cat.location=(2.4,-3.65,.35);cat.rotation_euler.z=-.5
tail=bpy.data.objects.new('CatTail',None);bpy.context.collection.objects.link(tail);tail.parent=cat;tail.location=(0,.20,.15)
for j in range(8):
 t=j/7; o=ico('Cat tail segment',(.38*math.sin(t*2),t*.4,t*.34),(.07,.09,.07),catmat,2);o.parent=tail
# Fallen sakura, grass tufts, garden bamboo and a small stone path.
for i in range(75):
 x=random.uniform(-6,6);y=random.uniform(-4,3.5)
 if (x/5.6)**2+((y+1.1)/2.7)**2<1:continue
 o=ico('Fallen sakura petal',(x,y,.42),(.045,.075,.014),random.choice(pinks));o.rotation_euler.z=random.random()*math.tau
for x,y in [(-5.8,1.1),(5.7,2.1),(-2.3,3.7)]:
 for k in range(4):
  xx=x+k*.16;h=1.2+random.random()*.7;beam('Bamboo stem',(xx,y,.3),(xx,y,h),.035,leaf)
  for z in [.6,.95,1.3]:
   beam('Bamboo node',(xx,y,z),(xx,y,z+.03),.05,bamboo)
   ico('Bamboo leaf',(xx+.16,y,z),(.27,.055,.03),leaf)
# Preview ripple rings are also saved to Blender; web animates their scale.
for i,(x,y) in enumerate([(-3.2,-.6),(.3,-2.6),(3.5,-1.5),(-1.3,-3.0),(1.5,-2.6)]):
 vs=[]
 for j in range(48):
  a=j/48*math.tau
  for r in [.27,.28]:vs.append((r*math.cos(a),r*math.sin(a),0))
 o=mesh('Ripple_'+str(i),vs,[(2*j,2*j+1,(2*j+3)%96,(2*j+2)%96) for j in range(48)],ripplemat);o.location=(x,y,.665)
# Preview animation is editable in Blender too. Runtime uses its own lightweight animation.
for i in range(6):
 root=bpy.data.objects.get('Koi_'+str(i))
 for frame in range(1,242,20):
  a=i*math.tau/6+(frame-1)/240*math.tau
  root.location=(math.cos(a)*(3.0+i*.12),-1.1-math.sin(a)*(1.55+i*.025),.70)
  root.rotation_euler.z=a;root.keyframe_insert(data_path='location',frame=frame);root.keyframe_insert(data_path='rotation_euler',frame=frame)
for frame in range(1,242,10):
 tail.rotation_euler.y=math.sin(frame*.12)*.2;tail.keyframe_insert(data_path='rotation_euler',frame=frame)
for i in range(36):
 x=random.uniform(-6,6);y=random.uniform(-3,3);z=random.uniform(2,5)
 o=ico('FallingPetal_'+str(i),(x,y,z),(.045,.075,.013),random.choice(pinks),1)
 o.keyframe_insert(data_path='location',frame=1);o.keyframe_insert(data_path='rotation_euler',frame=1)
 o.location=(x+1.5,y+.3,.6);o.rotation_euler=(2.4,1.8,3.2);o.keyframe_insert(data_path='location',frame=240);o.keyframe_insert(data_path='rotation_euler',frame=240)
bpy.context.scene.frame_end=240;bpy.context.scene.frame_set(1)
# Daylight and camera remain in the editable Blender file.
bpy.ops.object.light_add(type='AREA', location=(-3,-4,10)); bpy.context.object.data.energy=1800; bpy.context.object.data.shape='DISK'; bpy.context.object.data.size=8
bpy.ops.object.camera_add(location=(11,-16,12)); cam=bpy.context.object; cam.rotation_euler=(Vector((0,0,1))-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.type='ORTHO'; cam.data.ortho_scale=19
sc=bpy.context.scene; sc.camera=cam; sc.world.color=(.35,.35,.35); sc.render.resolution_x=1500; sc.render.resolution_y=1200; sc.render.resolution_percentage=100
sc['README']='Ivan Digital Garden. Editable original meshes. Export assets/garden.glb after edits. Web day/night lighting lives in scene.js.'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','Ivan-Japanese-Garden.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT,'assets','garden.glb'),export_format='GLB',export_cameras=False,export_lights=False,export_animations=False)
print('GARDEN_SAVED',len(sc.objects))
