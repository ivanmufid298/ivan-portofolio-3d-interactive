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
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.scale=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if min(scale)>.045:
  mod=o.modifiers.new('Soft crafted edges','BEVEL');mod.width=min(.045,min(scale)*.15);mod.segments=1
  bpy.ops.object.modifier_apply(modifier=mod.name)
 return finish(o,name,material)
def ico(name,loc,scale,material,sub=1):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc); o=bpy.context.object; o.scale=scale
 for p in o.data.polygons:p.use_smooth=name.startswith('Koi')
 return finish(o,name,material)
def beam(name,a,b,r,material):
 d=Vector(b)-Vector(a); bpy.ops.mesh.primitive_cylinder_add(vertices=8,radius=r,depth=d.length,location=(Vector(a)+Vector(b))/2); o=bpy.context.object; o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
 for p in o.data.polygons:p.use_smooth=len(p.vertices)==4
 return finish(o,name,material)
def mesh(name,vs,fs,material):
 m=bpy.data.meshes.new(name); m.from_pydata(vs,[],fs); m.update(); o=bpy.data.objects.new(name,m); bpy.context.collection.objects.link(o); o.data.materials.append(material); return o
# A deliberately sculpted floating garden. Blender Z becomes web Y on export.
ico('Floating garden foundation',(0,0,-.75),(7.6,5.8,1.6),earth,2)
cube('Garden level lawn',(0,0,.16),(12,9,.48),grass)
ico('Moss garden edge',(0,0,-.23),(7.45,5.7,.65),grass,2)
wp=next(n for n in water.node_tree.nodes if n.type=='BSDF_PRINCIPLED');wp.inputs['Roughness'].default_value=.2;wp.inputs['Alpha'].default_value=.78
water.surface_render_method='DITHERED'
pondverts=[(0,-1.1,.65)]+[(2.28*math.cos(i*math.tau/96),-1.1+2.52*math.sin(i*math.tau/96),.65) for i in range(97)]
mesh('Koi pond',pondverts,[(0,i+1,i+2) for i in range(96)],water)
mesh('Pond submerged bed',[(x,y,.425) for x,y,z in pondverts],[(0,i+1,i+2) for i in range(96)],mat('Pond depth teal',(.10,.28,.27)))
stones=[mat('River stone '+str(i),c) for i,c in enumerate([(.42,.45,.40),(.58,.57,.49),(.33,.39,.37),(.64,.62,.54),(.46,.50,.47)])]
for i in range(42):
 t=i/42*math.tau; x=2.42*math.cos(t); y=-1.1+2.66*math.sin(t)
 if abs(y+1.2)<.8 and abs(x)>2.1:continue
 o=ico('Pond riverstone',(x,y,.52),(random.uniform(.14,.40),random.uniform(.16,.35),random.uniform(.10,.28)),random.choice(stones));o.rotation_euler=(random.random()*.4,random.random()*.3,random.random()*6)
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
for x,y,s in [(-5.5,3.2,.85),(-1.2,3.4,1.05),(5,2.7,.95),(-5.7,-3.4,.65)]:
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
# Connected gravel paths lead from torii to the west bridge landing and from east landing to temple.
gravel=mat('Sand garden path',(.65,.60,.46))
routes=[((-3.6,1.8),(-3.6,-1.2)),((-3.6,-1.2),(-2.25,-1.2)),((2.25,-1.2),(3.5,-1.2)),((3.5,-1.2),(3.5,.1)),((3.5,.1),(2.5,.1))]
for (ax,ay),(bx,by) in routes:
 dx=bx-ax;dy=by-ay;length=math.hypot(dx,dy);o=cube('Connected gravel walkway',((ax+bx)/2,(ay+by)/2,.445),(length+.2,.95,.09),gravel);o.rotation_euler.z=math.atan2(dy,dx)
 for j in range(max(2,int(length/.38))):
  t=j/max(1,int(length/.38)-1);o=cube('Walkway stone',(ax+dx*t,ay+dy*t,.51),(.30,.53,.07),random.choice(stones));o.rotation_euler.z=math.atan2(dy,dx)+random.uniform(-.12,.12)
for x in [-2.38,2.38]:cube('Bridge bank abutment',(x,-1.2,.52),(.65,1.5,.26),stone)
# Small living details, all editable in the source file.
ivory=mat('Koi porcelain',(.95,.88,.72)); orange=mat('Koi vermilion',(.90,.20,.055)); black=mat('Ink',(.022,.028,.025)); leaf=mat('Lotus jade',(.12,.32,.16)); gold=mat('Flower pollen',(.98,.61,.12)); ripplemat=mat('Ripple foam',(.56,.79,.73)); bamboo=mat('Bamboo shade',(.47,.32,.16))
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
for idx,(x,y) in enumerate([(-1.4,-2.4),(-.7,-3.0),(1,-2.95),(1.5,-.2),(.8,.65),(-.8,-.1)]):
 verts=[(x,y,.665)]+[(x+.38*math.cos(t),y+.34*math.sin(t),.67) for t in [(.22+i/24*(math.tau-.44)) for i in range(25)]]
 mesh('Lotus leaf',verts,[(0,i,i+1) for i in range(1,25)],leaf)
 if idx%2==0:
  for ring in range(2):
   for j in range(7):
    t=j*math.tau/7+ring*.4; p=ico('Lotus flower petal',(x+math.cos(t)*(.13-ring*.06),y+math.sin(t)*(.13-ring*.06),.74+ring*.08),(.17,.065,.055),pinks[(j+1)%4],2);p.rotation_euler=(0,-.35-ring*.3,t)
  ico('Lotus pollen heart',(x,y,.84),(.065,.065,.05),gold,2)
