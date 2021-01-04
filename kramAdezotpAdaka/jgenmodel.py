'''
abstraction of a java class file
'''
class Jfile:
  def __init__(self,fnm):
    self.nm=fnm
    self.imports=[]
    self.classes=[]
  
  def codegen(self,fh):
    for i in self.imports:
      print(i,file=fh)
    print('',file=fh)
    for c in self.classes:
      c.codegen(fh)


'''
rudimentary class abstraction for a java class
'''
class Jclass:
  def __init__(self,clsnm):
    self.nm=clsnm
    self.modifiers=[]
    self.constructors=[]
    self.inherits=''
    self.vardecls=[]
    self.methods=[]
  
  def modifstr(self):
    return ' '.join(self.modifiers) + ('' if len(self.modifiers)==0 else ' ')
    
  def setparent(self,clsnm):
    self.inherits='' if clsnm=='' else ' extends '+clsnm
  
  def hasmethod(self,mname):
    for m in self.methods:
      if mname==m.nm:
        return True
    return False
  
  def codegen(self,fh):
    elems=(self.modifstr(),self.nm,self.inherits)
    print('%sclass %s%s{'%elems,file=fh)
    for v in self.vardecls:
      print('  %s'%v,file=fh)
    print('',file=fh)
    for c in self.constructors:
      c.codegen(fh)
      print('',file=fh)
    for m in self.methods:
      m.codegen(fh)
      print('',file=fh)
    print('}',file=fh)


'''
rudimentary java method abstraction
'''
class Jmethod:
  def __init__(self,mthnm):
    self.nm=mthnm
    self.modifiers=[]
    self.returntype='void'
    self.annotations=[]
    self.parameters=[]
    self.statements=[]
  
  def modifstr(self):
    return ' '.join(self.modifiers) + ('' if len(self.modifiers)==0 else ' ')
  
  def codegen(self,fh):
    for a in self.annotations:
      print('  %s'%a,file=fh)
    elems=(self.modifstr(),self.returntype,self.nm,','.join(self.parameters))
    print('  %s%s %s(%s){'%elems,file=fh)
    for s in self.statements:
      print('    %s'%(s),file=fh)
    print('  }',file=fh)


class Jif:
  def __init__(self,cond):
    self.cond=cond
    self.statements=[]
    
  def codegen(self,fh):
    print('    if (%s) {'%self.cond,file=fh)
    for s in self.statements:
      print('      %s'%(s),file=fh)
    print('    }',file=fh)
    
  def stmtgen(self):
    sb=[]
    sb.append('if (%s) {'%self.cond)
    for s in self.statements:
      sb.append('  %s'%(s))
    sb.append('}')
    return sb


'''
java constructor abstraction
'''
class Jctor:
  def __init__(self,clsnm):
    self.nm=clsnm
    self.modifiers=[]
    self.parameters=[]
    self.statements=[]
    
  def modifstr(self):
    return ' '.join(self.modifiers) + ('' if len(self.modifiers)==0 else ' ')
  
  def codegen(self,fh):
    elems=(self.modifstr(),self.nm,','.join(self.parameters))
    print('  %s%s(%s){'%elems,file=fh)
    for s in self.statements:
      print('    %s'%(s),file=fh)
    print('  }',file=fh)
    
