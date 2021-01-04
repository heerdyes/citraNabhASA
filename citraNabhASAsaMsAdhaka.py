'''
language: citraNabhASA
translates citr files into java
'''

import sys
import os
from kramAdezotpAdaka.jgenlib import *

if len(sys.argv)!=3:
  print('usage: python3 citraNabhASAsaMsAdhaka.py <program.citr> <gendir>')
  raise SystemExit


# fndecl
def eattillspace(s):
  sploc=s.find(' ')
  if sploc==-1:
    return s,''
  else:
    scar=s[0:sploc]
    scdr=s[sploc+1:]
    return scar,scdr

# translate line
def anuvadatu(ln):
  cmd,argstr=eattillspace(ln)
  args=argstr.split(' ')
  genstmt=[]
  if cmd=='fill':
    rgba=args
    if len(rgba)==3:
      genstmt.append('gc.setFill(Color.rgb(%s,%s,%s));'%(rgba[0],rgba[1],rgba[2]))
    elif len(rgba)==4:
      genstmt.append('gc.setFill(Color.rgb(%s,%s,%s,%s));'%(rgba[0],rgba[1],rgba[2],rgba[3]))
    else:
      print('[error] %s'%ln)
      raise Exception('unsupported rgba array length: %d'%len(rgba))
  elif cmd=='stroke':
    rgba=args
    if len(rgba)==3:
      genstmt.append('gc.setStroke(Color.rgb(%s,%s,%s));'%(rgba[0],rgba[1],rgba[2]))
    elif len(rgba)==4:
      genstmt.append('gc.setStroke(Color.rgb(%s,%s,%s,%s));'%(rgba[0],rgba[1],rgba[2],rgba[3]))
    else:
      print('[error] %s'%ln)
      raise Exception('unsupported rgba array length: %d'%len(rgba))
  elif cmd=='rect':
    xywh=args
    genstmt.append('gc.strokeRect(%s,%s,%s,%s);'%(xywh[0],xywh[1],xywh[2],xywh[3]))
  elif cmd=='fillrect':
    genstmt.append('gc.fillRect(%s,%s,%s,%s);'%(args[0],args[1],args[2],args[3]))
  elif cmd=='p':
    genstmt.append('System.out.println(%s);'%argstr)
  elif cmd=='v':
    genstmt.append('var %s;'%argstr)
  elif cmd=='j':
    genstmt.append('%s;'%argstr)
  elif cmd=='line':
    xypq=args
    genstmt.append('gc.strokeLine(%s,%s,%s,%s);'%(xypq[0],xypq[1],xypq[2],xypq[3]))
  elif cmd=='inc':
    v,dv=args[0],args[1]
    genstmt.append('%s=%s+%s;'%(v,v,dv))
  elif cmd=='size':
    sw,sh=args[0],args[1]
    genstmt.append('c=new Canvas(%s,%s);'%(sw,sh))
    genstmt.append('gc=c.getGraphicsContext2D();')
  elif cmd=='oval':
    px,py,pw,ph=args[0],args[1],args[2],args[3]
    genstmt.append('gc.strokeOval(%s,%s,%s,%s);'%(px,py,pw,ph))
  elif cmd=='filloval':
    px,py,pw,ph=args[0],args[1],args[2],args[3]
    genstmt.append('gc.fillOval(%s,%s,%s,%s);'%(px,py,pw,ph))
  elif cmd=='frameinterval':
    genstmt.append('protected long frameinterval=%s;'%argstr)
  elif cmd=='exit':
    genstmt.append('System.exit(0);')
  else:
    print('[anuvadatu] unknown cmd: %s'%cmd)
    genstmt.append('// non-translatable line: %s'%ln)
  return genstmt

def slurpfile(flnm):
  prog=None
  with open(citrfn) as fc:
    try:
      prog=fc.readlines()
    except Exception as e:
      print('problem: %s'%str(e))
  return prog

def procnode(jtarget,staq,line):
  kword=line[1:-1]
  if kword=='end':
    topel=staq.pop()
    if topel.__class__==Jmethod:
      jtarget.methods.append(topel)
    elif topel.__class__==Jif:
      ifblk=topel.stmtgen()
      outermeth=staq[-1]
      if outermeth.__class__!=Jmethod:
        raise Exception('citraNabhASA does not yet support nested blocks!')
      outermeth.statements+=ifblk
    else:
      print('dumping staq:')
      print(staq)
      raise Exception('inner element is neither Jmethod nor Jif!')
  elif kword.startswith('if '):
    iftok,cond=eattillspace(kword)
    ifgen=Jif(cond)
    staq.append(ifgen)
  else:
    mgen=Jmethod(kword)
    if kword=='keyPressed':
      mgen.parameters.append('KeyEvent e')
      mgen.statements.append('String key=e.getCharacter();')
      mgen.statements.append('KeyCode keyCode=e.getCode();')
    staq.append(mgen)

# process the program
def procprog(prog,jtarget):
  staq=[]
  for rawline in prog:
    line=rawline.strip()
    if line=='' or line.startswith('#'):
      continue
    if line.startswith('['):
      procnode(jtarget,staq,line)
    else:
      stmts=anuvadatu(line)
      if len(staq)>0:
        for stmt in stmts:
          staq[-1].statements.append(stmt)
      else:
        jtarget.vardecls+=stmts

# generate the abstract class structure
def genmaincls(prog,clsnm):
  jtarget=Jclass(clsnm)
  jtarget.modifiers.append('public')
  jtarget.setparent('Application')
  jtarget.vardecls+=j_vardecls()
  jtarget.methods+=[
    j_d(),
    j_setupMouseSensor(),
    j_setupKeyboardSensor(),
    j_info(),
    j_start()
  ]
  # translating from .citr program
  procprog(prog,jtarget)
  if not jtarget.hasmethod('mousePressed'):
    jtarget.methods.append(j_mousePressed())
  if not jtarget.hasmethod('mouseReleased'):
    jtarget.methods.append(j_mouseReleased())
  if not jtarget.hasmethod('mouseMoved'):
    jtarget.methods.append(j_mouseMoved())
  if not jtarget.hasmethod('mouseDragged'):
    jtarget.methods.append(j_mouseDragged())
  if not jtarget.hasmethod('keyPressed'):
    jtarget.methods.append(j_keyPressed())
  jtarget.methods.append(j_main())
  return jtarget

# generate the java compilation unit
def genfile(prog,clsnm):
  jf=Jfile(clsnm)
  jf.imports+=j_FXImports()
  jf.classes.append(j_kAlapAlaka(clsnm))
  jf.classes.append(genmaincls(prog,clsnm))
  return jf

# fndecl end


# flow
citrfn=sys.argv[1]
gendir=sys.argv[2]
if not citrfn.endswith('.citr'):
  print('this program only eats *.citr files')
  raise SystemExit
print('processing file: %s'%citrfn)

prog=slurpfile(citrfn)
jcls=citrfn.split('.')[0]
print('generating class syntax object')
jgencode=genfile(prog,jcls)

with open('%s%s%s.java'%(gendir,os.sep,jcls),'w') as fgen:
  print('generating file: %s.java'%jcls)
  jgencode.codegen(fgen)