# Koi roots are preserved for swimming animation in Three.js.
for i in range(14):
 before=set(bpy.data.objects)
 body=ico('Koi streamlined body',(0,0,0),(.105,.34,.075),ivory,2)
 body.data.materials.append(orange);body.data.materials.append(black)
 for p in body.data.polygons:
  c=p.center
  if c.z>.25 and ((-.62<c.y<-.15 and c.x>-.5) or (.15<c.y<.55 and c.x<.65)):p.material_index=1
  if i%3==0 and c.z>.35 and c.y>.6:p.material_index=2
 ico('Koi head',(0,-.285,0),(.086,.105,.06),ivory,2)
 for x in [-.072,.072]:ico('Koi eye',(x,-.31,.025),(.012,.016,.012),black,2)
 for s in [-1,1]:
  o=ico('Koi translucent pectoral fin',(s*.11,-.07,-.018),(.09,.12,.012),ivory,2);o.rotation_euler.z=s*.6
 tailfin=mesh('KoiTail_'+str(i),[(-.12,.18,0),(-.05,.08,.015),(0,0,0),(.05,.08,.015),(.12,.18,0),(0,.13,0)],[(0,1,2,5),(2,3,4,5)],orange);tailfin.location=(0,.27,0)
 parts=set(bpy.data.objects)-before; root=bpy.data.objects.new('Koi_'+str(i),None);bpy.context.collection.objects.link(root)
 for o in parts:o.parent=root
 a=i*math.tau/14;root.location=(math.cos(a)*1.5,-1.1+math.sin(a)*1.8,.535);root.rotation_euler.z=a
# Fallen sakura, grass tufts, garden bamboo and a small stone path.
for i in range(75):
 x=random.uniform(-6,6);y=random.uniform(-4,3.5)
 if (x/5.6)**2+((y+1.1)/2.7)**2<1:continue
 o=ico('Fallen sakura petal',(x,y,.42),(.045,.075,.014),random.choice(pinks));o.rotation_euler.z=random.random()*math.tau
for x,y in [(-5.8,2.3),(5.5,1.0),(-2.5,4.0),(.1,4.0),(5.3,-2.8)]:
 for k in range(7):
  xx=x+random.uniform(-.35,.35);yy=y+random.uniform(-.3,.3);h=random.uniform(1.8,3.1)
  beam('Bamboo stem',(xx,yy,.4),(xx+.09,yy,h),.045,leaf)
  for j in range(1,6):
   z=.45+j*(h-.5)/6;beam('Bamboo node',(xx,yy,z),(xx,yy,z+.035),.056,bamboo)
   if j<3:continue
   side=(-1)**j;beam('Bamboo twig',(xx,yy,z),(xx+side*.3,yy+.08,z+.13),.013,leaf)
   for q in range(3):
    o=ico('Bamboo lance leaf',(xx+side*(.16+q*.1),yy+.08,z+.13),(.21,.045,.018),leaf);o.rotation_euler.z=side*(.3+q*.4)
# A curved stepping-stone approach remains clear of the pond and torii posts.
for j in range(10):
 t=j/9;x=-3.6+1.5*math.sin(t*1.6);y=-1.9-t*2.35
 o=ico('Approach stepping stone',(x,y,.46),(.31+random.random()*.06,.24,.075),stones[j%5],1);o.rotation_euler.z=random.random()

# Preview ripple rings are also saved to Blender; web animates their scale.
for i,(x,y) in enumerate([(-1.3,-.6),(.3,-2.6),(1.5,-1.5),(-1.3,-2.8),(1.5,-2.6)]):
 vs=[]
 for j in range(48):
  a=j/48*math.tau
  for r in [.27,.28]:vs.append((r*math.cos(a),r*math.sin(a),0))
 o=mesh('Ripple_'+str(i),vs,[(2*j,2*j+1,(2*j+3)%96,(2*j+2)%96) for j in range(48)],ripplemat);o.location=(x,y,.665)
# Lush green trees and irregular banks balance the sakura canopy.
greens=[mat('Evergreen '+str(i),c) for i,c in enumerate([(.10,.27,.18),(.17,.36,.21),(.29,.43,.23),(.23,.38,.28)])]
for x,y,s in [(5,0,1),(-5.85,-1.2,.65),(4.4,3.8,1.1),(-3.7,3.5,.9)]:
 beam('Green tree trunk',(x,y,.4),(x,y,2.0*s),.12,wood)
 for j in range(8):
  a=j*2.4;ico('Green tree canopy',(x+math.cos(a)*.45*s,y+math.sin(a)*.4*s,(1.8+j*.075)*s),(.65*s,.60*s,.55*s),greens[j%4],2)
