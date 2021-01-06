import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.HashMap;
import java.util.ArrayList;
import java.io.FileWriter;
import java.io.PrintWriter;

public class transgraph{
  static List<String> stmts=new ArrayList<String>();
  static HashMap<String,String> symtab=new HashMap<String,String>();
  static List<String> staq=new ArrayList<String>();
  static String INDENT_PREF="  ";
  
  static void d(String msg){
    System.out.println(msg);
  }
  
  static void f(String msg){
    System.out.println("[ERROR] "+msg);
    System.exit(0);
  }
  
  static void u(){
    d("usage: java transgraph <genartfile>");
    System.exit(0);
  }
  
  static void push(String s){
    staq.add(s);
  }
  
  static String pop(){
    if(staq.isEmpty()){
      return null;
    }
    return staq.remove(staq.size()-1);
  }
  
  static String top(){
    if(staq.isEmpty()){
      return null;
    }
    return staq.get(staq.size()-1);
  }
  
  static String interpolateline(String ln){
    int ptr=0;
    String interpln=ln;
    for(;;){
      if(ptr>=ln.length()){break;}
      int idx=ln.indexOf("#[",ptr);
      if(idx==-1){break;}
      int xbeg=idx+2;
      int xend=ln.indexOf("]",xbeg);
      if(xend==-1){throw new RuntimeException("expression did not end");}
      String k=ln.substring(xbeg,xend);
      String v=symtab.get(k);
      if(v==null){throw new RuntimeException("no such global symbol: "+v);}
      interpln=interpln.replace("#["+k+"]",v);
      ptr=xend+1;
    }
    return interpln;
  }
  
  static void rendercode(String tmplfn){
    String outfn=symtab.get("outfn");
    String clsnm=symtab.get("clsnm");
    try(
      FileWriter fw=new FileWriter(outfn);
      PrintWriter pw=new PrintWriter(fw);
    ){
      List<String> tlns=Files.readAllLines(Paths.get(tmplfn));
      for(String ln:tlns){
        if(ln.contains("$$genart$$")){
          int iloc=ln.indexOf("$$genart$$");
          String prespace=ln.substring(0,iloc);
          for(String stmt:stmts){
            pw.printf("%s%s\n",prespace,stmt);
          }
        }else{
          String interpline=interpolateline(ln);
          pw.println(interpline);
        }
      }
    }catch(Exception e){
      e.printStackTrace();
    }
  }
  
  static String genindent(){
    if(top()==null){
      return "";
    }
    StringBuffer sb=new StringBuffer();
    for(int i=0;i<staq.size();i++){
      sb.append(INDENT_PREF);
    }
    return sb.toString();
  }
  
  static String scope(){
    String t=top();
    if(t==null){
      return "";
    }
    return t;
  }
  
  static void processdirective(String car,String cdr){
    d("TODO");
  }
  
  static void transmuteline(String ln){
    String line=ln.strip();
    String car,cdr;
    if(line.contains(" ")){
      int ispc=line.indexOf(" ");
      car=line.substring(0,ispc);
      cdr=line.substring(ispc+1);
    }else{
      car=line;
      cdr="";
    }
    // no-ops
    if(line.length()==0) return;
    if(line.startsWith("#")) return;
    // special-ops
    if(car.startsWith("@")){
      processdirective(car,cdr);
      return;
    }
    // commands
    if(car.equals("print")){
      String jgen=String.format("%sSystem.out.println(%s);",genindent(),cdr);
      stmts.add(jgen);
    }else if(car.equals("let")){
      String[] args=cdr.split(" ");
      // validate let syntax
      if(!args[1].equals("be")){
        String exmsg=String.format("%slet statement syntax violated. found '%s' instead of 'be'",genindent(),args[1]);
        throw new RuntimeException(exmsg);
      }
      String vnm=args[0];
      String vval=args[2];
      if("global".equals(scope())){
        symtab.put(vnm,vval);
      }else{
        String jgen=String.format("%svar %s=%s;",genindent(),vnm,vval);
        stmts.add(jgen);
      }
    }else if(car.equals("line")){
      String[] args=cdr.split(" ");
      String jgen=String.format("%sgc.strokeLine(%s,%s,%s,%s);",genindent(),args[0],args[1],args[2],args[3]);
      stmts.add(jgen);
    }else if(car.equals("inc")){
      String[] args=cdr.split(" ");
      stmts.add(String.format("%s%s+=%s;",genindent(),args[0],args[1]));
    }else if(car.equals("end")){
      String currscope=pop();
      if(!currscope.equals("global")){
        stmts.add(String.format("%s}",genindent()));
      }
    }else if(car.equals("repeat")){
      String[] args=cdr.split(" ");
      if(!args[1].equals("times")){
        throw new RuntimeException(
          String.format("[error] '%s' found instead of 'times'",args[1]));
      }
      try{
        Integer.parseInt(args[0]);
      }catch(NumberFormatException nfe){
        throw new RuntimeException("repeat command accepts only integers!");
      }
      String jgen=String.format("%sfor(int i=0;i<%s;i++){",genindent(),args[0]);
      stmts.add(jgen);
      push("repeat");
    }else if(car.equals("global")){
      if("global".equals(scope())){
        throw new RuntimeException("cannot nest global scopes!");
      }
      push("global");
    }else if(car.equals("wait")){
      stmts.add(String.format("%sThread.sleep(%s);",genindent(),cdr));
    }
  }
  
  public static void main(String[] args){
    if(args.length!=1) { u(); }
    d(args[0]);
    try{
      String fn=args[0];
      String[] nmext=fn.split("\\.");
      String clsnm=nmext[0];
      String gaext=nmext[1];
      if(!gaext.equals("ga")){
        d("genartfile must have extension .ga!");
      }
      List<String> lines=Files.readAllLines(Paths.get(fn));
      for(String ln:lines){
        transmuteline(ln);
      }
      symtab.put("outfn",clsnm+".java");
      symtab.put("clsnm",clsnm);
      rendercode("FXTemplate.java");
    }catch(IOException e){
      e.printStackTrace();
    }
  }
  
}
