from kramAdezotpAdaka.jgenmodel import *

def j_d():
  md=Jmethod('d')
  md.parameters.append('String msg')
  md.statements.append('System.out.printf("[%s] %s%n",dlevel,msg);');
  return md

def j_setupMouseSensor():
  msms=Jmethod('setupMouseSensor')
  smsbody='''if(c==null){
  throw new RuntimeException("canvas found to be null!");
}
c.addEventHandler(MouseEvent.MOUSE_PRESSED,
  new EventHandler<MouseEvent>(){
    @Override
    public void handle(MouseEvent e){
      mousePressed(e);
    }
  }
);
c.addEventHandler(MouseEvent.MOUSE_RELEASED,
  new EventHandler<MouseEvent>(){
    @Override
    public void handle(MouseEvent e){
      mouseReleased(e);
    }
  }
);
c.addEventHandler(MouseEvent.MOUSE_MOVED,
  new EventHandler<MouseEvent>(){
    @Override
    public void handle(MouseEvent e){
      mouseMoved(e);
    }
  }
);
c.addEventHandler(MouseEvent.MOUSE_DRAGGED,
  new EventHandler<MouseEvent>(){
    @Override
    public void handle(MouseEvent e){
      mouseDragged(e);
    }
  }
);
c.setFocusTraversable(true);'''
  stmtseq=smsbody.split('\n')
  msms.statements+=stmtseq
  return msms

def j_setupKeyboardSensor():
  msks=Jmethod('setupKeyboardSensor')
  msks.statements.append('s.setOnKeyPressed(e->keyPressed(e));')
  return msks

def j_info():
  mi=Jmethod('info')
  mibody='''String javaVersion=System.getProperty("java.version");
String javafxVersion=System.getProperty("javafx.version");
d("[java] "+javaVersion);
d("[javafx] "+javafxVersion);
if(javaVersion==null || javafxVersion==null){
  throw new RuntimeException("java or javafx version is empty!");
}'''
  stmtseq=mibody.split('\n')
  mi.statements+=stmtseq
  return mi

def j_start():
  ms=Jmethod('start')
  ms.annotations.append('@Override')
  ms.modifiers.append('public')
  ms.parameters.append('Stage stage')
  msbody='''info();
setup();
Group root=new Group();
root.getChildren().add(c);
s=new Scene(root);
setupMouseSensor();
setupKeyboardSensor();
kAlapAlaka kp=new kAlapAlaka(this,frameinterval);
Timer t=new Timer();
t.scheduleAtFixedRate(kp,kp.T,kp.T);
stage.initStyle(StageStyle.UNDECORATED);
stage.setScene(s);
stage.show();'''
  stmtseq=msbody.split('\n')
  ms.statements+=stmtseq
  return ms
  
def j_keyPressed():
  mkp=Jmethod('keyPressed')
  mkp.parameters.append('KeyEvent e')
  mkpbody='''KeyCode kc=e.getCode();
d(kc.toString());
if(kc.equals(KeyCode.ESCAPE)){
  d("exiting...");
  System.exit(0);
}'''
  stmtseq=mkpbody.split('\n')
  mkp.statements+=stmtseq
  return mkp
  
def j_main():
  mm=Jmethod('main')
  mm.modifiers+=['public','static']
  mm.returtype='void'
  mm.parameters.append('String[] args')
  mm.statements.append('launch();')
  return mm

def j_mousePressed():
  mmp=Jmethod('mousePressed')
  mmp.parameters.append('MouseEvent e')
  return mmp

def j_mouseReleased():
  mmp=Jmethod('mouseReleased')
  mmp.parameters.append('MouseEvent e')
  return mmp

def j_mouseMoved():
  mmp=Jmethod('mouseMoved')
  mmp.parameters.append('MouseEvent e')
  return mmp

def j_mouseDragged():
  mmp=Jmethod('mouseDragged')
  mmp.parameters.append('MouseEvent e')
  return mmp

def j_kpctor(maincls):
  kpc=Jctor('kAlapAlaka')
  kpc.parameters+=[
    '%s mref'%maincls,
    'long millis'
  ]
  kpc.statements+=[
    'this.mref=mref;',
    'T=millis;'
  ]
  return kpc

def j_kprun():
  kpr=Jmethod('run')
  kpr.modifiers.append('public')
  kpr.returntype='void'
  kpr.statements.append('mref.draw();')
  return kpr

def j_kAlapAlaka(maincls):
  gk=Jclass('kAlapAlaka')
  gk.setparent('TimerTask')
  gk.vardecls+=[
    '%s mref;'%maincls,
    'long T;'
  ]
  gk.constructors.append(j_kpctor(maincls))
  gk.methods.append(j_kprun())
  return gk

def j_FXImports():
  return [
    'import java.io.*;',
    'import java.awt.image.RenderedImage;',
    'import javax.imageio.ImageIO;',
    'import javafx.application.Application;',
    'import javafx.scene.Scene;',
    'import javafx.scene.canvas.Canvas;',
    'import javafx.scene.canvas.GraphicsContext;',
    'import javafx.scene.paint.Color;',
    'import javafx.stage.Stage;',
    'import javafx.stage.StageStyle;',
    'import javafx.scene.Group;',
    'import javafx.scene.input.MouseEvent;',
    'import javafx.scene.input.KeyEvent;',
    'import javafx.event.EventHandler;',
    'import javafx.scene.input.KeyCode;',
    'import javafx.scene.image.WritableImage;',
    'import javafx.embed.swing.SwingFXUtils;',
    'import java.util.List;',
    'import java.util.ArrayList;',
    'import java.util.Timer;',
    'import java.util.TimerTask;',
    'import static java.lang.Math.sqrt;',
    'import static java.lang.Math.sin;',
    'import static java.lang.Math.cos;',
    'import static java.lang.Math.pow;',
    'import static java.lang.Math.abs;',
    'import static java.lang.Math.log;',
    'import static java.lang.Math.exp;'
  ]

def j_vardecls():
  return [
    'protected GraphicsContext gc;',
    'protected Canvas c;',
    'protected Scene s;',
    'protected String dlevel="INFO";',
    'protected volatile boolean dragging=false;',
    'protected double pmouseX=-1.0;',
    'protected double pmouseY=-1.0;',
    'protected double t=0.0;',
    'protected double dt=0.05;',
    'protected long frameinterval=10;',
    'protected int mouseX=0;',
    'protected int mouseY=0;'
  ]