for i in range(28):
 a=i*math.tau/28;x=3.2*math.cos(a);y=-1.1+3.25*math.sin(a)
 if abs(y+1.2)<.9 or (x>1 and y>0):continue
 ico('Bank shrub',(x,y,.57),(random.uniform(.25,.50),random.uniform(.25,.4),random.uniform(.22,.5)),random.choice(greens),2)
 for j in range(3):ico('Shrub small leaf mass',(x+random.uniform(-.25,.25),y+random.uniform(-.2,.2),.78),(.15,.16,.2),random.choice(greens),1)
# Japanese bamboo water feature: stone basin, hollow spout and rocking shishi-odoshi.
fx,fy=2.95,-2.75
ico('Fountain foundation',(fx,fy,.48),(.72,.60,.16),stones[2],2)
bpy.ops.mesh.primitive_torus_add(major_segments=24,minor_segments=8,location=(fx,fy,.72),major_radius=.42,minor_radius=.13);finish(bpy.context.object,'Tsukubai stone basin',stones[1])
ico('Fountain basin water',(fx,fy,.70),(.39,.39,.025),water,2)
for x in [fx-.22,fx+.22]:beam('Fountain bamboo support',(x,fy+.3,.45),(x,fy+.3,1.55),.065,bamboo)
beam('Fountain bamboo upright',(fx,fy+.48,.45),(fx,fy+.48,1.9),.085,bamboo)
beam('Fountain bamboo spout',(fx,fy+.48,1.85),(fx,fy,1.85),.075,bamboo)
ico('Bamboo hollow mouth',(fx,fy-.005,1.85),(.052,.013,.052),black,2)
beam('FountainStream',(fx,fy,1.80),(fx,fy,1.17),.016,water)
pivot=bpy.data.objects.new('BambooRocker',None);bpy.context.collection.objects.link(pivot);pivot.location=(fx,fy,1.13)
o=beam('Rocking bamboo tube',(0,-.32,0),(0,.38,0),.095,bamboo);o.parent=pivot
o=ico('Bamboo receiver hollow',(0,-.326,0),(.071,.012,.071),black,2);o.parent=pivot
beam('Fountain outlet trickle',(fx,fy-.32,1.12),(fx,fy-.32,.72),.012,water)
# Sky objects are world-space geometry. They are never parented to the camera.
sunmat=mat('Sun warm glow',(1,.75,.35),1.5);moonmat=mat('Moon ivory glow',(.77,.87,1),1.1)
ico('SkySun',(-6,20,6.6),(1.1,1.1,1.1),sunmat,3)
ico('SkyMoon',(-6,20,6.6),(.8,.8,.8),moonmat,3)
cloudmat=mat('Cloud soft white',(.92,.95,.90))
for i,(x,y,z) in enumerate([(-11,15,7),(1,18,8),(12,15,7),(-18,7,8)]):
 for j in range(5):ico('SkyCloud_'+str(i),(x+j*.7,y+math.sin(j)*.4,z+math.sin(j*.7)*.3),(1.3,.65,.5),cloudmat,2)
# Preview animation is editable in Blender too. Runtime uses its own lightweight animation.
for i in range(14):
 root=bpy.data.objects.get('Koi_'+str(i))
 for frame in range(1,242,20):
  a=i*math.tau/14+(frame-1)/240*math.tau*(.8+i*.035)
  rx=1.0+(i%4)*.2;ry=1.25+(i%5)*.15;root.location=(math.cos(a)*rx,-1.1-math.sin(a)*ry,.535)
  root.rotation_euler.z=math.atan2(-rx*math.sin(a),ry*math.cos(a));root.keyframe_insert(data_path='location',frame=frame);root.keyframe_insert(data_path='rotation_euler',frame=frame)
for frame in range(1,242,10):
 pivot.rotation_euler.x=max(0,math.sin(frame*.03))*.45;pivot.keyframe_insert(data_path='rotation_euler',frame=frame)
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
for i,(name,pos,aim) in enumerate([('Torii',(-2.6,4.4,9),(-3.6,1.85,-.8)),('Bridge',(6.4,5.7,8.8),(0,1.1,1.2)),('Pond',(3.8,6.8,6.8),(.4,.65,1.65)),('Temple',(8.5,5.4,7.4),(2.5,2.6,-1.6))]):
 bpy.ops.object.camera_add(location=(pos[0],-pos[2],pos[1]));shot=bpy.context.object;shot.name='View_'+str(i+1)+'_'+name;shot.data.lens=45;shot.rotation_euler=(Vector((aim[0],-aim[2],aim[1]))-shot.location).to_track_quat('-Z','Y').to_euler();marker=sc.timeline_markers.new(name,frame=1+i*60);marker.camera=shot
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','Ivan-Japanese-Garden.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT,'assets','garden.glb'),export_format='GLB',export_cameras=False,export_lights=False,export_animations=False)
print('GARDEN_SAVED',len(sc.objects))
